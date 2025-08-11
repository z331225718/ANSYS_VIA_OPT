
import os
import numpy as np
from ansys.aedt.core import Desktop, Hfss
from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args
import traceback
import copy

import logging
import time
import pandas as pd

EVALUATION_COUNT = 0
CONSECUTIVE_ZERO_COST_COUNT = 0

def check_and_remove_lock_file(project_path):
    """Checks for and removes a .lock file associated with an AEDT project."""
    lock_file_path = project_path + ".lock"
    if os.path.exists(lock_file_path):
        print(f"Found and removing stale lock file: {lock_file_path}")
        try:
            os.remove(lock_file_path)
            print("Lock file removed successfully.")
        except OSError as e:
            print(f"Error removing lock file: {e}. Please check file permissions.")

# -----------------------------------------------------------------------------
# 1. CONFIGURATION
# -----------------------------------------------------------------------------
# --- Project Details ---
PROJECT_PATH = os.path.abspath("FCBGA_From_XML_v2.aedt")
DESIGN_NAME = "FCBGA_Differential_Pair_From_XML"
SETUP_NAME = "Setup1"


# --- Iteration Control ---
TOTAL_ITERATIONS = 100 # Total number of optimization runs
STOP_AFTER_N_CONSECUTIVE_ZEROS = 2 # Set to 0 or less to disable early stopping

# --- Adaptive Search Space Parameters ---
ENABLE_ADAPTIVE_SPACE = True # Set to False to use a fixed parameter space for the entire run
GENERATION_SIZE = 20  # Number of iterations per generation
ELITE_FRACTION = 0.25  # Top 25% of results are used to determine the next search space
SPACE_SHRINK_FACTOR = 1.5  # How much to shrink the space (larger value = less shrinkage)
BOUNDARY_EDGE_FRACTION = 0.05 # Defines the "edge" of the boundary for pressure check (5%)
BOUNDARY_PRESSURE_THRESHOLD = 0.3 # Percentage of elite points needed to trigger expansion (30%)
BOUNDARY_EXPANSION_FACTOR = 0.2 # How much to expand the boundary by (20%)

# ----------------------------------------------------------------------------
# 2. COST CALCULATION STRATEGIES
# -----------------------------------------------------------------------------

class CostCalculator:
    """Abstract base class for all cost calculation strategies."""
    def __init__(self):
        self.name = self.__class__.__name__
        self.history = []

    def calculate(self, hfss):
        """Calculates the cost. Must be implemented by subclasses."""
        raise NotImplementedError

    def normalize(self, cost):
        """Normalizes the cost based on its history."""
        if not self.history:
            return cost
        max_cost = max(self.history) if self.history else 1.0
        return cost / max_cost if max_cost > 0 else cost

class SParameterCost(CostCalculator):
    """Calculates cost based on S-parameter violations over a frequency range."""
    def __init__(self, expression, targets, freq_range):
        super().__init__()
        self.expression = expression
        self.targets = targets
        self.freq_range = freq_range

    def calculate(self, hfss):
        print(f"  - INFO ({self.name}): Retrieving S-parameter data for expression '{self.expression}'...")
        solution_data = hfss.post.get_solution_data(self.expression)

        if not solution_data or not hasattr(solution_data, 'primary_sweep_values'):
            print(f"  - WARNING ({self.name}): Invalid solution data provided.")
            return 100.0

        s_db = np.array(solution_data.data_real())
        freq_unit = solution_data.units_sweeps.get('Freq', 'GHz')
        
        conversion_factors = {'GHz': 1.0, 'MHz': 1e-3, 'kHz': 1e-6, 'Hz': 1e-9}
        conversion_to_ghz = conversion_factors.get(freq_unit)
        if conversion_to_ghz is None:
            raise ValueError(f"Unknown frequency unit '{freq_unit}' encountered.")

        freq_ghz = np.array(solution_data.primary_sweep_values) * conversion_to_ghz
        
        mask = (freq_ghz >= self.freq_range[0]) & (freq_ghz <= self.freq_range[1])
        s_db_filtered = s_db[mask]
        freq_ghz_filtered = freq_ghz[mask]

        if len(s_db_filtered) == 0:
            print(f"  - WARNING ({self.name}): No data points in the specified frequency range.")
            return 100.0

        target_db_array = np.zeros_like(freq_ghz_filtered)
        last_freq_limit = 0.0
        for freq_limit, target_db in self.targets:
            segment_mask = (freq_ghz_filtered > last_freq_limit) & (freq_ghz_filtered <= freq_limit)
            target_db_array[segment_mask] = target_db
            last_freq_limit = freq_limit
            
        violations = np.maximum(0, s_db_filtered - target_db_array)
        cost = np.sum(violations)
        self.history.append(cost)
        return cost

