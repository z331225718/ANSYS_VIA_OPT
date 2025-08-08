
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


OPTIMIZATION_MODE = 'single_point'  # Options: 'single_point' or 'wideband'

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

# --- Performance Goal ---
# For single_point mode: The target S11 value at the target frequency.
TARGET_S11_DB_SINGLE_POINT = -15.0 

# For wideband mode: A list of (frequency_limit, target_db) pairs.
# Defines a piecewise target. The list must be sorted by frequency.
# Example: [(28.0, -20.0), (56.0, -15.0)] means:
# - Freq <= 28.0 GHz, target is -20.0 dB
# - 28.0 < Freq <= 56.0 GHz, target is -15.0 dB
WIDEBAND_TARGETS = [
    (28.0, -20.0),
    (56.0, -15.0)
]
# Target frequency in GHz for single-point optimization.
TARGET_FREQ_GHZ = 56.0
# Frequency range in GHz for wideband optimization.
WIDEBAND_FREQ_START_GHZ = 0.0
WIDEBAND_FREQ_END_GHZ = 56.0

# -----------------------------------------------------------------------------
# 2. DEFINE INITIAL PARAMETER SPACE
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
    Real(0.45, 0.65, name='BGA_antipad_diameter'),
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
# 3. OBJECTIVE FUNCTION (No changes needed here)
# -----------------------------------------------------------------------------
@use_named_args(INITIAL_PARAM_SPACE)
def evaluate_hfss(**params):
    global hfss
    print("\n" + "="*60)
    print(f"Evaluating parameters:")
    try:
        for name, value in params.items():
            hfss[name] = f"{value}mm"
            print(f"  - Setting {name} = {value:.4f}mm")
        print("  - Running HFSS analysis...")
        hfss.analyze_setup(SETUP_NAME)
        print("  - Analysis complete.")
        print("  - Retrieving S-parameter data...")
        solution_data = hfss.post.get_solution_data("dB(St(Diff1,Diff1))")
        if not solution_data or not hasattr(solution_data, 'primary_sweep_values'):
            print("  - ERROR: Failed to retrieve valid solution data.")
            return 100.0
        s11_db = np.array(solution_data.data_real())
        
        # --- Robust Unit Handling ---
        # Programmatically determine the frequency unit from the solution data
        freq_unit = solution_data.units_sweeps['Freq']
        
        # Calculate the conversion factor to bring the frequency to GHz
        if freq_unit == 'GHz':
            conversion_to_ghz = 1.0
        elif freq_unit == 'MHz':
            conversion_to_ghz = 1e-3
        elif freq_unit == 'kHz':
            conversion_to_ghz = 1e-6
        elif freq_unit == 'Hz':
            conversion_to_ghz = 1e-9
        else:
            raise ValueError(f"Unknown frequency unit '{freq_unit}' encountered.")
            
        # Apply the conversion factor to get a reliable frequency array in GHz
        freq_ghz = np.array(solution_data.primary_sweep_values) * conversion_to_ghz

        # --- The Cost Calculation (Mode-dependent) ---
        segmented_costs = []
        if OPTIMIZATION_MODE == 'wideband':
            mask = (freq_ghz >= WIDEBAND_FREQ_START_GHZ) & (freq_ghz <= WIDEBAND_FREQ_END_GHZ)
            s11_db_filtered = s11_db[mask]
            freq_ghz_filtered = freq_ghz[mask]

            if len(s11_db_filtered) == 0:
                print(f"  - WARNING: No data points in the specified wideband range.")
                return 100.0
            
            # --- Build the piecewise target array and calculate segmented costs ---
            target_db_array = np.zeros_like(freq_ghz_filtered)
            total_violations = np.zeros_like(freq_ghz_filtered)
            last_freq_limit = 0.0
            
            for freq_limit, target_db in WIDEBAND_TARGETS:
                segment_mask = (freq_ghz_filtered > last_freq_limit) & (freq_ghz_filtered <= freq_limit)
                target_db_array[segment_mask] = target_db
                
                # Calculate violations for this specific segment
                segment_s11 = s11_db_filtered[segment_mask]
                segment_target = target_db_array[segment_mask]
                segment_violations = np.maximum(0, segment_s11 - segment_target)
                segmented_costs.append(np.sum(segment_violations))
                
                last_freq_limit = freq_limit

            # Total cost is the sum of all violations across all segments
            violations = np.maximum(0, s11_db_filtered - target_db_array)
            cost = np.sum(violations)
            print(f"  - Cost (Total Integrated Area): {cost:.4f}")

        elif OPTIMIZATION_MODE == 'single_point':
            target_freq_index = (np.abs(freq_ghz - TARGET_FREQ_GHZ)).argmin()
            value_to_evaluate = s11_db[target_freq_index]
            actual_freq_ghz = freq_ghz[target_freq_index]
            print(f"  - S(Diff1,Diff1) at {actual_freq_ghz:.2f} GHz: {value_to_evaluate:.4f} dB")
            cost = max(0, value_to_evaluate - TARGET_S11_DB_SINGLE_POINT)
            print(f"  - Cost (Deviation from {TARGET_S11_DB_SINGLE_POINT}dB): {cost:.4f}")
        
        else:
            raise ValueError(f"Unknown OPTIMIZATION_MODE: {OPTIMIZATION_MODE}")

        # --- Update counters for logging and early stopping ---
        global EVALUATION_COUNT, CONSECUTIVE_ZERO_COST_COUNT
        EVALUATION_COUNT += 1
        
        if cost == 0:
            CONSECUTIVE_ZERO_COST_COUNT += 1
            print(f"  - Zero cost achieved. Consecutive count: {CONSECUTIVE_ZERO_COST_COUNT}")
        else:
            CONSECUTIVE_ZERO_COST_COUNT = 0 # Reset counter if the cost is not zero

        # --- Log the results, including segmented costs ---
        generation = (EVALUATION_COUNT - 1) // GENERATION_SIZE + 1
        iteration_in_gen = (EVALUATION_COUNT - 1) % GENERATION_SIZE + 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        cost_values_to_log = [f"{cost:.6f}"]
        if OPTIMIZATION_MODE == 'wideband':
            cost_values_to_log.extend([f"{sc:.6f}" for sc in segmented_costs])

        param_values = [f"{params[name]:.6f}" for name in PARAM_NAMES]
        log_data = [timestamp, str(generation), str(iteration_in_gen), str(EVALUATION_COUNT)] + cost_values_to_log + param_values
        
        logger.info(','.join(log_data))

        print("="*60)
        return cost
    except Exception as e:
        print(f"  - An exception occurred during HFSS evaluation: {e}")
        traceback.print_exc()
        return 100.0

# -----------------------------------------------------------------------------
# 4. ADAPTIVE SPACE & PLOTTING FUNCTIONS
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
        # Dynamically create headers for segmented costs
        cost_headers = ['Cost'] # Start with the total cost
        if OPTIMIZATION_MODE == 'wideband':
            last_freq = 0.0
            for freq_limit, _ in WIDEBAND_TARGETS:
                cost_headers.append(f"Cost_{last_freq:.1f}-{freq_limit:.1f}GHz")
                last_freq = freq_limit

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
                    param_dict['Cost'] = result.func_vals
                    df = pd.DataFrame(param_dict)

                    # 2. Analyze results and compute new space
                    elite_df = df.nsmallest(int(len(df) * ELITE_FRACTION), 'Cost')
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
