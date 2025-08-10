import pandas as pd
from pathlib import Path
import shutil
from ansys.aedt.core import Hfss
import sys

# --- CONFIGURATION ---
# The CSV file containing the optimization log data
LOG_FILE = Path("optimization_log.csv")
# The base AEDT project file to be used as a template
BASE_PROJECT_FILE = Path("FCBGA_From_XML_v2.aedt")
# The directory to save the new optimized project files
OUTPUT_DIRECTORY = Path("Optimized_AEDT_Projects")
# Ansys Electronics Desktop version
AEDT_VERSION = "2023.2" # Or your specific version

def apply_best_parameters():
    """
    Reads an optimization log, finds the best parameter set for each cost function,
    and creates a new AEDT project for each of these sets.
    """
    # 1. Load Data and Prepare Environment
    if not LOG_FILE.exists():
        print(f"错误: 未找到日志文件 '{LOG_FILE}'", file=sys.stderr)
        return
    
    if not BASE_PROJECT_FILE.exists():
        print(f"错误: 未找到基础项目文件 '{BASE_PROJECT_FILE}'", file=sys.stderr)
        return

    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    print(f"--- 新的优化项目将保存在: {OUTPUT_DIRECTORY.resolve()} ---")

    print(f"--- 正在从 '{LOG_FILE}' 加载数据 ---")
    df = pd.read_csv(LOG_FILE)

    # 2. Identify parameter and cost columns
    all_columns = df.columns.tolist()
    cost_columns = [col for col in all_columns if col.startswith('Cost')]
    if not cost_columns:
        print("错误: 日志中未找到任何'Cost'列", file=sys.stderr)
        return
        
    last_cost_col_index = all_columns.index(cost_columns[-1])
    param_names = all_columns[last_cost_col_index + 1:]
    
    print(f"找到 {len(cost_columns)} 个成本列进行处理: {cost_columns}")
    print(f"找到 {len(param_names)} 个设计参数.")

    # 3. Launch AEDT
    print(f"--- 正在启动 Ansys Electronics Desktop {AEDT_VERSION} ---")
    # This launches AEDT. new_desktop_session=True ensures it's a new instance.
    # We will reuse this instance for all operations.
    hfss = None
    try:
        hfss = Hfss(version=AEDT_VERSION, new_desktop=True)
        
        # 4. Process each cost function
        for cost in cost_columns:
            print(f"\n--- 正在处理成本项: {cost} ---")
            
            # Find all rows with the minimum value for the current cost
            min_cost_value = df[cost].min()
            tied_rows_df = df[df[cost] == min_cost_value].copy() # Use .copy() to avoid SettingWithCopyWarning

            best_row = None
            # Check if there's a tie
            if len(tied_rows_df) > 1:
                print(f"  - 发现 {len(tied_rows_df)} 个方案并列最小成本 ({min_cost_value}). 正在应用决胜局逻辑...")
                
                # Tie-breaking logic: if analyzing a component cost, use 'Cost' (total) as the tie-breaker.
                if cost != 'Cost' and 'Cost' in df.columns:
                    print("  - 使用 'Cost' (总成本) 作为决胜局标准.")
                    best_row = tied_rows_df.loc[tied_rows_df['Cost'].idxmin()]
                else:
                    # Fallback for two cases:
                    # 1. We are analyzing the 'Cost' (total) column itself and there's a tie.
                    # 2. We are analyzing a component cost, but no 'Cost' (total) column exists.
                    print("  - 使用其余成本项之和作为决胜局标准.")
                    other_costs = [c for c in cost_columns if c != cost]
                    if other_costs:
                        tied_rows_df['TieBreaker_Cost'] = tied_rows_df[other_costs].sum(axis=1)
                        best_row = tied_rows_df.loc[tied_rows_df['TieBreaker_Cost'].idxmin()]
                    else:
                        # If there are no other costs to sum, just pick the first tied result.
                        best_row = tied_rows_df.iloc[0]
            else:
                print(f"  - 找到唯一最优方案.")
                best_row = tied_rows_df.iloc[0]

            # Create a dictionary of the optimal parameters
            best_params = best_row[param_names].to_dict()
            
            print(f"  - 选定的最优成本值: {best_row[cost]}")
            if cost != 'Cost' and 'Cost' in best_row:
                 print(f"  - (决胜局) 总成本: {best_row['Cost']}")
            elif 'TieBreaker_Cost' in best_row:
                 print(f"  - (决胜局) 其余成本之和: {best_row['TieBreaker_Cost']}")

            print(f"  - 对应的参数将在新项目里被设置.")

            # Define new project path
            new_project_name = f"{BASE_PROJECT_FILE.stem}_Optimized_for_{cost}.aedt"
            new_project_path = OUTPUT_DIRECTORY / new_project_name

            # Copy the base project to the new path
            print(f"  - 复制模板项目到: {new_project_path}")
            shutil.copy(BASE_PROJECT_FILE, new_project_path)
            
            # Open the newly copied project in AEDT
            hfss.load_project(str(new_project_path.resolve()))
            
            # Set the design variables
            print("  - 正在更新HFSS中的设计变量...")
            for param_name, param_value in best_params.items():
                try:
                    # pyaedt expects variables to be strings with units
                    # Assuming all parameters are lengths and should be in 'mm'
                    # This might need adjustment if units vary
                    value_with_unit = f"{param_value}mm"
                    hfss[param_name] = value_with_unit
                    print(f"    - 设置 {param_name} = {value_with_unit}")
                except Exception as e:
                    print(f"    - 警告: 无法设置参数 '{param_name}'. 错误: {e}", file=sys.stderr)

            # Save and close the project
            print("  - 正在保存并关闭项目...")
            hfss.save_project()
            hfss.close_project(hfss.active_project.name)
            print(f"  - 成功创建项目: {new_project_path.name}")

    except Exception as e:
        print(f"\n处理过程中发生严重错误: {e}", file=sys.stderr)
        print("请确保Ansys Electronics Desktop已正确安装，并且版本与脚本中设置的匹配。", file=sys.stderr)

    finally:
        # 5. Release AEDT
        if hfss:
            print("\n--- 正在关闭 Ansys Electronics Desktop ---")
            hfss.release_desktop()
    
    print("\n--- 所有任务完成 ---")


if __name__ == "__main__":
    apply_best_parameters()