class TDRCost(CostCalculator):
    """Calculates cost based on TDR impedance deviation and flatness."""
    def __init__(self, expression, target_impedance, time_range, weight_proximity=1.0, weight_flatness=1.0):
        super().__init__()
        self.expression = expression
        self.target_impedance = target_impedance
        self.time_range = time_range
        self.w_proximity = weight_proximity
        self.w_flatness = weight_flatness
        self.name = f"TDRCost_w_prox_{self.w_proximity}_w_flat_{self.w_flatness}"
        self.report_name = f"_gemini_tdr_report_{self.expression}" # Unique name for the dynamic report

    def calculate(self, hfss):
        """Dynamically creates a TDR report, extracts data, and calculates cost."""
        try:
            print(f"  - INFO ({self.name}): Dynamically creating TDR report for '{self.expression}'...")
            
            # --- Step 1: Dynamically create the TDR report ---
            report = hfss.post.create_report(
                expressions=self.expression,
                domain="Time",
                primary_sweep="Time",
            )
            # --- Step 2: Get data from the newly created report ---
            tdr_data = report.get_solution_data()

            if not tdr_data or not hasattr(tdr_data, 'primary_sweep_values'):
                print(f"  - ERROR ({self.name}): Failed to retrieve TDR data from dynamically created report.")
                return 1000.0

            # --- Step 3: Process data and calculate cost (as before) ---
            time_ns = np.array(tdr_data.primary_sweep_values)
            impedance_z = np.array(tdr_data.data_real())

            mask = (time_ns >= self.time_range[0]) & (time_ns <= self.time_range[1])
            z_filtered = impedance_z[mask]

            if len(z_filtered) < 2:
                print(f"  - WARNING ({self.name}): Less than 2 data points in the specified time range.")
                return 1000.0

            cost_proximity = np.mean((z_filtered - self.target_impedance)**2)
            dz = z_filtered[1:] - z_filtered[:-1]
            cost_flatness = np.mean(dz**2)
            total_cost = (self.w_proximity * cost_proximity) + (self.w_flatness * cost_flatness)
            
            print(f"    - Proximity Cost (MSE): {cost_proximity:.4f}")
            print(f"    - Flatness Cost (MSD): {cost_flatness:.4f}")
            
            self.history.append(total_cost)
            return total_cost

        except Exception as e:
            print(f"  - ERROR ({self.name}): An exception occurred during TDR cost calculation: {e}")
            traceback.print_exc()
            return 1000.0
        finally:
            # --- Step 4: Clean up by deleting the dynamic report ---
            try:
                hfss.post.delete_report(self.report_name)
                print(f"  - INFO ({self.name}): Successfully deleted dynamic report '{self.report_name}'.")
            except Exception as e:
                print(f"  - WARNING ({self.name}): Could not delete dynamic report '{self.report_name}'. It may remain in the project.")

# --- New Cost Objectives Configuration ---
COST_OBJECTIVES = [
    {
        'strategy': SParameterCost(
            expression="dB(St(Diff1,Diff1))",
            targets=[(28.0, -20.0), (56.0, -15.0)],
            freq_range=(0.0, 56.0)
        ),
        'weight': 1.0
    },
    # Uncomment the block below to enable TDR optimization
    # {
    #     'strategy': TDRCost(
    #         expression="TDRZt(Diff1)",
    #         target_impedance=85, 
    #         time_range=(0.1, 0.5), # Unit: ns
    #         weight_proximity=1.0,  # TDR internal weight: Proximity to target
    #         weight_flatness=0.8    # TDR internal weight: Flatness
    #     ),
    #     'weight': 1.0 # Weight of the TDR objective in the total cost
    # }
]

# -----------------------------------------------------------------------------
# 3. DEFINE INITIAL PARAMETER SPACE
# -----------------------------------------------------------------------------
INITIAL_PARAM_SPACE = [
    Real(0.15, 0.22, name='Via_1_3_pitch'),
    Real(0.18, 0.25, name='Via_1_3_antipad_diameter'),
    Real(0.20, 0.28, name='Via_3_5_pitch'),
    Real(0.22, 0.30, name='Via_3_5_antipad_diameter'),
    Real(0.35, 0.45, name='Via_5_6_pitch'),
    Real(0.32, 0.40, name='Via_5_6_antipad_diameter'),
    Real(0.21, 0.29, name='Via_6_8_pitch'),
    Real(0.22, 0.30, name='Via_6_8_antipad_diameter'),
    Real(0.20, 0.28, name='Via_8_10_pitch'),
    Real(0.22, 0.30, name='Via_8_10_antipad_diameter'),
    Real(0.45, 0.65, name='Ball_antipad_diameter'),
    # --- Added Trace Parameters ---
    Real(0.04, 0.08, name='Cu8_trace_gap'),
    Real(0.02, 0.035, name='Cu8_trace_width'),
    Real(0.04, 0.08, name='Cu1_trace_gap'),
    Real(0.02, 0.035, name='Cu1_trace_width')
]
# Keep a copy of the absolute bounds for clamping
ABSOLUTE_BOUNDS = {p.name: (p.low, p.high) for p in INITIAL_PARAM_SPACE}
PARAM_NAMES = [p.name for p in INITIAL_PARAM_SPACE]

