# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Ansys HFSS automation project** using Python and `pyaedt` library to create fully parameterized 10-layer FCBGA (Flip-Chip Ball Grid Array) differential signal models. The project reads configuration from XML files and generates complete HFSS models with signal paths, GND planes, anti-pads, and precise port setups.

## Core Architecture

### Main Components
- **FcbgaModeler class** (`create_fcbga_model.py`): Orchestrates entire model creation workflow
- **XML Configuration** (`fcbga_parameters.xml`): Defines all geometric and material parameters
- **HFSS Scripts**: `hfss_setup.py`, `create_port*.py` for analysis setup

### Key Workflow
1. **Initialization**: `setup_aedt()` starts AEDT session
2. **Parameter Loading**: `define_variables_and_materials()` parses XML into HFSS variables
3. **Geometry Creation**: Sequential creation of signal paths, vias, planes
4. **Boolean Operations**: GND plane subtraction with anti-pads
5. **Port Creation**: Custom terminal ports using COM interface for differential pairs

## Development Commands

### Prerequisites
```bash
pip install pyaedt
# Ensure Ansys Electronics Desktop (AEDT) 2023.2+ is installed
```

### Running Models
```bash
# Basic execution
python create_fcbga_model.py

# Custom configuration
python create_fcbga_model.py --xml custom_config.xml --version 2025.2
```

### Testing & Validation
- Visual inspection in HFSS 3D Modeler
- Parameter sweep testing via XML modification
- Port impedance verification
- Layer stackup consistency checks

## Critical Patterns & Best Practices

### 1. Naming Conventions
- **HFSS Entities**: Use only letters, numbers, underscores (`_`)
- **Forbidden**: hyphens (`-`), spaces, special characters
- **Sanitize**: Always clean external names (XML/CSV) before HFSS use

### 2. Parameter Management
- **XML → Python → HFSS Variables**: Clear parameter pipeline
- **Units**: Always include units in HFSS expressions (mm, GHz)
- **Validation**: Check variable expressions before creation

### 3. Geometry Calculation Strategy
- **Sequential Python Calculation**: Perform complex logic in Python
- **Avoid Complex HFSS Expressions**: Prevent solver circular dependencies
- **Fixed Values**: Pass final coordinates as strings (e.g., `"1.234mm"`)

### 4. Dynamic Layout Generation
- **XML Configuration**: Use `<layouts><layout type="outer">...</layout></layouts>`
- **Selector Parameter**: Add `layout_type` parameter to main class
- **Conditional Logic**: Use Python `if/elif` based on XML type attribute

### 5. Port Creation Challenges
- **Limitation**: `pyaedt` lacks native differential terminal port support
- **Solution**: Direct COM interface via `AutoIdentifyPorts`
- **Reference Conductors**: Dynamic selection based on port layer position

## File Structure

```
Ansys_ViaOPT/
├── create_fcbga_model.py      # Main orchestration class
├── fcbga_parameters.xml       # Configuration parameters
├── FCBGA_From_XML_v2.aedt     # Generated HFSS project
├── hfss_setup.py             # Analysis setup script
├── create_port_*.py          # Port creation utilities
└── *.aedt                    # Generated model files
```

## Common Development Tasks

### Adding New Layers
1. Update `fcbga_parameters.xml` with layer definitions
2. Add corresponding via styles if needed
3. Update routing rules for new layer
4. Test parameter regeneration

### Custom Ball Patterns
1. Add new `<ball_map>` type in XML
2. Update geometry calculations in `create_signal_and_gnd_paths()`
3. Modify GND ball coordinate generation

### Extending Port Types
1. Extend `_create_terminal_port()` method
2. Add new reference conductor selection logic
3. Update impedance calculations as needed

## Error Handling & Troubleshooting

### AEDT Connection Issues
- Verify license availability
- Check version compatibility (pyaedt ↔ AEDT)
- Ensure proper environment variables

### XML Parsing Errors
- Validate XML syntax with online tools
- Check required attributes in each section
- Verify unit consistency

### Geometry Creation Failures
- Validate HFSS variable expressions
- Check layer naming consistency
- Ensure material properties are defined

## Performance Considerations

- **Model Complexity**: 10-layer FCBGA generates large models
- **Parameter Sweep**: Use XML modification for batch runs
- **Memory**: Monitor RAM usage during complex geometries
- **Save Frequency**: Periodic saves during long operations