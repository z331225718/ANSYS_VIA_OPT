import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import io
import base64

# --- CONFIGURATION ---
LOG_FILE = Path("optimization_log.csv")
REPORT_FILE = Path("analysis_report_zh_segmented.html")

def plot_to_base64(plt_figure):
    """Converts a matplotlib figure to a base64 encoded string for HTML embedding."""
    buf = io.BytesIO()
    plt_figure.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    buf.seek(0)
    base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(plt_figure)
    return base64_str

def df_to_html(df, title):
    """Converts a pandas DataFrame to a styled HTML table."""
    html = f"<h4>{title}</h4>"
    # Add index=False to hide the DataFrame index in the HTML table
    html += df.to_html(classes='styled-table', border=0, index=False)
    return html

def create_html_report(report_sections, cost_columns):
    """Generates the final self-contained HTML report from a list of sections."""
    
    # Create navigation links
    nav_links = "<h2>目录</h2><ul>"
    # Add a link for the convergence plot
    nav_links += '<li><a href="#convergence_plot">成本收敛过程</a></li>'
    for cost_name in cost_columns:
        # Sanitize cost_name for use in HTML id
        anchor_id = cost_name.replace(" ", "_").replace("(", "").replace(")", "")
        nav_links += f'<li><a href="#{anchor_id}">对 "{cost_name}" 的分析</a></li>'
    # Add a link for parameter distributions
    nav_links += '<li><a href="#parameter_distributions">参数分布图</a></li>'
    nav_links += "</ul>"

    body_content = nav_links + "".join(report_sections)
    
    html_content = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>优化过程数据分析报告 (增强版)</title>
        <style>
            body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 25px; background-color: #f4f4f9; scroll-behavior: smooth; }}
            h1, h2, h3, h4 {{ color: #2c3e50; }}
            h1 {{ text-align: center; border-bottom: 3px solid #34495e; padding-bottom: 10px;}}
            h2 {{ border-bottom: 2px solid #7f8c8d; padding-bottom: 8px; margin-top: 40px; }}
            h3 {{ border-bottom: 1px dashed #bdc3c7; padding-bottom: 6px; margin-top: 30px; }}
            p {{ color: #34495e; line-height: 1.6; }}
            ul {{ list-style-type: square; background: #ffffff; padding: 15px 30px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            li a {{ color: #2980b9; text-decoration: none; font-size: 1.1em; }}
            li a:hover {{ text-decoration: underline; color: #3498db; }}
            .styled-table {{ border-collapse: collapse; margin: 25px 0; font-size: 0.9em; width: 100%; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); }}
            .styled-table thead tr {{ background-color: #34495e; color: #ffffff; text-align: center; }}
            .styled-table th, .styled-table td {{ padding: 12px 15px; text-align: center; border-right: 1px solid #dddddd;}}
            .styled-table th:last-child, .styled-table td:last-child {{ border-right: none; }}
            .styled-table tbody tr {{ border-bottom: 1px solid #dddddd; }}
            .styled-table tbody tr:nth-of-type(even) {{ background-color: #f3f3f3; }}
            .styled-table tbody tr.best-row {{ background-color: #d4efdf; }}
            .styled-table tbody tr.worst-row {{ background-color: #f5b7b1; }}
            .styled-table tbody tr:last-of-type {{ border-bottom: 2px solid #34495e; }}
            .plot-container {{ text-align: center; margin-top: 20px; padding: 15px; background-color: #ffffff; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin-bottom: 30px;}}
            .grid-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
            img {{ max-width: 95%; height: auto; display: inline-block; }}
        </style>
    </head>
    <body>
        <h1>优化过程数据分析报告 (增强版)</h1>
        {body_content}
    </body>
    </html>
    '''
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

def plot_convergence(df, cost_columns):
    """Plots the convergence of cost functions over iterations."""
    print("  - Plotting cost convergence...")
    fig, ax = plt.subplots(figsize=(14, 8))
    for cost in cost_columns:
        ax.plot(df['Total_Iteration'], df[cost], label=cost, alpha=0.8)
    ax.set_xlabel('迭代总次数 (Total_Iteration)')
    ax.set_ylabel('成本函数值 (Cost)')
    ax.set_title('成本函数收敛过程', fontsize=18, pad=12)
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plot_b64 = plot_to_base64(fig)
    html = f'<div id="convergence_plot" class="plot-container"><h2>成本收敛过程</h2><img src="data:image/png;base64,{plot_b64}" alt="成本收敛图"></div>'
    return html

def plot_parameter_distributions(df, param_names):
    """Plots the distribution of each parameter."""
    print("  - Plotting parameter distributions...")
    html = '<div id="parameter_distributions"><h2>参数分布图</h2><div class="grid-container">'
    for param in param_names:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(df[param], kde=True, ax=ax)
        ax.set_title(f'参数 "{param}" 的分布', fontsize=14)
        ax.set_xlabel('参数值')
        ax.set_ylabel('频数')
        plot_b64 = plot_to_base64(fig)
        html += f'<div class="plot-container"><h4>{param}</h4><img src="data:image/png;base64,{plot_b64}" alt="{param} distribution"></div>'
    html += '</div></div>'
    return html

def analyze_single_cost(df, cost_name, param_names):
    """Performs a full analysis for a single cost column and returns it as an HTML string."""
    print(f"  - Analyzing '{cost_name}'...")
    anchor_id = cost_name.replace(" ", "_").replace("(", "").replace(")", "")
    analysis_html = f'<div id="{anchor_id}"><h2>对 "{cost_name}" 的分析</h2>'
    
    # 1. Best and Worst 5
    best_5_df = df.nsmallest(5, cost_name)[param_names + [cost_name]].reset_index(drop=True)
    worst_5_df = df.nlargest(5, cost_name)[param_names + [cost_name]].reset_index(drop=True)
    analysis_html += df_to_html(best_5_df, f'"{cost_name}" 值最低的5组参数 (最佳方案)')
    analysis_html += df_to_html(worst_5_df, f'"{cost_name}" 值最高的5组参数 (最差方案)')

    # 2. Sensitivity
    correlations = df[[cost_name] + param_names].corr()[cost_name].sort_values(ascending=False, key=abs)
    sensitivity_df = correlations.drop(cost_name).to_frame(name='与成本的相关系数').reset_index()
    analysis_html += df_to_html(sensitivity_df, "参数敏感度排序 (相关系数绝对值)")

    # 3. Heatmap
    fig_heatmap = plt.figure(figsize=(16, 14))
    sns.heatmap(df[[cost_name] + param_names].corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG', annot_kws={"size": 8})
    plt.title(f'{cost_name} 与各参数的相关性热力图', fontdict={'fontsize':18}, pad=12)
    heatmap_b64 = plot_to_base64(fig_heatmap)
    analysis_html += f'<div class="plot-container"><h3>相关性热力图</h3><img src="data:image/png;base64,{heatmap_b64}" alt="相关性热力图"></div>'

    # 4. Scatter Plots
    scatter_plots_html = f'<h3>成本 vs. 各参数散点图</h3><div class="grid-container">'
    for param in param_names:
        fig_scatter, ax = plt.subplots(figsize=(8, 6))
        sc = ax.scatter(df[param], df[cost_name], c=df['Total_Iteration'], cmap='viridis', alpha=0.6)
        ax.set_xlabel(param); ax.set_ylabel(cost_name); ax.grid(True)
        fig_scatter.colorbar(sc, ax=ax, label='迭代次数')
        plot_html = f'<div class="plot-container"><h4>{cost_name} vs. {param}</h4><img src="data:image/png;base64,{plot_to_base64(fig_scatter)}" alt="{cost_name} vs. {param}"></div>'
        scatter_plots_html += plot_html
    analysis_html += scatter_plots_html + '</div>'
    
    analysis_html += '</div>'
    return analysis_html

def analyze_optimization_log():
    # 1. Load Data
    if not LOG_FILE.exists(): print(f"错误: 未找到日志文件 '{LOG_FILE}'", file=sys.stderr); return
    print(f"--- 正在从 '{LOG_FILE}' 加载数据 ---")
    df = pd.read_csv(LOG_FILE)
    
    # 2. Identify parameter and cost columns
    all_columns = df.columns.tolist()
    cost_columns = [col for col in all_columns if col.startswith('Cost')]
    if cost_columns:
        last_cost_col_index = all_columns.index(cost_columns[-1])
        param_names = all_columns[last_cost_col_index + 1:]
    else:
        param_names = []
    
    if not cost_columns: print("错误: 日志中未找到任何'Cost'列", file=sys.stderr); return
    print(f"找到 {len(cost_columns)} 个成本列进行分析: {cost_columns}")
    print(f"找到 {len(param_names)} 个参数进行分析: {param_names}")

    # 3. Generate report sections
    report_sections = []
    
    # Section 1: Overall Statistics
    print("--- 正在生成统计摘要 ---")
    stats_df = df[cost_columns + param_names].describe().reset_index()
    stats_html = "<h2>一、整体描述性统计分析</h2><p>此表格提供了所有成本及参数的统计摘要。</p>"
    stats_html += df_to_html(stats_df, "统计摘要")
    report_sections.append(stats_html)

    # Section 2: Convergence Plot
    print("--- 正在生成成本收敛图 ---")
    report_sections.append(plot_convergence(df, cost_columns))

    # Section 3: Loop through each cost column for detailed analysis
    print("--- 正在为每个成本维度生成深度分析 ---")
    for cost_name in cost_columns:
        report_sections.append(analyze_single_cost(df, cost_name, param_names))

    # Section 4: Parameter Distributions
    print("--- 正在生成参数分布图 ---")
    report_sections.append(plot_parameter_distributions(df, param_names))

    # 4. Create the final HTML report
    print(f"--- 正在生成HTML报告 ---")
    create_html_report(report_sections, cost_columns)
    
    print(f"\n--- 分析完成 ---")
    print(f"成功！分析报告已生成: {REPORT_FILE.resolve()}")

if __name__ == "__main__":
    try:
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False
    except Exception as e:
        print(f"无法设置中文字体: {e}", file=sys.stderr)
    analyze_optimization_log()
