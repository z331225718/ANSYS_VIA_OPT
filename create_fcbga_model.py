"""
This script uses pyaedt to create a detailed, parametric FCBGA differential pair model in Ansys HFSS.

It reads all geometric and material parameters from an external XML file (fcbga_parameters.xml),
builds the model, and saves the project. It adheres to HFSS variable naming conventions (no '$' prefix, no hyphens).
"""
import os
import traceback
import xml.etree.ElementTree as ET
from ansys.aedt.core import Hfss

class FcbgaModeler:
    """Manages the creation of a complex parametric FCBGA model from an XML file."""

    def __init__(self, project_path, project_name, xml_path, ball_map_type, aedt_version="2023.2"):
        self.project_path = project_path
        self.project_name = project_name
        self.xml_path = xml_path
        self.ball_map_type = ball_map_type
        self.full_project_path = os.path.join(project_path, f"{project_name}.aedt")
        self.aedt_version = aedt_version
        self.hfss = None
        self.modeler = None
        
        # Initialize all data dictionaries
        self.stackup_info = {}
        self.via_styles = {}
        self.ball_style = {}
        self.routing_rules = {}
        self.z_coordinates = {}
        self.material_props = {}
        self.ball_map_settings = {}
        self.model_settings = {}

        # Lists to keep track of created parts
        self.p_path_parts = []
        self.n_path_parts = []
        self.g_ball_parts = []
        self.p_ball_parts = []
        self.n_ball_parts = []
        self.clearance_parts = []
        
        # To store ball positions for port creation
        self.p_ball_positions = []
        self.n_ball_positions = []
        self.gnd_anchor_pos = None # To store a reliable point on the GND plane

        print(f"Project will be saved to: {self.full_project_path}")
        print(f"Reading parameters from: {self.xml_path}")
        print(f"Using ball map type: {self.ball_map_type}")

    @staticmethod
    def sanitize_name(name):
        return name.replace('-', '_')

    def setup_aedt(self):
        """Initializes AEDT and sets up the HFSS design."""
        print(f"Launching AEDT version {self.aedt_version}...")
        self.hfss = Hfss(
            version=self.aedt_version,
            new_desktop=True,
            close_on_exit=False,
            project=self.project_name,
            design="FCBGA_Differential_Pair_From_XML"
        )
        self.modeler = self.hfss.modeler
        print("AEDT session and HFSS design created successfully.")

    def define_variables_and_materials(self):
        """Parses XML, defines HFSS variables, and populates instance dictionaries."""
        print("Parsing XML and defining design variables and materials...")
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        # 1. Stackup Information
        self.hfss["z_start"] = "0mm"
        current_z_expr = "z_start"
        for layer in root.findall('./stackup/layer'):
            name = layer.get('name')
            name_s = self.sanitize_name(name)
            thickness = layer.get('thickness')
            thickness_var = f"t_{name_s}"
            self.hfss[thickness_var] = thickness
            
            z_top_var = f"z_{name_s}_top"
            self.hfss[z_top_var] = current_z_expr
            self.z_coordinates[name_s] = z_top_var
            
            self.stackup_info[name] = {
                'type': layer.get('type'),
                'material': layer.get('material'),
                'filling_material': layer.get('filling_material'),
                'thickness_val': thickness,
                'thickness_var': thickness_var,
                'z_top_var': z_top_var,
                'z_bottom_expr': f"{z_top_var} - {thickness_var}"
            }
            current_z_expr = self.stackup_info[name]['z_bottom_expr']

        # 2. Via Styles
        for via in root.findall('./via_styles/via'):
            name = via.get('name')
            self.via_styles[name] = {}
            for param, value in via.attrib.items():
                if param != 'name':
                    var_name = f"{self.sanitize_name(name)}_{param}"
                    self.hfss[var_name] = value
                    self.via_styles[name][param] = value

        # 3. Ball Style
        ball_element = root.find('./ball_style/ball')
        if ball_element is not None:
            self.ball_style = {}
            for param, value in ball_element.attrib.items():
                var_name = f"ball_{param}"
                self.hfss[var_name] = value
                self.ball_style[param] = value
            # Add radius for easier use later
            self.hfss["ball_radius"] = "ball_diameter/2"
            self.ball_style["radius_var"] = "ball_radius"


        # 4. Routing Rules
        for rule in root.findall('./routing_rules/rule'):
            layer_name = rule.get('layer')
            self.routing_rules[layer_name] = {}
            for param, value in rule.attrib.items():
                if param != 'layer':
                    var_name = f"{self.sanitize_name(layer_name)}_trace_{param}"
                    self.hfss[var_name] = value
                    self.routing_rules[layer_name][param] = value

        # 5. Material Properties
        for mat in root.findall('./materials_properties/material'):
            name = mat.get('name')
            self.material_props[name] = {
                "permittivity": mat.get('permittivity'),
                "loss_tangent": mat.get('loss_tangent')
            }
        
        if "solder" not in self.hfss.materials:
            solder_mat = self.hfss.materials.add_material("solder")
            solder_mat.conductivity = 4.1e6
            solder_mat.permittivity = 1
            print("      - Created new material 'solder'.")

        # 6. Ball Map Settings
        for ball_map in root.findall('./ball_maps/ball_map'):
            if ball_map.get('type') == self.ball_map_type:
                self.ball_map_settings = ball_map.attrib
                print(f"      - Loaded ball map settings for '{self.ball_map_type}'.")
                break

        # 7. Model Settings
        model_settings_node = root.find('./model_settings')
        if model_settings_node is not None:
            self.model_settings = model_settings_node.attrib
            print(f"      - Loaded model settings: {self.model_settings}")
        else:
            self.model_settings['margin'] = '0.5mm' # Default value
            print("      - WARNING: Model settings not found in XML, using default margin.")

        print("All variables and materials from XML have been defined in HFSS and Python.")

    def _create_stacked_via(self, base_name, x_pos_var, y_pos_var, segments):
        """Creates a complex stacked via from a list of segments."""
        safe_base_name = self.sanitize_name(base_name)
        all_parts = []
        for i, (start_layer, end_layer, via_style_name) in enumerate(segments):
            start_layer_s, end_layer_s, via_style_s = [self.sanitize_name(s) for s in [start_layer, end_layer, via_style_name]]
            z_start_var = self.z_coordinates[start_layer_s]
            z_end_var = self.z_coordinates[end_layer_s]
            height_expr = f"{z_start_var} - {z_end_var}"
            drill_d_var, pad_up_d_var, pad_down_d_var = [f"{via_style_s}_{p}" for p in ["drill_diameter", "pad_diameter_up", "pad_diameter_down"]]
            
            drill = self.modeler.create_cylinder("Z", [x_pos_var, y_pos_var, z_start_var], f"{drill_d_var}/2", f"-({height_expr})", name=f"{safe_base_name}_drill_{i}")
            all_parts.append(drill)
            if i == 0:
                all_parts.append(self.modeler.create_cylinder("Z", [x_pos_var, y_pos_var, z_start_var], f"{pad_up_d_var}/2", f"-t_{start_layer_s}", name=f"{safe_base_name}_pad_up"))
            all_parts.append(self.modeler.create_cylinder("Z", [x_pos_var, y_pos_var, z_end_var], f"{pad_down_d_var}/2", f"-t_{end_layer_s}", name=f"{safe_base_name}_pad_shared_{i}"))
        
        if all_parts:
            united_object_name = self.modeler.unite(all_parts, keep_originals=False)
            if united_object_name != safe_base_name:
                 self.modeler[united_object_name].name = safe_base_name
            return self.modeler[safe_base_name]
        return None

    def _get_layer_z_center_expr(self, layer_name):
        """Returns a string expression for the Z-center of a copper layer."""
        layer_name_s = self.sanitize_name(layer_name)
        z_top_var = self.z_coordinates[layer_name_s]
        thickness_var = f"t_{layer_name_s}"
        return f"({z_top_var}) - ({thickness_var}/2)"

    def _create_differential_trace_parametric(self, layer_name, p_start_x, p_start_y, n_start_x, n_start_y, p_end_x, p_end_y, n_end_x, n_end_y):
        """Creates a fully parametric 4-point differential trace."""
        layer_name_s = self.sanitize_name(layer_name)
        z_center_expr = self._get_layer_z_center_expr(layer_name)
        width_var = f"{layer_name_s}_trace_width"
        gap_var = f"{layer_name_s}_trace_gap"
        thickness_var = f"t_{layer_name_s}"

        p_trace_x_expr = f"-(({gap_var}/2) + ({width_var}/2))"
        n_trace_x_expr = f"(({gap_var}/2) + ({width_var}/2))"

        p2_y_expr = f"{p_start_y} + abs({p_trace_x_expr} - ({p_start_x}))"
        p3_y_expr = f"{p_end_y} - abs({p_end_x} - ({p_trace_x_expr}))"
        n2_y_expr = f"{n_start_y} + abs({n_trace_x_expr} - ({n_start_x}))"
        n3_y_expr = f"{n_end_y} - abs({n_end_x} - ({n_trace_x_expr}))"

        p_points = [[p_start_x, p_start_y, z_center_expr], [p_trace_x_expr, p2_y_expr, z_center_expr], [p_trace_x_expr, p3_y_expr, z_center_expr], [p_end_x, p_end_y, z_center_expr]]
        n_points = [[n_start_x, n_start_y, z_center_expr], [n_trace_x_expr, n2_y_expr, z_center_expr], [n_trace_x_expr, n3_y_expr, z_center_expr], [n_end_x, n_end_y, z_center_expr]]

        p_trace = self.modeler.create_polyline(points=p_points, name=f"P_Trace_{layer_name_s}", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        n_trace = self.modeler.create_polyline(points=n_points, name=f"N_Trace_{layer_name_s}", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        self.p_path_parts.append(p_trace.name)
        self.n_path_parts.append(n_trace.name)

    def _create_differential_trace_halved(self, layer_name, p_start_x, p_start_y, n_start_x, n_start_y, trace_length_var):
        """Creates a fully parametric 3-point differential trace with a 45-degree start."""
        layer_name_s = self.sanitize_name(layer_name)
        z_center_expr = self._get_layer_z_center_expr(layer_name)
        width_var = f"{layer_name_s}_trace_width"
        gap_var = f"{layer_name_s}_trace_gap"
        thickness_var = f"t_{layer_name_s}"

        p_trace_x_expr = f"-(({gap_var}/2) + ({width_var}/2))"
        n_trace_x_expr = f"(({gap_var}/2) + ({width_var}/2))"

        p2_y_expr = f"{p_start_y} + abs({p_trace_x_expr} - ({p_start_x}))"
        n2_y_expr = f"{n_start_y} + abs({n_trace_x_expr} - ({n_start_x}))"

        p_points = [[p_start_x, p_start_y, z_center_expr], [p_trace_x_expr, p2_y_expr, z_center_expr], [p_trace_x_expr, f"{p_start_y} + {trace_length_var}", z_center_expr]]
        n_points = [[n_start_x, n_start_y, z_center_expr], [n_trace_x_expr, n2_y_expr, z_center_expr], [n_trace_x_expr, f"{n_start_y} + {trace_length_var}", z_center_expr]]

        p_trace = self.modeler.create_polyline(points=p_points, name=f"P_Trace_{layer_name_s}", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        n_trace = self.modeler.create_polyline(points=n_points, name=f"N_Trace_{layer_name_s}", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        self.p_path_parts.append(p_trace.name)
        self.n_path_parts.append(n_trace.name)

    def _create_via_connection_trace(self, layer_name, p_via1_x, p_via1_y, n_via1_x, n_via1_y, p_via2_x, p_via2_y, n_via2_x, n_via2_y):
        """Creates a simple parametric 2-point trace to connect two vias on a shared layer."""
        layer_name_s = self.sanitize_name(layer_name)
        z_center_expr = self._get_layer_z_center_expr(layer_name)
        width_var = f"{layer_name_s}_trace_width"
        thickness_var = f"t_{layer_name_s}"

        p_points = [[p_via1_x, p_via1_y, z_center_expr], [p_via2_x, p_via2_y, z_center_expr]]
        n_points = [[n_via1_x, n_via1_y, z_center_expr], [n_via2_x, n_via2_y, z_center_expr]]

        p_conn = self.modeler.create_polyline(points=p_points, name=f"P_Trace_{layer_name_s}_conn", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        n_conn = self.modeler.create_polyline(points=n_points, name=f"N_Trace_{layer_name_s}_conn", xsection_type="Rectangle", xsection_width=width_var, xsection_height=thickness_var)
        self.p_path_parts.append(p_conn.name)
        self.n_path_parts.append(n_conn.name)

    def create_signal_and_gnd_paths(self):
        """Creates the full signal and GND paths including balls, vias, and traces."""
        print("Creating signal and GND paths...")
        
        # 1. Define Ball and Pad Geometry
        self.hfss["p_ball_x"] = "-ball_pitch/2"
        self.hfss["n_ball_x"] = "ball_pitch/2"
        self.hfss["y_ball"] = "0mm"
        z_ball_pad_top = self.z_coordinates["Cu10"]
        z_ball_bottom = f"{z_ball_pad_top} - t_Cu10"
        p_pad = self.modeler.create_cylinder("Z", ["p_ball_x", "y_ball", z_ball_pad_top], "ball_pad_diameter/2", "-t_Cu10", name="P_Ball_Pad")
        n_pad = self.modeler.create_cylinder("Z", ["n_ball_x", "y_ball", z_ball_pad_top], "ball_pad_diameter/2", "-t_Cu10", name="N_Ball_Pad")
        self.p_path_parts.append(p_pad.name)
        self.n_path_parts.append(n_pad.name)

        p_ball = self.modeler.create_cylinder("Z", ["p_ball_x", "y_ball", z_ball_bottom], "ball_diameter/2", "-ball_height", name="P_Ball")
        p_ball.material_name = "solder"
        self.p_ball_parts.append(p_ball.name)
        n_ball = self.modeler.create_cylinder("Z", ["n_ball_x", "y_ball", z_ball_bottom], "ball_diameter/2", "-ball_height", name="N_Ball")
        n_ball.material_name = "solder"
        self.n_ball_parts.append(n_ball.name)

        # 2. GND Balls and Pads
        gnd_coords = []
        if self.ball_map_settings.get('type') == 'outer':
            gnd_coords = [("-ball_pitch*1.5", "y_ball"), ("ball_pitch*1.5", "y_ball"), ("-ball_pitch*1.5", "y_ball + ball_pitch"), ("-ball_pitch*0.5", "y_ball + ball_pitch"), ("ball_pitch*0.5", "y_ball + ball_pitch"), ("ball_pitch*1.5", "y_ball + ball_pitch")]
        elif self.ball_map_settings.get('type') == 'inner':
            gnd_coords = [("-ball_pitch*1.5", "y_ball - ball_pitch"), ("-ball_pitch*0.5", "y_ball - ball_pitch"), ("ball_pitch*0.5", "y_ball - ball_pitch"), ("ball_pitch*1.5", "y_ball - ball_pitch"), ("-ball_pitch*1.5", "y_ball"), ("ball_pitch*1.5", "y_ball"), ("-ball_pitch*1.5", "y_ball + ball_pitch"), ("-ball_pitch*0.5", "y_ball + ball_pitch"), ("ball_pitch*0.5", "y_ball + ball_pitch"), ("ball_pitch*1.5", "y_ball + ball_pitch")]

        for i, (x, y) in enumerate(gnd_coords):
            gnd_ball = self.modeler.create_cylinder("Z", [x, y, z_ball_bottom], "ball_diameter/2", "-ball_height", name=f"GND_Ball_{i}")
            gnd_ball.material_name = "solder"
            self.g_ball_parts.append(gnd_ball.name)
            if i == 0:
                self.gnd_anchor_pos = [x, y] # Store the parametric position of the first GND ball

        # 3. Define Via Pitches and X-Coordinates
        self.hfss["p_x_via8_10"], self.hfss["n_x_via8_10"] = "-Via_8_10_pitch/2", "Via_8_10_pitch/2"
        self.hfss["p_x_via6_8"], self.hfss["n_x_via6_8"] = "-Via_6_8_pitch/2", "Via_6_8_pitch/2"
        self.hfss["p_x_via5_6"], self.hfss["n_x_via5_6"] = "-Via_5_6_pitch/2", "Via_5_6_pitch/2"
        self.hfss["p_x_via3_5"], self.hfss["n_x_via3_5"] = "-Via_3_5_pitch/2", "Via_3_5_pitch/2"
        self.hfss["p_x_via1_3"], self.hfss["n_x_via1_3"] = "-Via_1_3_pitch/2", "Via_1_3_pitch/2"

        # 4. Calculate Y-Coordinates
                # 4. Calculate Y-Coordinates with robust conditional logic
        # Condition to check if tangency is geometrically possible
        self.hfss["cond_10_8"] = "(ball_pad_diameter/2 + Via_9_10_pad_diameter_down/2)^2 - (p_ball_x - p_x_via8_10)^2 >= 0"
        self.hfss["y_via8_10"] = "y_ball + if(cond_10_8, sqrt((ball_pad_diameter/2 + Via_9_10_pad_diameter_down/2)^2 - (p_ball_x - p_x_via8_10)^2), 0)"

        self.hfss["l_cu8_trace_fixed"] = "1/2*ball_antipad_diameter + 1/2*Via_5_6_pad_diameter_down"
        self.hfss["y_via6_8_from_fixed_trace"] = "y_via8_10 + l_cu8_trace_fixed"

        # Condition for Via_6_8 and Via_5_6 tangency
        self.hfss["cond_6_5"] = "(Via_6_7_pad_diameter_up/2 + Via_5_6_pad_diameter_down/2)^2 - (p_x_via6_8 - p_x_via5_6)^2 >= 0"
        self.hfss["y_via5_6_if_fixed"] = "y_via6_8_from_fixed_trace + if(cond_6_5, sqrt((Via_6_7_pad_diameter_up/2 + Via_5_6_pad_diameter_down/2)^2 - (p_x_via6_8 - p_x_via5_6)^2), 0)"
        
        self.hfss["y_via5_6_min_clearance"] = "(1/2*ball_antipad_diameter + 1/2*Via_5_6_pad_diameter_down) + Via_5_6_antipad_diameter/2"
        self.hfss["y_via5_6"] = "max(y_via5_6_if_fixed, y_via5_6_min_clearance)"

        # Final Y coordinates using the conditional logic
        self.hfss["y_via6_8"] = "y_via5_6 - if(cond_6_5, sqrt((Via_6_7_pad_diameter_up/2 + Via_5_6_pad_diameter_down/2)^2 - (p_x_via6_8 - p_x_via5_6)^2), 0)"

        self.hfss["cond_5_3"] = "(Via_5_6_pad_diameter_up/2 + Via_4_5_pad_diameter_down/2)^2 - (p_x_via5_6 - p_x_via3_5)^2 >= 0"
        self.hfss["y_via3_5"] = "y_via5_6 + if(cond_5_3, sqrt((Via_5_6_pad_diameter_up/2 + Via_4_5_pad_diameter_down/2)^2 - (p_x_via5_6 - p_x_via3_5)^2), 0)"

        self.hfss["cond_3_1"] = "(Via_3_4_pad_diameter_up/2 + Via_2_3_pad_diameter_down/2)^2 - (p_x_via3_5 - p_x_via1_3)^2 >= 0"
        self.hfss["y_via1_3"] = "y_via3_5 + if(cond_3_1, sqrt((Via_3_4_pad_diameter_up/2 + Via_2_3_pad_diameter_down/2)^2 - (p_x_via3_5 - p_x_via1_3)^2), 0)" 

        # 5. Create Vias
        p_via_8_10 = self._create_stacked_via("P_Via_8_10", "p_x_via8_10", "y_via8_10", [("Cu8", "Cu9", "Via_8-9"), ("Cu9", "Cu10", "Via_9-10")])
        n_via_8_10 = self._create_stacked_via("N_Via_8_10", "n_x_via8_10", "y_via8_10", [("Cu8", "Cu9", "Via_8-9"), ("Cu9", "Cu10", "Via_9-10")])
        self.p_path_parts.append(p_via_8_10.name)
        self.n_path_parts.append(n_via_8_10.name)

        p_via_6_8 = self._create_stacked_via("P_Via_6_8", "p_x_via6_8", "y_via6_8", [("Cu6", "Cu7", "Via_6-7"), ("Cu7", "Cu8", "Via_7-8")])
        n_via_6_8 = self._create_stacked_via("N_Via_6_8", "n_x_via6_8", "y_via6_8", [("Cu6", "Cu7", "Via_6-7"), ("Cu7", "Cu8", "Via_7-8")])
        self.p_path_parts.append(p_via_6_8.name)
        self.n_path_parts.append(n_via_6_8.name)

        p_via_5_6 = self._create_stacked_via("P_Via_5_6", "p_x_via5_6", "y_via5_6", [("Cu5", "Cu6", "Via_5-6")])
        n_via_5_6 = self._create_stacked_via("N_Via_5_6", "n_x_via5_6", "y_via5_6", [("Cu5", "Cu6", "Via_5-6")])
        self.p_path_parts.append(p_via_5_6.name)
        self.n_path_parts.append(n_via_5_6.name)

        p_via_3_5 = self._create_stacked_via("P_Via_3_5", "p_x_via3_5", "y_via3_5", [("Cu3", "Cu4", "Via_3-4"), ("Cu4", "Cu5", "Via_4-5")])
        n_via_3_5 = self._create_stacked_via("N_Via_3_5", "n_x_via3_5", "y_via3_5", [("Cu3", "Cu4", "Via_3-4"), ("Cu4", "Cu5", "Via_4-5")])
        self.p_path_parts.append(p_via_3_5.name)
        self.n_path_parts.append(n_via_3_5.name)

        p_via_1_3 = self._create_stacked_via("P_Via_1_3", "p_x_via1_3", "y_via1_3", [("Cu1", "Cu2", "Via_1-2"), ("Cu2", "Cu3", "Via_2-3")])
        n_via_1_3 = self._create_stacked_via("N_Via_1_3", "n_x_via1_3", "y_via1_3", [("Cu1", "Cu2", "Via_1-2"), ("Cu2", "Cu3", "Via_2-3")])
        self.p_path_parts.append(p_via_1_3.name)
        self.n_path_parts.append(n_via_1_3.name)

        # 6. Connect Tangent Vias and Pads
        self._create_via_connection_trace("Cu10", "p_x_via8_10", "y_via8_10", "n_x_via8_10", "y_via8_10", "p_ball_x", "y_ball", "n_ball_x", "y_ball")
        self._create_via_connection_trace("Cu6", "p_x_via5_6", "y_via5_6", "n_x_via5_6", "y_via5_6", "p_x_via6_8", "y_via6_8", "n_x_via6_8", "y_via6_8")
        self._create_via_connection_trace("Cu5", "p_x_via3_5", "y_via3_5", "n_x_via3_5", "y_via3_5", "p_x_via5_6", "y_via5_6", "n_x_via5_6", "y_via5_6")
        self._create_via_connection_trace("Cu3", "p_x_via1_3", "y_via1_3", "n_x_via1_3", "y_via1_3", "p_x_via3_5", "y_via3_5", "n_x_via3_5", "y_via3_5")

        # 7. Create Main Traces
        self._create_differential_trace_parametric("Cu8", "p_x_via8_10", "y_via8_10", "n_x_via8_10", "y_via8_10", "p_x_via6_8", "y_via6_8", "n_x_via6_8", "y_via6_8")
        self.hfss["l_cu1_trace"] = "1mm"
        self.hfss["y_cu1_end"] = "y_via1_3 + l_cu1_trace"
        self._create_differential_trace_halved("Cu1", "p_x_via1_3", "y_via1_3", "n_x_via1_3", "y_via1_3", "l_cu1_trace")
        
        # 8. Unite all signal path components
        if self.p_path_parts:
            p_main_part_name = self.modeler.unite(self.p_path_parts, keep_originals=False)
            self.modeler[p_main_part_name].name = "P_Path"
            self.hfss.modeler["P_Path"].material_name = "copper"
        
        if self.n_path_parts:
            n_main_part_name = self.modeler.unite(self.n_path_parts, keep_originals=False)
            self.modeler[n_main_part_name].name = "N_Path"
            self.hfss.modeler["N_Path"].material_name = "copper"

        print("Signal and GND paths created.")

    def _create_antipad(self, name, x_pos_p_var, x_pos_n_var, y_pos_var, pitch_var, antipad_d_var, start_layer_name, end_layer_name):
        """Helper function to create a full anti-pad structure for a differential pair."""
        safe_name = self.sanitize_name(name)
        start_layer_s = self.sanitize_name(start_layer_name)
        end_layer_s = self.sanitize_name(end_layer_name)
        z_start_var = self.z_coordinates[start_layer_s]
        z_end_var = self.z_coordinates[end_layer_s]
        height_expr = f"{z_start_var} - ({z_end_var} - t_{end_layer_s})"
        
        p_cyl = self.modeler.create_cylinder("Z", [x_pos_p_var, y_pos_var, z_start_var], f"{antipad_d_var}/2", f"-({height_expr})", name=f"{safe_name}_p_cyl")
        n_cyl = self.modeler.create_cylinder("Z", [x_pos_n_var, y_pos_var, z_start_var], f"{antipad_d_var}/2", f"-({height_expr})", name=f"{safe_name}_n_cyl")
        box = self.modeler.create_box(origin=[x_pos_p_var, f"{y_pos_var} - {antipad_d_var}/2", z_start_var], sizes=[pitch_var, antipad_d_var, f"-({height_expr})"], name=f"{safe_name}_box")
        
        united_antipad_name = self.modeler.unite([p_cyl, n_cyl, box], keep_originals=False)
        if united_antipad_name != safe_name:
            self.modeler[united_antipad_name].name = safe_name
        self.clearance_parts.append(safe_name)

    def create_clearances(self):
        """Creates all anti-pad and trace clearance geometries as per rules."""
        print("Creating all clearance geometries...")
        self._create_antipad("Antipad_Ball", "p_ball_x", "n_ball_x", "y_ball", "ball_pitch", "ball_antipad_diameter", "Cu3", "Cu10")
        self._create_antipad("Antipad_Via_8_10", "p_x_via8_10", "n_x_via8_10", "y_via8_10", "Via_8_10_pitch", "Via_8_10_antipad_diameter", "Cu8", "Cu10")
        self._create_antipad("Antipad_Via_6_8", "p_x_via6_8", "n_x_via6_8", "y_via6_8", "Via_6_8_pitch", "Via_6_8_antipad_diameter", "Cu6", "Cu8")
        self._create_antipad("Antipad_Via_5_6", "p_x_via5_6", "n_x_via5_6", "y_via5_6", "Via_5_6_pitch", "Via_5_6_antipad_diameter", "Cu4", "Cu7")
        self._create_antipad("Antipad_Via_3_5", "p_x_via3_5", "n_x_via3_5", "y_via3_5", "Via_3_5_pitch", "Via_3_5_antipad_diameter", "Cu3", "Cu5")
        self._create_antipad("Antipad_Via_1_3", "p_x_via1_3", "n_x_via1_3", "y_via1_3", "Via_1_3_pitch", "Via_1_3_antipad_diameter", "Cu1", "Cu3")

        self.hfss["clearance_w_cu1"] = "2*(Cu1_trace_width + Cu1_trace_space + Cu1_trace_gap)"
        self.hfss["clearance_w_cu8"] = "2*(Cu8_trace_width + Cu8_trace_space + Cu8_trace_gap)"
        clearance_cu1 = self.modeler.create_box(origin=["-clearance_w_cu1/2", "y_via1_3", self.z_coordinates["Cu1"]], sizes=["clearance_w_cu1", "l_cu1_trace", "-t_Cu1"], name="Clearance_Cu1")
        clearance_cu8 = self.modeler.create_box(origin=["-clearance_w_cu8/2", "y_via8_10", self.z_coordinates["Cu8"]], sizes=["clearance_w_cu8", "y_via6_8 - y_via8_10", "-t_Cu8"], name="Clearance_Cu8")
        self.clearance_parts.extend([clearance_cu1.name, clearance_cu8.name])
        print("Clearance geometry creation completed.")

    def perform_subtraction(self):
        """Subtracts all clearance objects from the copper layers."""
        print("Performing boolean subtractions...")
        # Get only the copper layer names for subtraction
        copper_layers = [self.sanitize_name(layer.get('name')) for layer in ET.parse(self.xml_path).findall('./stackup/layer') if layer.get('type') == 'signal']
        
        # Subtract the clearance parts from the copper layers to form the GND planes
        if self.clearance_parts and copper_layers:
            self.modeler.subtract(blank_list=copper_layers, tool_list=self.clearance_parts, keep_originals=False)
            print("Subtractions completed.")
        else:
            print("No clearance parts or copper layers to perform subtraction.")

    def create_stackup_and_boundaries(self):
        """Creates the stackup geometry, including copper layers and their corresponding filling dielectrics."""
        print("Creating stackup geometry with dynamic boundaries...")

        # Define parametric model boundaries
        margin = self.model_settings.get('margin', '0.5mm') # Get margin from settings
        self.hfss["model_x_margin"] = margin
        self.hfss["model_y_margin"] = margin
        self.hfss["gnd_x_max"] = "ball_pitch*1.5 + ball_pad_diameter/2"
        self.hfss["gnd_x_min"] = "-gnd_x_max"
        self.hfss["model_x_min"] = "gnd_x_min - model_x_margin"
        self.hfss["model_x_size"] = "gnd_x_max - gnd_x_min + 2*model_x_margin"
        self.hfss["model_y_min"] = f"{self.ball_map_settings.get('dielectric_layer_y_start', '-1.5mm')}"
        self.hfss["model_y_max"] = "y_cu1_end + model_y_margin"
        self.hfss["model_y_size"] = "model_y_max - model_y_min"

        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        for layer in root.findall('./stackup/layer'):
            layer_name_orig = layer.get('name')
            layer_name_s = self.sanitize_name(layer_name_orig)
            layer_type = layer.get('type')
            layer_material = layer.get('material')
            z_top_var = self.z_coordinates[layer_name_s]
            thickness_var = f"t_{layer_name_s}"

            y_start_var = self.ball_map_settings.get('signal_layer_y_start') if layer_type == 'signal' else "model_y_min"
            y_size_expr = f"model_y_max - ({y_start_var})" if layer_type == 'signal' else "model_y_size"
            x_start_var = "model_x_min"
            x_size_expr = "model_x_size"
            
            box_params = {
                "origin": [x_start_var, y_start_var, z_top_var],
                "sizes": [x_size_expr, y_size_expr, f"-({thickness_var})"],
            }

            if layer_type == 'dielectric':
                box = self.modeler.create_box(name=layer_name_s, **box_params)
                if layer_material not in self.hfss.materials:
                    if layer_material in self.material_props:
                        props = self.material_props[layer_material]
                        new_mat = self.hfss.materials.add_material(layer_material)
                        new_mat.permittivity = props["permittivity"]
                        new_mat.dielectric_loss_tangent = props["loss_tangent"]
                box.material_name = layer_material
                box.color = (100, 150, 100)
            
            elif layer_type == 'signal':
                # Create the main copper layer
                copper_box = self.modeler.create_box(name=layer_name_s, **box_params)
                copper_box.material_name = "copper"
                copper_box.color = (200, 130, 50)

                # Create the filling dielectric layer with dielectric-level dimensions
                filling_material = layer.get('filling_material')
                if filling_material:
                    filling_box_params = {
                        "origin": [x_start_var, "model_y_min", z_top_var],
                        "sizes": [x_size_expr, "model_y_size", f"-({thickness_var})"],
                    }
                    filling_box = self.modeler.create_box(name=f"Filling_{layer_name_s}", **filling_box_params)
                    if filling_material not in self.hfss.materials:
                        if filling_material in self.material_props:
                            props = self.material_props[filling_material]
                            new_mat = self.hfss.materials.add_material(filling_material)
                            new_mat.permittivity = props["permittivity"]
                            new_mat.dielectric_loss_tangent = props["loss_tangent"]
                    filling_box.material_name = filling_material
                    filling_box.color = (120, 120, 180)  # Assign a distinct color
                    
        print("Stackup and filling layers created.")

    def set_design_settings(self):
        """设置HFSS设计参数"""
        print("设置HFSS设计参数...")
        
        # 设置设计参数
        design_settings = [
            "NAME:Design Settings Data",
            "Use Advanced DC Extrapolation:=", False,
            "Use Power S:=", False,
            "Export FRTM After Simulation:=", False,
            "Export Rays After Simulation:=", False,
            "Export After Simulation:=", False,
            "Allow Material Override:=", True,
            "Calculate Lossy Dielectrics:=", True,
            "Perform Minimal validation:=", False,
            "EnabledObjects:=", [],
            "Port Validation Settings:=", "Standard",
            "Save Adaptive support files:=", False
        ]
        
        model_validation = [
            "NAME:Model Validation Settings",
            "EntityCheckLevel:=", "Strict",
            "IgnoreUnclassifiedObjects:=", False,
            "SkipIntersectionChecks:=", False
        ]
        
        self.hfss.odesign.SetDesignSettings(design_settings, model_validation)
        print("设计参数设置完成")

    def create_air_region_and_boundary(self):
        """创建空气区域和辐射边界"""
        print("创建空气区域和辐射边界...")
        
        # 使用create_air_region方法创建空气区域
        # y_pos=0mm (+y方向为0), 其他方向为3mm
        self.modeler.create_air_region(
            x_pos=3,      # +x方向3mm
            y_pos=0,      # +y方向0mm
            z_pos=3,      # +z方向3mm
            x_neg=3,      # -x方向3mm
            y_neg=3,      # -y方向3mm
            z_neg=3,      # -z方向3mm
            is_percentage=False  # 使用absolute坐标
        )
        
        # 设置辐射边界条件
        self.hfss.assign_radiation_boundary_to_objects("Region")
        print("空气区域和辐射边界创建完成")

    def create_hfss_setup_and_sweep(self):
        """创建HFSS setup和频率扫描"""
        print("创建HFSS setup和频率扫描...")
        
        # 创建setup
        setup = self.hfss.create_setup(
            name="Setup1",
            setup_type="HFSSDriven"
        )
        setup.props["SolveType"] = 'MultiFrequency'
        setup.props["MultipleAdaptiveFreqsSetup"] = {'1GHz':[0.02],'28GHz':[0.02],'67GHz':[0.02],'100GHz':[0.02]}
        setup.props["MaximumPasses"] = 20
        setup.props["BasisOrder"] = -1
        # 创建频率扫描
        self.hfss.create_linear_step_sweep(
            setup="Setup1",
            unit="GHz",
            start_frequency=0,
            stop_frequency=100,
            step_size=0.01,
            name="Sweep",
            save_fields=False,
            sweep_type="Interpolating"
        )
        
        print("HFSS setup和频率扫描创建完成")

    def save_project_and_keep_open(self):
        """Saves the project and keeps AEDT open. Called from a finally block, so it's robust."""
        try:
            # Check if hfss object exists and is usable
            if self.hfss and getattr(self.hfss, 'project_name', None):
                if not os.path.exists(self.project_path):
                    os.makedirs(self.project_path)
                print(f"Saving project to: {self.full_project_path}")
                self.hfss.save_project(file_name=self.full_project_path)
                self.hfss.release_desktop(close_projects=False, close_desktop=False)
                print("Project saved. AEDT session remains open.")
            else:
                print("HFSS session not initialized or project not loaded. Cannot save project.")
        except Exception as e:
            # Catch potential errors during the save operation itself
            print(f"An error occurred while trying to save the project: {e}")

    def save_and_close(self):
        """Saves the project and closes AEDT."""
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        print(f"Saving project to: {self.full_project_path}")
        self.hfss.save_project(file_name=self.full_project_path)
        print("Releasing AEDT desktop session...")
        self.hfss.release_desktop(close_projects=True, close_desktop=True)
        print("Script finished.")

    def _create_terminal_port(self, port_name, sheet_object, layer_name, sheet_center):
        """Creates a terminal port using AutoIdentifyPorts via a script."""
        print(f"      - Creating terminal port '{port_name}' on layer '{layer_name}'...")
        
        # 1. Determine reference conductors dynamically
        layer_num = int(layer_name.replace('Cu', ''))
        reference_conductors = []
        if layer_num == 1:
            reference_conductors = ["Cu1", "Cu2"]
        elif layer_num == 10:
            reference_conductors = ["Cu9", "Cu10"]
        else:
            reference_conductors = [f"Cu{layer_num-1}", f"Cu{layer_num}", f"Cu{layer_num+1}"]
        
        # 2. Get face ID from the center of the sheet (center is passed directly)
        face_id = self.modeler.get_faceid_from_position(sheet_center,sheet_object.name)
        oModule = self.hfss.odesign.GetModule("BoundarySetup")
        oModule.AutoIdentifyPorts(
            [
                "NAME:Faces",
                face_id
            ],
            True,
            [
                "NAME:ReferenceConductors",
                *reference_conductors
            ],
            port_name,
            True
        )
        if not face_id:
            print(f"      - ERROR: Could not get face ID for sheet '{sheet_object.name}'. Aborting port creation.")
            return


    def create_ports_and_excitations(self):
        """Creates and assigns ports and excitations for the model, with corrected API usage."""
        print("Creating ports and excitations (Corrected)...")

        # 1. Create Port for Cu1 Differential Pair
        # -----------------------------------------
        port_layer = "Cu1"
        layer_num = int(port_layer.replace('Cu', ''))

        cu_props_main = self.stackup_info.get(port_layer)

        # Robustly determine port height and Z-origin
        if layer_num == 1:
            dielectric_above_props = self.stackup_info.get("SM_top_layer")
            dielectric_below_props = self.stackup_info.get("DRILL1-2")
            port_height_formula = f"2 * ({dielectric_above_props['thickness_var']} + {dielectric_below_props['thickness_var']})"
            port_z_origin = self.z_coordinates[self.sanitize_name("Cu2")]
        elif layer_num == 10:
            dielectric_above_props = self.stackup_info.get("DRILL9-10")
            dielectric_below_props = self.stackup_info.get("SM_BOTTOM")
            port_height_formula = f"2 * ({dielectric_above_props['thickness_var']} + {dielectric_below_props['thickness_var']})"
            port_z_origin = self.z_coordinates[self.sanitize_name("Cu10")]
        else:
            dielectric_above_props = self.stackup_info.get(f"DRILL{layer_num-1}-{layer_num}")
            dielectric_below_props = self.stackup_info.get(f"DRILL{layer_num}-{layer_num+1}")
            port_height_formula = f"{dielectric_above_props['thickness_var']} + {dielectric_below_props['thickness_var']}"
            port_z_origin = self.z_coordinates[self.sanitize_name(f"Cu{layer_num+1}")]

        if not all([cu_props_main, dielectric_above_props, dielectric_below_props]):
            print(f"      - ERROR: Missing required layer definitions for {port_layer} port. Aborting.")
            return

        line_width_var = f"{self.sanitize_name(port_layer)}_trace_width"
        line_gap_var = f"{self.sanitize_name(port_layer)}_trace_gap"
        line_space_var = f"{self.sanitize_name(port_layer)}_trace_space"
        
        port_width_formula = f"2 * (2*{line_width_var} + {line_gap_var} + 2*{line_space_var})"
        port_center_y = "y_cu1_end"
        
        # The 'origin' for create_rectangle is its center point.
        port_sheet_center = [f"-({port_width_formula})/2", port_center_y, port_z_origin]

        port_sheet_cu1 = self.hfss.modeler.create_rectangle(
            orientation='XZ',
            origin=port_sheet_center,
            sizes=[port_height_formula, port_width_formula],
            name="Port_Sheet_Cu1"
        )
        port_sheet_cu1.color = (255, 0, 255)
        
        # Use the new terminal port creation method, passing the calculated center
        self._create_terminal_port("P1", port_sheet_cu1, port_layer, port_sheet_center)

        # 2. Create Ports for BGA Balls
        # -----------------------------
        p_ball_center_x, p_ball_center_y = "p_ball_x", "y_ball"
        n_ball_center_x, n_ball_center_y = "n_ball_x", "y_ball"
        ball_z_bottom = f"({self.stackup_info['Cu10']['z_bottom_expr']}) - ball_height"

        all_created_balls = self.p_ball_parts + self.n_ball_parts + self.g_ball_parts
        if all_created_balls:
            ball_map_type = self.ball_map_settings.get('type')
            origin = None
            sizes = None
            bga_gnd_sheet = None

            if ball_map_type == 'outer': # 2-row
                origin = ["-ball_pitch*1.5 - ball_diameter/2", "ball_pitch + ball_diameter/2", ball_z_bottom]
                sizes = ["3*ball_pitch + ball_diameter", "-ball_pitch - ball_diameter - 0.3mm"]
            elif ball_map_type == 'inner': # 3-row
                origin = ["-ball_pitch*1.5 - ball_diameter/2", "ball_pitch + ball_diameter/2", ball_z_bottom]
                sizes = ["3*ball_pitch + ball_diameter", "-2*ball_pitch - ball_diameter"]

            if origin and sizes:
                bga_gnd_sheet = self.hfss.modeler.create_rectangle(
                    orientation='XY',
                    origin=origin,
                    sizes=sizes,
                    name="BGA_GND_Sheet"
                )
            else:
                print(f"      - WARNING: Unknown ball map type '{ball_map_type}'. Skipping BGA GND sheet creation.")

            if bga_gnd_sheet:
                p_port_sheet = self.hfss.modeler.create_circle(
                    orientation='XY',
                    origin=[p_ball_center_x, p_ball_center_y, ball_z_bottom],
                    radius="1.1 * ball_radius",
                    name="P_Port_Sheet_BGA"
                )
                n_port_sheet = self.hfss.modeler.create_circle(
                    orientation='XY',
                    origin=[n_ball_center_x, n_ball_center_y, ball_z_bottom],
                    radius="1.1 * ball_radius",
                    name="N_Port_Sheet_BGA"
                )
                
                self.hfss.modeler.subtract(bga_gnd_sheet, [p_port_sheet, n_port_sheet], keep_originals=True)
                self.hfss.assign_perfecte_to_sheets(bga_gnd_sheet.name)
                print(f"      - Assigned Perfect E boundary to '{bga_gnd_sheet.name}'.")

                p_axis_start = [p_ball_center_x, p_ball_center_y, ball_z_bottom]
                p_axis_end = [f"{p_ball_center_x} + 1.1 * ball_radius", p_ball_center_y, ball_z_bottom]
                n_axis_start = [n_ball_center_x, n_ball_center_y, ball_z_bottom]
                n_axis_end = [f"{n_ball_center_x} - 1.1 * ball_radius", n_ball_center_y, ball_z_bottom]

                self.hfss.lumped_port(assignment=p_port_sheet.name, integration_line=[p_axis_start, p_axis_end], reference=bga_gnd_sheet.name, impedance=50, name="P2_BGA_P")
                self.hfss.lumped_port(assignment=n_port_sheet.name, integration_line=[n_axis_start, n_axis_end], reference=bga_gnd_sheet.name, impedance=50, name="P3_BGA_N")
                print(f"      - Created lumped ports for P and N BGA balls.")
        else:
            print("      - WARNING: No ball parts found, skipping BGA port creation.")

        print("Finished creating ports and excitations.")

    def create_return_path_bodies(self):
        """Creates fully parametric, continuous return path bodies between GND planes using a non-destructive sweep-intersect method."""
        print("Creating fully parametric continuous return path bodies...")
        
        if not self.gnd_anchor_pos:
            print("  - ERROR: GND anchor position not found. Cannot create return paths.")
            return

        num_layers = len([l for l in self.stackup_info.values() if l['type'] == 'signal'])

        # Define a safe coordinate point using the parametric position of the first GND ball
        safe_x_expr = self.gnd_anchor_pos[0]
        safe_y_expr = self.gnd_anchor_pos[1]

        for i in range(1, num_layers):
            try:
                upper_cu_name = f"Cu{i}"
                lower_cu_name = f"Cu{i+1}"
                
                # Directly construct the expected dielectric name based on convention
                diel_layer_name = f"DRILL{i}-{i+1}"
                if diel_layer_name not in self.stackup_info:
                    # Fallback for other naming conventions, though less likely with current XML
                    diel_layer_name_alt = f"Dielectric_{i}"
                    if self.sanitize_name(diel_layer_name_alt) in self.z_coordinates:
                        diel_layer_name = diel_layer_name_alt
                    else:
                        print(f"  - WARNING: Could not find dielectric layer between {upper_cu_name} and {lower_cu_name}. Skipping.")
                        continue

                # Get parametric expressions for Z coordinates and thickness
                z_upper_bottom_expr = self.stackup_info[upper_cu_name]['z_bottom_expr']
                z_lower_top_expr = self.stackup_info[lower_cu_name]['z_top_var']
                diel_thickness_var = self.stackup_info[diel_layer_name]['thickness_var']

                # 1. Get Face IDs using the safe point expressions
                face_id_upper = self.modeler.get_faceid_from_position([safe_x_expr, safe_y_expr, z_upper_bottom_expr], assignment=upper_cu_name)
                face_id_lower = self.modeler.get_faceid_from_position([safe_x_expr, safe_y_expr, z_lower_top_expr], assignment=lower_cu_name)

                if not face_id_upper or not face_id_lower:
                    print(f"  - WARNING: Could not find face ID for {upper_cu_name} or {lower_cu_name}. Skipping.")
                    continue

                # 2. Create temporary, independent sheet objects from the faces
                temp_sheet_upper = self.modeler.create_object_from_face(face_id_upper)
                temp_sheet_lower = self.modeler.create_object_from_face(face_id_lower)

                # 3. Sweep the temporary sheets using parametric vectors
                swept_body1 = self.modeler.sweep_along_vector(temp_sheet_upper.name, [0, 0, f"-{diel_thickness_var}"])
                swept_body2 = self.modeler.sweep_along_vector(temp_sheet_lower.name, [0, 0, f"{diel_thickness_var}"])

                # 4. Intersect the swept bodies to get the final return path
                return_path_name = self.modeler.intersect([swept_body1.name, swept_body2.name], keep_originals=False)
                return_path_obj = self.modeler[return_path_name]
                return_path_obj.name = f"Return_Path_{self.sanitize_name(diel_layer_name)}"
                return_path_obj.material_name = "copper"
                return_path_obj.color = (0, 128, 128) # Teal color for visibility
                print(f"  - Successfully created '{return_path_obj.name}'.")

            except Exception as e:
                print(f"--- ERROR: Failed to create return path for dielectric layer between {upper_cu_name} and {lower_cu_name}. ---")
                print(f"    Exception: {e}")
                traceback.print_exc()
                break
    def run(self):
        """Executes the complete model generation workflow in the correct order."""
        try:
            self.setup_aedt()
            self.define_variables_and_materials()
            self.create_signal_and_gnd_paths() # Must be first to define all coordinate variables
            self.create_stackup_and_boundaries() # Now can use the coordinate variables
            self.create_clearances()
            self.perform_subtraction()
            self.create_ports_and_excitations()
            self.set_design_settings()  # 设置设计参数
            self.create_air_region_and_boundary()  # 创建空气区域和辐射边界
            self.create_hfss_setup_and_sweep()  # 创建HFSS setup和频率扫描
            self.create_return_path_bodies() # Create the continuous return path bodies
            self.create_differential_pairs() # Create differential pairs
            self.set_conductor_roughness() # Set copper roughness
            print("FCBGA model generation complete.")
        except Exception as e:
            print("An error occurred during the model generation:")
            traceback.print_exc() # Print detailed traceback
        finally:
            self.save_project_and_keep_open()

    def set_conductor_roughness(self):
        """Sets the copper roughness for the main signal paths using the Huray model."""
        print("Setting conductor roughness for P_Path and N_Path...")
        try:
            self.hfss.assign_finite_conductivity(
                assignment=["P_Path", "N_Path"],
                use_huray=True,
                radius="0.4um",
                ratio="1.8",
                name="Roughness_PN_Paths"
            )
            print("      - Successfully applied Huray roughness model.")
        except Exception as e:
            print(f"      - ERROR: Failed to set conductor roughness. Error: {e}")
            traceback.print_exc()

    def create_differential_pairs(self):
        """Creates differential pairs from existing terminals based on the recorded script."""
        print("Creating differential pairs...")
        try:
            oModule = self.hfss.odesign.GetModule("BoundarySetup")
            
            # Using terminal names confirmed by user, derived from conductor names 'P_Path' and 'N_Path'.
            # Correcting the P/N assignment to be logically consistent (P=Positive).
            # Using impedance values from the user's recorded script.
            diff_pairs_data = [
                "NAME:EditDiffPairs",
                [
                    "NAME:Pair1",
                    "PosBoundary:=", "P_Path_T1",  # Corrected to P for Positive
                    "NegBoundary:=", "N_Path_T1",  # Corrected to N for Negative
                    "CommonName:=", "Comm1",
                    "CommonRefZ:=", "22.5ohm",
                    "DiffName:=", "Diff1",
                    "DiffRefZ:=", "90ohm",
                    "IsActive:=", True,
                    "UseMatched:=", False
                ],
                [
                    "NAME:Pair2",
                    "PosBoundary:=", "P2_BGA_P_T1",
                    "NegBoundary:=", "P3_BGA_N_T1",
                    "CommonName:=", "Comm2",
                    "CommonRefZ:=", "22.5ohm",
                    "DiffName:=", "Diff2",
                    "DiffRefZ:=", "90ohm",
                    "IsActive:=", True,
                    "UseMatched:=", False
                ]
            ]
            
            oModule.EditDiffPairs(diff_pairs_data)
            print("      - Successfully created differential pairs.")
        except Exception as e:
            print(f"      - ERROR: Failed to create differential pairs. Error: {e}")
            traceback.print_exc()



if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file_path = os.path.join(script_dir, "fcbga_parameters.xml")
    project_dir = script_dir
    project_name = "FCBGA_From_XML_v2"
    aedt_version = "2025.2"

    if not os.path.exists(xml_file_path):
        print(f"Error: XML file not found at {xml_file_path}")
    else:
        modeler = FcbgaModeler(
            project_path=project_dir,
            project_name=project_name,
            xml_path=xml_file_path,
            ball_map_type="outer",
            aedt_version=aedt_version
        )
        modeler.run()