# PSM-DID Monte Carlo Simulation

本项目为《机器学习与因果推断》课程作业，通过 Monte Carlo 模拟方法系统评估 **倾向得分匹配-双重差分（PSM-DID）** 方法的识别逻辑、优势、局限和适用场景。研究比较了单独 PSM、单独 DID（基础版和协变量调整版）以及 PSM-DID 三种方法在三种不同数据生成过程（DGP）下的表现，并基于模拟结果对一篇核心期刊实证论文进行了方法学评价。

## 项目结构

```
├── monte_carlo.py                     # 完整模拟代码
├── assignment01_psm_did_monte_carlo.md # 作业要求
├── ai_chat.py                         # AI 使用代码
├── ai_usage_record.md                 # AI 工具使用记录
├── ai_report.md                       # AI 辅助写作说明
├── final_report.md                    # 完整作业报告
├── figures/                           # 图表文件夹
│   ├── results_scenario_A.png         # 场景 A 结果图
│   ├── results_scenario_B.png         # 场景 B 结果图
│   ├── results_scenario_C.png         # 场景 C 结果图
│   ├── balance_scenario_A.png         # 场景 A 平衡性检验图
│   ├── balance_scenario_B.png         # 场景 B 平衡性检验图
│   ├── balance_scenario_C.png         # 场景 C 平衡性检验图
│   ├── ps_distribution_scenario_A.png # 场景 A 倾向得分分布图
│   ├── ps_distribution_scenario_B.png # 场景 B 倾向得分分布图
│   ├── ps_distribution_scenario_C.png # 场景 C 倾向得分分布图
│   ├── summary_bias_comparison.png    # 三个场景偏误汇总图
│   └── summary_rmse_comparison.png    # 三个场景 RMSE 汇总图
└── README.md                          # 项目说明文件
```

├──

## 环境依赖

代码使用 Python 3.8+，所需库如下：

```bash
pip install numpy pandas scipy scikit-learn matplotlib seaborn tqdm
```

AI 使用 Deepseek v4 ，通过调用API进行访问，AI代码使用在 ai_chat.py 中。

## 快速运行

在终端中执行以下命令即可运行完整模拟（三个场景各 500 次，样本量 N=1000）：

```bash
python monte_carlo.py
```

运行完成后，控制台会输出每个场景下各方法的 Bias、RMSE、标准差等统计量，同时所有图表将自动保存为 PNG 文件。

## 模拟设计

### 基本参数
- 样本量：$N = 1000$
- 时期数：$T = 2$（处理前 $t=0$，处理后 $t=1$）
- 模拟次数：$R = 500$
- 真实处理效应：$\tau = 1$（常数）
- 协变量：$X_i \sim N(0, 1)$
- 个体固定效应：$\alpha_i \sim N(0, 1)$
- 随机误差：$\varepsilon_{it} \sim N(0, 0.5)$
- 匹配方法：1:1 最近邻匹配，卡尺 = 0.05，有放回

### 三种数据生成过程（DGP）

#### 场景 A – DID 表现的基准情形
**目的**：处理组和控制组满足无条件平行趋势。  
**处理分配**：$D_i$ 随机生成，与 $X_i$ 无关。  
**结果方程**：$Y_i(0, t) = \alpha_i + 0.5X_i + t + \varepsilon_{it}$  
**预期**：DID 表现最优，PSM 和 PSM-DID 因匹配损失样本而效率略低。

#### 场景 B – PSM-DID 优于 DID 的情形
**目的**：趋势差异依赖于 $X_i$，匹配后可恢复条件平行趋势。  
**处理分配**：$P(D_i=1 \mid X_i) = \text{logit}^{-1}(-2 + 2X_i)$  
**结果方程**：$Y_i(0, t) = \alpha_i + 1.5X_i + t + 1.5X_i \cdot t + \varepsilon_{it}$  
**预期**：未匹配 DID 严重有偏，PSM-DID 几乎无偏，且优于单独 PSM。

#### 场景 C – PSM-DID 失败的情形
**目的**：存在不可观测的时间变化混淆（$U_i$ 同时影响处理和结果趋势）。  
**处理分配**：$P(D_i=1 \mid X_i, U_i) = \text{logit}^{-1}(-1 + X_i + U_i)$  
**结果方程**：$Y_i(0, t) = \alpha_i + 0.5X_i + t + 0.8U_i \cdot t + \varepsilon_{it}$  
**预期**：所有方法均有偏，且 PSM/PSM-DID 的偏误可能大于未匹配 DID。

## 模拟结果

运行代码后，控制台输出如下统计结果（已验证）：

