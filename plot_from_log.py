import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
import sys

# --- CONFIGURATION ---
LOG_FILE = Path("optimization_log.csv")
PLOT_INTERVAL_MS = 2000  # Update plot every 2 seconds

# --- SETUP ---
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(14, 8)) # Increased figure size for table

def animate(i):
    """
    This function is called periodically by FuncAnimation.
    It reads the log file and updates the plot.
    """
    if not LOG_FILE.exists():
        print(f"Waiting for log file: {LOG_FILE}...", file=sys.stderr)
        return

    try:
        df = pd.read_csv(LOG_FILE)
        
        # --- DYNAMICALLY FIND COST AND PARAMETER COLUMNS ---
        cost_columns = [col for col in df.columns if col.startswith('Cost')]
        if not cost_columns: return
        
        # This logic assumes parameters start right after the last cost column
        last_cost_column_index = df.columns.get_loc(cost_columns[-1])
        param_names = df.columns[last_cost_column_index + 1:].tolist()
        
        if 'Total_Iteration' not in df.columns or not param_names:
            print("Log file is not yet fully formed.", file=sys.stderr)
            return

        # --- FIND THE BEST POINT BASED ON TOTAL COST (first occurrence in case of a tie) ---
        best_cost_info = None
        # Robustly use the first found cost column as the primary one for finding the best point.
        # This aligns with the convention that the first cost column is the total/main cost.
        if cost_columns and cost_columns[0] in df.columns and not df[cost_columns[0]].empty:
            primary_cost_col = cost_columns[0]
            min_cost_value = df[primary_cost_col].min()
            # Explicitly find the first index matching the minimum value
            best_idx = df[df[primary_cost_col] == min_cost_value].index[0]
            best_row = df.loc[best_idx]
            best_cost_info = {
                'iter': best_row['Total_Iteration'],
                'cost': best_row[primary_cost_col],
                'params': best_row[param_names]
            }

        ax.clear()
        
        # --- PLOT EACH COST COLUMN ---
        primary_cost_col = cost_columns[0] if cost_columns else None
        for cost_col in cost_columns:
            is_primary = (cost_col == primary_cost_col)
            marker = 'o' if is_primary else None
            linestyle = '-' if is_primary else '--'
            linewidth = 2.5 if is_primary else 1.5
            ax.plot(df['Total_Iteration'], df[cost_col], label=cost_col, marker=marker, 
                    linestyle=linestyle, linewidth=linewidth, markersize=4, alpha=0.8)

        # --- HIGHLIGHT BEST POINT AND DISPLAY PARAMETER TABLE ---
        if best_cost_info:
            # 1. Highlight the best point on the main 'Cost' curve
            ax.scatter(best_cost_info['iter'], best_cost_info['cost'], 
                       color='red', s=150, zorder=10, marker='*', 
                       label=f"Best Cost: {best_cost_info['cost']:.4f}")

            # 2. Display the table of best parameters
            table_data = [[param, f"{value:.4f}"] for param, value in best_cost_info['params'].items()]
            col_labels = ['Best Parameter', 'Value']
            table = ax.table(cellText=table_data, colLabels=col_labels, loc='lower right', 
                             cellLoc='center', colWidths=[0.2, 0.15])
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1, 1.5)

        # --- FORMATTING ---
        ax.set_xlabel("Total Iteration")
        ax.set_ylabel("Cost Value")
        ax.set_title("Live Optimization Progress")
        # Adjust legend location to avoid overlapping with the table
        ax.legend(loc='upper left')
        ax.grid(True)
        fig.tight_layout(pad=1.5)

    except pd.errors.EmptyDataError:
        print("Log file is empty, waiting for data...", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred while plotting: {e}", file=sys.stderr)

def main():
    print("--- Starting Live Plotter ---")
    print(f"Monitoring log file: {LOG_FILE.resolve()}")
    print("Close the plot window to stop the script.")
    
    # The FuncAnimation object must be assigned to a variable to keep it alive.
    ani = FuncAnimation(fig, animate, interval=PLOT_INTERVAL_MS, cache_frame_data=False)
    
    plt.show()
    
    print("--- Plotter stopped. ---")

if __name__ == "__main__":
    main()