# Global HFSS object
hfss = None

# -----------------------------------------------------------------------------
# 4. OBJECTIVE FUNCTION
# -----------------------------------------------------------------------------
@use_named_args(INITIAL_PARAM_SPACE)
def evaluate_hfss(**params):
    global hfss, EVALUATION_COUNT, CONSECUTIVE_ZERO_COST_COUNT
    EVALUATION_COUNT += 1
    print("\n" + "="*60)
    print(f"Evaluation #{EVALUATION_COUNT}")
    print(f"Evaluating parameters:")
    try:
        for name, value in params.items():
            hfss[name] = f"{value}mm"
            print(f"  - Setting {name} = {value:.4f}mm")
        
        print("  - Running HFSS analysis...")
        hfss.analyze_setup(name = SETUP_NAME,cores=64,tasks=1)
        print("  - Analysis complete.")
        
        total_cost = 0.0
        individual_costs = {}

        print("  - Calculating costs from objectives:")
        for obj in COST_OBJECTIVES:
            strategy = obj['strategy']
            weight = obj['weight']
            
            raw_cost = strategy.calculate(hfss)
            individual_costs[strategy.name] = raw_cost
            print(f"    - Strategy: {strategy.name}, Raw Cost: {raw_cost:.4f}")

            normalized_cost = strategy.normalize(raw_cost)
            weighted_cost = normalized_cost * weight
            total_cost += weighted_cost
            print(f"    - Normalized Cost: {normalized_cost:.4f}, Weighted Cost: {weighted_cost:.4f}")

        print(f"  - Cost (Total Weighted): {total_cost:.4f}")

        if total_cost == 0:
            CONSECUTIVE_ZERO_COST_COUNT += 1
            print(f"  - Zero cost achieved. Consecutive count: {CONSECUTIVE_ZERO_COST_COUNT}")
        else:
            CONSECUTIVE_ZERO_COST_COUNT = 0

        # --- Log the results ---
        generation = (EVALUATION_COUNT - 1) // GENERATION_SIZE + 1
        iteration_in_gen = (EVALUATION_COUNT - 1) % GENERATION_SIZE + 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        cost_values_to_log = [f"{total_cost:.6f}"]
        cost_values_to_log.extend([f"{individual_costs.get(obj['strategy'].name, 0):.6f}" for obj in COST_OBJECTIVES])

        param_values = [f"{params[name]:.6f}" for name in PARAM_NAMES]
        log_data = [timestamp, str(generation), str(iteration_in_gen), str(EVALUATION_COUNT)] + cost_values_to_log + param_values
        
        logger.info(','.join(log_data))

        print("="*60)
        return total_cost
    except Exception as e:
        print(f"  - An exception occurred during HFSS evaluation: {e}")
        traceback.print_exc()
        return 100.0



# -----------------------------------------------------------------------------
# 5. UTILITY FUNCTIONS
# -----------------------------------------------------------------------------

def setup_logging():
    """Sets up a CSV logger to record optimization progress."""
    log_filename = 'optimization_log.csv'
    file_exists = os.path.exists(log_filename)
    
    handler = logging.FileHandler(log_filename)
    logger = logging.getLogger('OptimizationLogger')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(handler)

    if not file_exists:
        cost_headers = ['Total_Cost']
        for obj in COST_OBJECTIVES:
            cost_headers.append(f"Cost_{obj['strategy'].name}")
        
        header = ['Timestamp', 'Generation', 'Iteration_in_Gen', 'Total_Iteration'] + cost_headers + PARAM_NAMES
        logger.info(','.join(header))
    
    return logger


