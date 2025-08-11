# TDR 成本函数实现详解

## 核心目标

TDR（时域反射计）的优化目标是双重的：
1.  **接近目标阻抗**: 整个走线的特性阻抗应尽可能地接近一个目标值（如85欧姆）。
2.  **保持平坦**: 阻抗曲线应尽可能平滑，避免剧烈的波动和不连续。

## 数学原理：双分量加权成本

为了将这两个目标量化，我们设计了一个由两部分组成的成本函数，并将它们加权求和。

设：
*   `Z` 是在指定时间范围内的TDR阻抗值数组。
*   `Z_target` 是目标阻抗。

### 1. 接近度成本 (Proximity Cost)

我们使用**均方误差 (Mean Squared Error, MSE)** 来惩罚与目标值的偏差。这能有效且有力地 penalize 大的偏差。

`Cost_Proximity = mean( (Z - Z_target)^2 )`

### 2. 平坦度成本 (Flatness Cost)

我们使用**均方一阶导数 (Mean Squared First Derivative)** 来惩罚曲线的波动。平坦曲线的导数趋近于零。我们通过计算相邻点之差来近似导数。

1.  `dZ = Z[1:] - Z[:-1]`  (计算差分)
2.  `Cost_Flatness = mean( dZ^2 )`

### 最终TDR成本

总成本是这两个分量的加权和，权重可以在 `TDRCost` 类的构造函数中指定。

`Total_TDR_Cost = w_proximity * Cost_Proximity + w_flatness * Cost_Flatness`

## 代码实现 (`TDRCost` 类)

```python
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

    def calculate(self, hfss):
        try:
            # 1. 独立获取TDR数据
            tdr_data = hfss.post.get_solution_data(
                self.expression, # e.g., "TDRZt(Diff1)"
                setup_sweep_name=hfss.setups[0].name,
                domain="Time",
                report_category="TDR_Report" # Prerequisite
            )
            
            # ... (错误处理) ...

            time_ns = np.array(tdr_data.primary_sweep_values)
            impedance_z = np.array(tdr_data.data_real())

            # 2. 筛选数据
            mask = (time_ns >= self.time_range[0]) & (time_ns <= self.time_range[1])
            z_filtered = impedance_z[mask]

            # ... (错误处理) ...

            # 3. 计算成本分量
            cost_proximity = np.mean((z_filtered - self.target_impedance)**2)
            dz = z_filtered[1:] - z_filtered[:-1]
            cost_flatness = np.mean(dz**2)

            # 4. 加权求和
            total_cost = (self.w_proximity * cost_proximity) + (self.w_flatness * cost_flatness)
            
            self.history.append(total_cost)
            return total_cost

        except Exception as e:
            # ... (异常处理) ...
            return 1000.0
```
**重要**: 使用此策略类前，必须在HFSS项目中手动或通过脚本创建一个名为 `TDR_Report` 的报告。