### 场景 A
| 方法      | Mean   | Bias    | RMSE   | Std    |
| --------- | ------ | ------- | ------ | ------ |
| basic_did | 0.9987 | -0.0013 | 0.0483 | 0.0483 |
| did_cov   | 0.9987 | -0.0013 | 0.0483 | 0.0483 |
| psm       | 1.0003 | 0.0003  | 0.0724 | 0.0724 |
| psm_did   | 1.0002 | 0.0002  | 0.0714 | 0.0714 |

**解读**：无条件平行趋势成立时，DID 效率最高（RMSE 最小）。PSM 和 PSM-DID 因匹配损失样本，效率下降约 33%。

### 场景 B
| 方法      | Mean   | Bias   | RMSE   | Std    |
| --------- | ------ | ------ | ------ | ------ |
| basic_did | 2.9313 | 1.9313 | 1.9340 | 0.1029 |
| did_cov   | 2.9313 | 1.9313 | 1.9340 | 0.1029 |
| psm       | 1.0372 | 0.0372 | 0.1209 | 0.1151 |
| psm_did   | 1.0117 | 0.0117 | 0.1024 | 0.1018 |

**解读**：未匹配 DID 偏误接近 193%，完全不可信；匹配后 PSM-DID 偏误降至 1.17%，RMSE 也最小。验证了 PSM-DID 通过匹配恢复条件平行趋势的能力。

### 场景 C
| 方法      | Mean   | Bias   | RMSE   | Std    |
| --------- | ------ | ------ | ------ | ------ |
| basic_did | 1.5925 | 0.5925 | 0.5961 | 0.0660 |
| did_cov   | 1.5925 | 0.5925 | 0.5961 | 0.0660 |
| psm       | 1.6676 | 0.6676 | 0.6762 | 0.1076 |
| psm_did   | 1.6676 | 0.6676 | 0.6761 | 0.1069 |

**解读**：所有方法均有显著偏误，且 PSM/PSM-DID 的偏误甚至大于基础 DID。这揭示了 PSM-DID 的核心局限——对**随时间变化的未观测混淆**完全无效，甚至可能放大偏误。

## 图表说明

运行代码后自动生成以下图表（均保存为 PNG）：

- **results_scenario_X.png**：每个场景的四合一图（核密度、偏误柱状图、RMSE 柱状图、箱线图）。
- **balance_scenario_X.png**：匹配前后协变量标准化差异及倾向得分均值差异。
- **ps_distribution_scenario_X.png**：倾向得分分布直方图及累积分布图（用于检验共同支持）。
- **summary_bias_comparison.png**：三个场景偏误汇总对比。
- **summary_rmse_comparison.png**：三个场景 RMSE 汇总对比。

这些图表可直接用于作业报告或论文展示。

## 理论解释要点

基于模拟结果，本作业回答了六个理论问题（详见报告）：

1. **PSM 有效条件**：处理分配仅依赖可观测协变量，且条件可忽略性成立（场景 B 证明）。
2. **DID 有效条件**：无条件平行趋势成立 + 个体固定效应可被差分消除（场景 A 证明）。
3. **PSM-DID 优于 DID 的条件**：趋势差异由可观测协变量驱动，匹配后条件平行趋势恢复（场景 B）。
4. **PSM-DID 失败条件**：存在随时间变化的不可观测混淆（场景 C），或共同支持严重不足。
5. **估计对象**：标准 1:1 最近邻匹配估计的是 **ATT**，若处理效应同质则 ATE=ATT。
6. **共同支持不足的影响**：同时增大偏误（外推）和方差（样本损失）。

## 参考文献

- Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score in observational studies for causal effects. *Biometrika*, 70(1), 41-55.
- Heckman, J. J., Ichimura, H., & Todd, P. E. (1997). Matching as an econometric evaluation estimator. *The Review of Economic Studies*, 64(4), 605-654.
- Smith, J. A., & Todd, P. E. (2005). Does matching overcome LaLonde's critique of nonexperimental estimators? *Journal of Econometrics*, 125(1-2), 305-353.
- 石大千，丁海，卫平，刘建江. 智慧城市建设能否降低环境污染[J]. 中国工业经济，2018(6): 117-135.（作业文献评价部分）

## 学术诚信与 AI 使用

本项目的代码完全由本人独立编写和调试，模拟结果真实可复现。在理论解释和文献评价部分使用了 AI 工具进行辅助梳理，所有核心判断和结论均由本人负责。详细的 AI 使用记录见 `ai_usage_record.md`。

## 联系方式

如有疑问或建议，欢迎通过课程讨论群或邮件 2023201527@ruc.edu.cn 联系。

--- 
**最后更新**：2026 年 5 月  
**课程**：机器学习与因果推断