# -----------------------------------------------------------------------------
# 5. MAIN EXECUTION BLOCK
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Setup logger first
    logger = setup_logging()

    # First, check for and remove any stale lock files
    check_and_remove_lock_file(PROJECT_PATH)

    

    with Desktop(new_desktop=False, non_graphical=True) as d:
        try:
            hfss = Hfss(project=PROJECT_PATH, design=DESIGN_NAME, new_desktop=False)
            print("Successfully connected to HFSS design.")

            num_generations = TOTAL_ITERATIONS // GENERATION_SIZE
            current_param_space = copy.deepcopy(INITIAL_PARAM_SPACE)
            all_x_iters, all_y_vals = [], []

            for gen in range(num_generations):
                print(f"\n--- Starting Generation {gen + 1}/{num_generations} ---")
                
                # --- Filter historical points to only include those within the new space ---
                valid_x0 = []
                valid_y0 = []
                if all_x_iters:
                    print(f"\nFiltering {len(all_x_iters)} historical points for the new space...")
                    for i, x_point in enumerate(all_x_iters):
                        is_valid = all(dim.low <= x_point[j] <= dim.high for j, dim in enumerate(current_param_space))
                        if is_valid:
                            valid_x0.append(x_point)
                            valid_y0.append(all_y_vals[i])
                    print(f"Found {len(valid_x0)} valid historical points to carry over.")

                result = gp_minimize(
                    func=evaluate_hfss,
                    dimensions=current_param_space,
                    n_calls=GENERATION_SIZE,
                    n_initial_points=max(1, GENERATION_SIZE // 4),
                    x0=valid_x0 if valid_x0 else None,
                    y0=valid_y0 if valid_y0 else None
                )
                
                all_x_iters.extend(result.x_iters)
                all_y_vals.extend(result.func_vals)

                # --- Check for early stopping ---
                if STOP_AFTER_N_CONSECUTIVE_ZEROS > 0 and CONSECUTIVE_ZERO_COST_COUNT >= STOP_AFTER_N_CONSECUTIVE_ZEROS:
                    print(f"\n!!! Stopping early: Achieved {CONSECUTIVE_ZERO_COST_COUNT} consecutive zero-cost results. !!!\n")
                    break # Exit the main generation loop
                
                
                
                if ENABLE_ADAPTIVE_SPACE:
                    # --- After each generation, adapt the parameter space ---
                    # 1. Create a DataFrame for easier analysis
                    param_dict = {name: [x[i] for x in result.x_iters] for i, name in enumerate(PARAM_NAMES)}
                    param_dict['Total_Cost'] = result.func_vals
                    df = pd.DataFrame(param_dict)

                    # 2. Analyze results and compute new space
                    elite_df = df.nsmallest(int(len(df) * ELITE_FRACTION), 'Total_Cost')
                    best_params_this_gen = result.x

                    new_space = []
                    print("\n--- Adjusting Parameter Space for Next Generation ---")
                    for j, param in enumerate(current_param_space):
                        # 2a. Default Shrinking Logic
                        mean = elite_df[param.name].mean()
                        std_dev = elite_df[param.name].std()
                        low = mean - SPACE_SHRINK_FACTOR * std_dev
                        high = mean + SPACE_SHRINK_FACTOR * std_dev

                        # 2b. Boundary Expansion Logic
                        boundary_edge = (param.high - param.low) * BOUNDARY_EDGE_FRACTION
                        upper_pressure_points = elite_df[elite_df[param.name] >= param.high - boundary_edge]
                        lower_pressure_points = elite_df[elite_df[param.name] <= param.low + boundary_edge]

                        if len(upper_pressure_points) / len(elite_df) > BOUNDARY_PRESSURE_THRESHOLD:
                            expand_amount = (param.high - param.low) * BOUNDARY_EXPANSION_FACTOR
                            high += expand_amount
                            print(f"  - Expanding upper bound for {param.name} to {high:.4f} (pressure detected)")

                        if len(lower_pressure_points) / len(elite_df) > BOUNDARY_PRESSURE_THRESHOLD:
                            expand_amount = (param.high - param.low) * BOUNDARY_EXPANSION_FACTOR
                            low -= expand_amount
                            print(f"  - Expanding lower bound for {param.name} to {low:.4f} (pressure detected)")

                        # 2c. Finalization and Safety Checks
                        best_param_val = best_params_this_gen[j]
                        low = min(low, best_param_val)
                        high = max(high, best_param_val)

                        abs_low, abs_high = ABSOLUTE_BOUNDS[param.name]
                        low = max(abs_low, low)
                        high = min(abs_high, high)

                        if low >= high:
                            low, high = abs_low, abs_high

                        new_space.append(Real(low, high, name=param.name))
                        if param.low != new_space[-1].low or param.high != new_space[-1].high:
                            print(f"  - New range for {param.name}: ({new_space[-1].low:.4f}, {new_space[-1].high:.4f})")
                    
                    current_param_space = new_space

            # --- Final Results ---
            print("\n" + "*"*60)
            print("Adaptive Optimization Finished!")
            best_cost_index = np.argmin(all_y_vals)
            best_cost = all_y_vals[best_cost_index]
            best_params_list = all_x_iters[best_cost_index]
            
            print(f"Best Cost Found: {best_cost:.4f}")
            print("Best Parameters:")
            for i, dim in enumerate(INITIAL_PARAM_SPACE):
                print(f"  - {dim.name}: {best_params_list[i]:.4f}mm")
            print("*"*60)

            

        except Exception as e:
            print(f"A critical error occurred: {e}")
            traceback.print_exc()
        finally:
            print("Script finished.")
