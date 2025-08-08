
### Prerequisites
```bash
pip install pyaedt
# Ensure Ansys Electronics Desktop (AEDT) 2023.2+ is installed
```

### Running the Model Generation
```bash
# Run the main script to generate the HFSS model
python create_fcbga_model.py
```

### Development
- Modify `fcbga_parameters.xml` to change the model's physical properties.
- The main logic is contained in `create_fcbga_model.py`.
- There are no automated tests; verification is done by inspecting the generated model in HFSS.
