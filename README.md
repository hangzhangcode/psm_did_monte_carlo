# PSM-DID 蒙特卡洛模拟分析
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

本仓库包含完成「机器学习与因果推断」课程作业1的全部代码与分析报告，通过蒙特卡洛（Monte Carlo）模拟系统研究PSM-DID、单独PSM和单独DID方法的识别逻辑、优势与局限性。

## 作业目标
1. 设计可控的数据生成过程，构造三种典型场景对比不同因果推断方法的表现
2. 量化评估各方法的偏差（Bias）、均方根误差（RMSE）等指标
3. 从理论层面解释不同场景下方法表现差异的原因
4. 结合模拟结果评价一篇使用PSM-DID的经济学论文

## 仓库结构
```
├── README.md               # 本说明文档
├── Psm.py                  # 核心模拟代码（数据生成+估计量实现+可视化）
├── assignment01_psm_did_monte_carlo.md  # 作业要求与背景
├── results/                # 模拟结果输出（含指标表格、可视化图表）
│   ├── metrics_A.csv       # 场景A的评估指标
│   ├── metrics_B.csv       # 场景B的评估指标
│   ├── metrics_C.csv       # 场景C的评估指标
│   └── figures/            # 核密度图、倾向得分分布图等
├── paper_evaluation.md     # 论文评价报告
└── ai_usage_record.md      # AI工具使用记录
```

## 核心功能说明
### 1. 数据生成（generate_data函数）
构造三种场景的面板数据：
- **场景A**：基准情形（无条件平行趋势成立）
- **场景B**：PSM-DID优势场景（趋势差异依赖可观测协变量X）
- **场景C**：PSM-DID失效场景（存在未观测时变混淆变量U）

### 2. 估计方法实现
| 方法    | 函数               | 核心逻辑                                          |
| ------- | ------------------ | ------------------------------------------------- |
| DID     | `estimate_did`     | 标准双重差分回归（Y ~ treat + time + treat:time） |
| PSM     | `estimate_psm`     | 倾向得分匹配后比较结果变化量的均值差              |
| PSM-DID | `estimate_psm_did` | 先匹配再在匹配样本上执行DID回归                   |

### 3. 模拟与评估
- `run_simulation`：执行500次蒙特卡洛模拟，输出各方法的估计结果
- `calculate_metrics`：计算偏差、RMSE、标准差等核心评估指标
- `plot_simulation_results`：绘制估计值核密度分布图，直观对比方法表现
- `check_balance_and_common_support`：检验协变量平衡性与倾向得分共同支持性

## 环境依赖
```bash
pip install numpy pandas seaborn matplotlib scikit-learn statsmodels
```

## 运行方式
```bash
# 直接运行完整模拟流程
python Psm.py

# 分步运行（建议在Jupyter Notebook中执行）
# 1. 生成模拟数据
df_A = generate_data(scenario="A")

# 2. 单次估计示例
did_est = estimate_did(df_A)
psm_est = estimate_psm(df_A)
psm_did_est = estimate_psm_did(df_A)

# 3. 执行完整模拟
sim_results_A = run_simulation("A")

# 4. 计算评估指标
metrics_A = calculate_metrics(sim_results_A, TAU_TRUE)

# 5. 可视化结果
plot_simulation_results(data_to_plot_A, TAU_TRUE, "场景A (基准)")
```

## 关键结果结论
1. **场景A**：DID、PSM、PSM-DID均能无偏估计真实处理效应，PSM-DID方差略低
2. **场景B**：DID存在显著偏差，PSM-DID通过匹配恢复条件平行趋势，偏差大幅降低
3. **场景C**：由于未观测时变混淆，PSM-DID仍无法解决识别问题，三种方法均失效


## 学术诚信声明
本仓库代码与报告为独立完成，仅用于课程作业交流。使用AI工具辅助的部分已在`ai_usage_record.md`中完整记录，所有引用内容均标注来源。严禁复制、篡改本仓库内容用于学术不端行为。