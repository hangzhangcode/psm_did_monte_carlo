--- 对话开始于 2026-05-19 17:06:55 ---


我：请按照这四个步骤，逐条分析我上传的作业文件，梳理作业要求、拆解任务、给出写作框架。

AI：好的，我已经完整通读了你上传的作业文件。这是一份关于“用Monte Carlo模拟理解PSM-DID”的课程作业，内容详实，要求明确。

现在，我将严格按照你要求的四个步骤进行分析和梳理。

---

### 步骤一：作业总体分析

本次作业的核心目标是：**通过自行设计的 Monte Carlo 模拟，深入理解 PSM-DID 方法在因果推断中的识别逻辑、适用条件、相对优势以及潜在局限，并最终能够评价一篇应用该方法的实证论文。**

**核心研究问题：**
在何种数据生成机制下，PSM-DID 的表现优于或劣于单独的 PSM 和 DID？其背后的理论原因是什么？

**全部任务要求（含评分标准对照）：**

1.  **设计数据生成过程 (DGP) (分值: 25%)**:
    -   必须构建一个面板或重复截面数据模拟环境。
    -   包含至少一个处理前协变量 `X_i`、至少两个时期（处理前/后）。
    -   **明确写出**处理分配机制、潜在/观测结果方程、真实处理效应 `τ`。
    -   模拟重复次数至少 500 次。
    -   **核心**: 设计至少三个场景（A, B, C），每个场景旨在检验 DGP 不同特征对 PSM-DID 表现的影响。
        -   **场景 A (基准):** 满足无条件平行趋势，预期 DID 表现良好。
        -   **场景 B (PSM-DID 优势):** 趋势差异依赖 `X_i`，匹配后满足条件平行趋势。
        -   **场景 C (PSM-DID 失败):** 存在不可观测时间异质性、共同支持不足或错误匹配变量。

2.  **比较三种估计方法 (分值: 20%)**:
    -   在每个场景下，比较 **单独 PSM**、**单独 DID** 和 **PSM-DID** 的表现。
    -   DID 方法需包含基础 DID 和控制协变量的 DID 回归版本。
    -   **报告指标**: 各方法估计值的平均值、Bias、RMSE、标准差。
    -   **可视化**: 展示估计值分布图、匹配前后协变量平衡情况、倾向得分共同支持图。
    -   **核心**: 解释“为什么”某个方法在一个场景下更好或更差，而非仅仅报告结果。

3.  **理论解释 (分值: 25%)**:
    -   回答六个特定理论问题，**并确保解释与模拟设计严格对应**，避免泛泛而谈。
    -   问题涵盖：PSM 的有效性条件、DID 的有效性条件、PSM-DID 相较于 DID 的优势条件、PSM-DID 的失败条件、匹配改变了估计对象（ATE vs. ATT）、共同支持不足的后果。

4.  **评价一篇实证论文 (分值: 20%)**:
    -   选择一篇使用 PSM-DID 的期刊论文（经济学、金融等相关领域）。
    -   **评价内容需涵盖**：研究问题与处理变量、选择 PSM-DID 的理由、匹配变量的时效性（是否处理前变量）、共同支持与平衡性检验、平行趋势假设的可信度与检验、不可观测混淆/政策干扰的风险、估计对象（ATE/ATT）、结合模拟经验给出可信度评估。

5.  **最终提交与写作 (分值: 10%)**:
    -   提交 Markdown 格式的研究报告（3000-5000字）、可复现代码、结果图表、论文信息、AI 使用记录。
    -   严格遵循学术诚信规范。

---

### 步骤二：任务分解

根据作业要求，你可以将整个作业拆解为以下几个明确的子任务：

1.  **任务分解 A: 概念构建与阅读**
    -   复习 PSM、DID、PSM-DID 的假设条件和理解逻辑。
    -   阅读建议文献，建立对模拟设计的理论支撑。

2.  **任务分解 B: 模拟场景设计与编码**
    -   **子任务 B1**: 编写一个通用的面板数据生成函数。该函数应能灵活调整参数，以产生满足不同场景要求的 DGP。
    -   **子任务 B2**: 设计场景 A（基准：无条件平行趋势）。
    -   **子任务 B3**: 设计场景 B（条件平行趋势）。
    -   **子任务 B4**: 设计场景 C（PSM-DID 失败情形）。
    -   *(可选)* 设计更多场景以深化探索。

3.  **任务分解 C: 估计方法实现与循环**
    -   **子任务 C1**: 实现 PSM（最近邻匹配等），并确保能从匹配后的样本中得到处理效应估计。
    -   **子任务 C2**: 实现基础 DID 和含协变量的 DID 回归。
    -   **子任务 C3**: 实现 PSM-DID：先在处理前协变量上做 PSM，然后在匹配样本上做 DID。
    -   **子任务 C4**: 编写一个循环，对每个场景重复运行 `DGP -> 估计 -> 存储结果` 至少 500 次。

4.  **任务分解 D: 结果分析与可视化**
    -   **子任务 D1**: 汇总每次模拟的结果，计算每个方法在每个场景下的平均值、Bias、RMSE、标准差。
    -   **子任务 D2**: 绘制估计值分布图（如直方图或核密度图）、比较偏误的箱线图。
    -   **子任务 D3**: 生成匹配前后协变量平衡性检验的图表（如 Love plot）。
    -   **子任务 D4**: 绘制倾向得分共同支持区域图。

5.  **任务分解 E: 理论解释撰写**
    -   **子任务 E1**: 结合模拟结果，逐一回答作业中提出的六个理论问题。确保每个解释都直接引用你设计的 DGP 和观察到的模拟结果。

6.  **任务分解 F: 文献评价**
    -   **子任务 F1**: 搜索并选择一篇合适的 PSM-DID 论文。
    -   **子任务 F2**: 按照作业给出的八个评价要点，系统性地分析该论文的识别策略。
    -   **子任务 F3**: 将评价与你在模拟中获得的经验联系起来。

7.  **任务分解 G: 整合与写作**
    -   **子任务 G1**: 将上述所有内容组织成一份结构清晰、逻辑连贯的 Markdown 研究报告。
    -   **子任务 G2**: 整理所有代码、图表和论文引用。
    -   **子任务 G3**: 撰写 AI 使用记录。

---

### 步骤三：整体解题与写作思路框架

**总体思路**：遵循“提出问题（作业要求）→ 设计工具（模拟）→ 验证猜想（结果）→ 深化理论（解释）→ 应用实践（文献评价）”的闭环逻辑。

**写作框架建议**：

1.  **摘要**
    -   简述研究目的（用模拟理解PSM-DID）。
    -   概括三个核心场景的设计意图。
    -   点明主要发现（PSM-DID在何种条件下有效/无效）。
    -   结论（对实证研究的启示）。

2.  **引言**
    -   重申PSM-DID在实证中的流行性和潜在风险。
    -   简述Monte Carlo模拟在因果推断方法论研究中的价值。
    -   概述本报告的路径图。

3.  **数据生成过程（DGP）设计**
    -   **3.1 基础设定**: 定义时期、样本量、协变量 (`X`)、真实效应 (`τ`)、误差项等。
    -   **3.2 处理分配机制**: 统一写出 `P(D_i=1 | X)` 的函数形式。
    -   **3.3 结果方程**: 写出 `Y_it(0)` 和 `Y_it(1)` 的生成方程。这是最关键的部分。
    -   **3.4 三个模拟场景**: 分别详细说明每个场景的**参数设置**如何体现其设计意图。**建议列表形式清晰地对比三个场景在结果方程、处理分配、未观测异质性等方面的差异。**

    *示例：*

    | 参数/特征            | 场景A (基准: 无条件平行趋势)                      | 场景B (条件平行趋势)                                        | 场景C (PSM-DID失败)                                                      |
    | :------------------- | :------------------------------------------------ | :---------------------------------------------------------- | :----------------------------------------------------------------------- |
    | **结果方程核心差异** | `Y(0)_it = α_i + λ_t + ε_it` <br> (α_i 与 D 相关) | `Y(0)_it = α_i + β*X_i + λ_t + ε_it` <br> (趋势差异由X驱动) | `Y(0)_it = α_i + β*X_i + θ*U_i*λ_t + ε_it` <br> (存在时间变化未观测混淆) |
    | **处理分配机制**     | `P(D=1\|X)` 但 `X` 不影响趋势                     | `P(D=1\|X)` 是强相关                                        | `P(D=1\|X)` 正常                                                         |
    | **平行趋势检验**     | 原始样本即满足                                    | 原始样本不满足，匹配后满足                                  | 匹配后仍不满足（或共同支持很差）                                         |
    | **预期结果**         | DID 表现最优                                      | PSM-DID 表现最优                                            | 所有方法均有偏，但 PSM-DID 偏误可能更大或方差更高                        |

4.  **模拟结果与理论解释**
    -   **4.1 场景A结果**: 展示各方法的 Bias, RMSE, 分布图。解释：为什么DID最优（消除了时间不变异质性），为什么PSM较差（可能遗漏了不可观测异质性）。
    -   **4.2 场景B结果**: 展示各方法的估计结果和匹配前后的平衡性检验（Love plot）。解释：为什么未匹配的DID有偏（违反了无条件平行趋势），而匹配后条件平行趋势成立，使得PSM-DID纠正了偏误。
    -   **4.3 场景C结果**: 展示共同支持图（可能存在稀疏或断尾），展示PSM-DID估计量仍有偏。解释：即使匹配了可观测变量，不可观测的时间变化混淆 (`θ*U_i*λ_t`) 仍然存在，导致条件平行趋势不成立。或者，由于共同支持不足，匹配过程引入了高方差和偏误。
    -   **4.4 小结**: 综合三个场景，回答作业中提出的六个理论问题，形成一张表格进行对比。

    *示例表格：回答理论问题与模拟设计的对应*

    | 理论问题                              | 对应的模拟场景与证据                                                                                    | 你的结论/解释                                                                                     |
    | ------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
    | 1. PSM 何时有效？                     | 场景A中，PSM 的偏误可能源于未控制的时间不变异质性。在场景B中匹配后，若处理选择基于可观测变量，PSM有效。 | PSM 有效需要**条件可忽略性**，即没有与处理效应相关的不可观测变量。                                |
    | 2. DID 何时有效？                     | 场景A中DID表现好（无条件平行趋势）。场景B中基础DID偏，但控制X后DID表现较好。                            | DID 有效性依赖于**平行趋势假设**，可以是无条件或条件于协变量。                                    |
    | 3. PSM-DID 何时优于 DID？             | 场景B中，PSM-DID 纠正了因 `X` 导致的趋势差异偏误，优于未匹配的 DID。                                    | 当趋势差异由可观测协变量驱动时，PSM-DID通过匹配使处理组和控制组在协变量上可比，从而恢复平行趋势。 |
    | 4. PSM-DID 何时失败？                 | 场景C中，存在 `U*λ_t` 导致不可观测时间混淆，PSM-DID无法解决。                                           | 如果存在**不可观测的、随时间变化的混淆因素**，无论怎么匹配都无法满足条件平行趋势，PSM-DID失效。   |
    | 5. 匹配是否改变估计对象 (ATE vs ATT)? | 通过检查PSM的权重设计（通常是ATT）来讨论。                                                              | PSM通常为处理组寻找匹配，其设计自然倾向于估计**ATT**。用户可将此点与场景B的估计结果对比分析。     |
    | 6. 共同支持不足的影响？               | 场景C中刻意制造共同支持不足，导致方差很大，且匹配偏差难以消除。                                         | 缺乏共同支持使得匹配依赖外推，导致估计方差激增和潜在的匹配偏误。                                  |

5.  **论文评价**
    -   **5.1 所选论文简介**: 确保引用完整。
    -   **5.2 识别策略分析**: 针对八个要点逐一或合并分析。
        -   *例如：* “作者使用PSM-DID的主要理由是……但其匹配变量`Schooling`是处理后的变量，这可能导致‘坏匹配’问题，正如我模拟中的场景……所暗示的风险。”
    -   **5.3 结合模拟经验的可信度评估**: “基于我的模拟，该论文的识别策略在假设……（如趋势差异仅由`X`驱动）时是可信的，但在……（如政策同期变动或存在不可观测的趋势驱动因素）时是脆弱的，类似于我设计的场景C。”

6.  **结论**
    -   总结核心发现。
    -   对实证研究者的建议。

7.  **附录**
    -   AI 使用记录。
    -   主要代码片段。

---

以上是对你作业的完整分析与框架梳理。请确认是否理解，并准备好进入下一步的具体提问环节。

我：帮我用Python编写可直接运行的PSM-DID 蒙特卡洛模拟完整代码，包含：三场景 DGP 面板数据生成、基础 DID、协变量 DID、纯 PSM、PSM-DID 四种估计，循环 500 次模拟，自动输出 Bias、RMSE、均值、标准差，附带平衡性检验、倾向得分共同支持图、核密度结果图。

AI：我来为你编写一个完整的PSM-DID蒙特卡洛模拟Python代码。由于代码较长，我将分成几个部分说明。

## 第一部分：完整代码

```python
"""
PSM-DID Monte Carlo Simulation
Author: AI Assistant
Description: 完整的PSM-DID蒙特卡洛模拟代码
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============ 1. 数据生成函数 ============

def generate_panel_data(N, T=2, seed=None, scenario='A', params=None):
    """
    生成面板数据
    
    Parameters:
    -----------
    N : int
        个体数量
    T : int
        时期数量（默认为2）
    seed : int
        随机种子
    scenario : str
        场景类型 ('A', 'B', 'C')
    params : dict
        参数设置
    
    Returns:
    --------
    pd.DataFrame
        面板数据
    """
    if seed is not None:
        np.random.seed(seed)
    
    # 默认参数
    default_params = {
        'A': {
            'tau': 1.0,  # 真实处理效应
            'beta_x': 0.5,  # 协变量对结果的影响
            'alpha_sd': 1.0,  # 个体异质性标准差
            'epsilon_sd': 0.5,  # 误差项标准差
            'treatment_prob': 0.5,  # 基准处理概率
            'x_effect_on_treatment': 1.0,  # X对处理选择的影响
        },
        'B': {
            'tau': 1.0,
            'beta_x': 1.5,  # 增强X对结果的影响
            'alpha_sd': 1.0,
            'epsilon_sd': 0.5,
            'treatment_prob': 0.5,
            'x_effect_on_treatment': 2.0,  # 增强X对处理选择的影响
        },
        'C': {
            'tau': 1.0,
            'beta_x': 0.5,
            'alpha_sd': 1.0,
            'epsilon_sd': 0.5,
            'treatment_prob': 0.5,
            'x_effect_on_treatment': 1.0,
            'u_effect': 0.8,  # 不可观测时间变化混淆
        }
    }
    
    params = params or default_params[scenario]
    
    # 生成个体特征
    X = np.random.normal(0, 1, N)  # 可观测协变量
    alpha = np.random.normal(0, params['alpha_sd'], N)  # 个体固定效应
    
    # 处理分配
    if scenario == 'A':
        # 简单处理分配，X对处理选择有影响但不影响趋势
        logit_ps = -1 + params['x_effect_on_treatment'] * X
        ps = 1 / (1 + np.exp(-logit_ps))
        D = np.random.binomial(1, ps)
    
    elif scenario == 'B':
        # X强烈影响处理选择和结果趋势
        logit_ps = -2 + params['x_effect_on_treatment'] * X
        ps = 1 / (1 + np.exp(-logit_ps))
        D = np.random.binomial(1, ps)
    
    elif scenario == 'C':
        # 引入不可观测混淆因素
        U = np.random.normal(0, 1, N)  # 不可观测变量
        logit_ps = -1 + params['x_effect_on_treatment'] * X + 1.0 * U
        ps = 1 / (1 + np.exp(-logit_ps))
        D = np.random.binomial(1, ps)
    
    # 生成结果变量
    data_list = []
    
    for t in range(T):
        time_effect = t  # 时间趋势
        
        # 基线结果（处理=0）
        if scenario == 'A':
            Y0 = alpha + 0.5 * X + time_effect + np.random.normal(0, params['epsilon_sd'], N)
        
        elif scenario == 'B':
            # 结果趋势依赖于X
            trend_effect = params['beta_x'] * X * t
            Y0 = alpha + params['beta_x'] * X + time_effect + trend_effect + np.random.normal(0, params['epsilon_sd'], N)
        
        elif scenario == 'C':
            # 不可观测时间变化混淆
            confound_effect = params['u_effect'] * U * t
            Y0 = alpha + 0.5 * X + time_effect + confound_effect + np.random.normal(0, params['epsilon_sd'], N)
        
        # 处理结果
        Y1 = Y0 + params['tau'] * D
        
        # 观测结果（处理后时期才有处理效应）
        if t == 1:
            Y = Y1
        else:
            Y = Y0
        
        # 构建数据框
        df_temp = pd.DataFrame({
            'id': range(N),
            'time': t,
            'Y': Y,
            'Y0': Y0,
            'Y1': Y1,
            'D': D,
            'X': X,
            'alpha': alpha
        })
        
        if scenario == 'C':
            df_temp['U'] = U
        
        data_list.append(df_temp)
    
    df = pd.concat(data_list, ignore_index=True)
    
    # 添加处理后标识
    df['post'] = (df['time'] == 1).astype(int)
    df['did'] = df['D'] * df['post']  # 交互项
    
    return df


# ============ 2. 估计函数 ============

def estimate_basic_did(df):
    """
    基础DID估计
    """
    # 计算各组各时期均值
    means = df.groupby(['D', 'post'])['Y'].mean()
    
    # DID估计量
    treat_diff = means[1, 1] - means[1, 0]
    control_diff = means[0, 1] - means[0, 0]
    
    tau_did = treat_diff - control_diff
    
    return tau_did


def estimate_covariate_did(df):
    """
    控制协变量的DID估计（使用OLS）
    """
    from sklearn.linear_model import LinearRegression
    
    # 准备数据
    X = df[['D', 'post', 'did', 'X']].values
    y = df['Y'].values
    
    # OLS估计
    model = LinearRegression()
    model.fit(X, y)
    
    # DID系数是交互项的系数（第3个变量）
    tau_did_cov = model.coef_[2]
    
    return tau_did_cov


def estimate_psm(df, method='basic'):
    """
    PSM估计（使用处理后结果的变化）
    """
    # 准备处理前数据
    df_pre = df[df['time'] == 0].copy()
    df_post = df[df['time'] == 1].copy()
    
    # 计算结果变化
    df_change = pd.merge(df_pre[['id', 'Y', 'D', 'X']], 
                         df_post[['id', 'Y']], 
                         on='id', 
                         suffixes=('_pre', '_post'))
    
    df_change['delta_Y'] = df_change['Y_post'] - df_change['Y_pre']
    
    # 估计倾向得分
    X_ps = df_change[['X']].values
    y_treat = df_change['D'].values
    
    logit = LogisticRegression(C=1e8)
    logit.fit(X_ps, y_treat)
    ps = logit.predict_proba(X_ps)[:, 1]
    
    df_change['ps'] = ps
    
    # 倾向得分匹配（最近邻匹配，1:1，有放回）
    treat_indices = df_change[df_change['D'] == 1].index
    control_indices = df_change[df_change['D'] == 0].index
    
    if len(treat_indices) == 0 or len(control_indices) == 0:
        return np.nan
    
    # 匹配
    treat_ps = df_change.loc[treat_indices, 'ps'].values.reshape(-1, 1)
    control_ps = df_change.loc[control_indices, 'ps'].values.reshape(-1, 1)
    
    nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
    nn.fit(control_ps)
    distances, indices = nn.kneighbors(treat_ps)
    
    # 获取匹配的控制组
    matched_control_indices = control_indices[indices.flatten()]
    
    # 计算ATT
    matched_treat = df_change.loc[treat_indices, 'delta_Y'].values
    matched_control = df_change.loc[matched_control_indices, 'delta_Y'].values
    
    tau_psm = np.mean(matched_treat - matched_control)
    
    return tau_psm


def estimate_psm_did(df, caliper=0.05):
    """
    PSM-DID估计
    """
    # 使用处理前协变量进行匹配
    df_pre = df[df['time'] == 0].copy()
    df_post = df[df['time'] == 1].copy()
    
    # 估计倾向得分
    X_ps = df_pre[['X']].values
    y_treat = df_pre['D'].values
    
    if len(np.unique(y_treat)) < 2:
        return np.nan
    
    logit = LogisticRegression(C=1e8)
    logit.fit(X_ps, y_treat)
    ps = logit.predict_proba(X_ps)[:, 1]
    
    df_pre['ps'] = ps
    
    # 分离处理组和控制组
    treat_indices = df_pre[df_pre['D'] == 1].index
    control_indices = df_pre[df_pre['D'] == 0].index
    
    if len(treat_indices) == 0 or len(control_indices) == 0:
        return np.nan
    
    # 匹配
    treat_ps = df_pre.loc[treat_indices, 'ps'].values.reshape(-1, 1)
    control_ps = df_pre.loc[control_indices, 'ps'].values.reshape(-1, 1)
    
    nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
    nn.fit(control_ps)
    distances, indices = nn.kneighbors(treat_ps)
    
    # 应用卡尺
    valid_matches = distances.flatten() <= caliper
    
    if np.sum(valid_matches) == 0:
        return np.nan
    
    matched_treat_indices = treat_indices[valid_matches]
    matched_control_indices = control_indices[indices.flatten()[valid_matches]]
    
    df_post = df_post.reset_index(drop=True)

    # 获取匹配后的处理组和控制组
    matched_treat_pre = df_pre.loc[matched_treat_indices, 'Y'].values
    matched_treat_post = df_post.iloc[matched_treat_indices]['Y'].values
    
    matched_control_pre = df_pre.loc[matched_control_indices, 'Y'].values
    matched_control_post = df_post.iloc[matched_control_indices]['Y'].values
    
    # DID计算
    treat_diff = matched_treat_post - matched_treat_pre
    control_diff = matched_control_post - matched_control_pre
    
    tau_psm_did = np.mean(treat_diff - control_diff)
    
    return tau_psm_did


def check_balance(df, df_matched):
    """
    检查匹配前后的协变量平衡性
    """
    # 匹配前
    before_treat = df[df['D'] == 1]['X']
    before_control = df[df['D'] == 0]['X']
    
    # 匹配后
    after_treat = df_matched[df_matched['D'] == 1]['X']
    after_control = df_matched[df_matched['D'] == 0]['X']
    
    # 计算标准化差异
    def std_diff(treat, control):
        pooled_std = np.sqrt((np.var(treat) + np.var(control)) / 2)
        return (np.mean(treat) - np.mean(control)) / pooled_std
    
    std_diff_before = std_diff(before_treat, before_control)
    std_diff_after = std_diff(after_treat, after_control)
    
    # t检验
    t_before = stats.ttest_ind(before_treat, before_control)
    t_after = stats.ttest_ind(after_treat, after_control)
    
    return {
        'std_diff_before': std_diff_before,
        'std_diff_after': std_diff_after,
        'p_value_before': t_before.pvalue,
        'p_value_after': t_after.pvalue
    }


# ============ 3. 蒙特卡洛模拟主函数 ============

def monte_carlo_simulation(scenario='A', N=1000, n_simulations=500, verbose=True):
    """
    执行蒙特卡洛模拟
    """
    results = []
    balance_results = []
    
    for sim in tqdm(range(n_simulations), desc=f'场景 {scenario}', disable=not verbose):
        # 生成数据
        df = generate_panel_data(N=N, seed=sim, scenario=scenario)
        
        # 各方法估计
        tau_true = 1.0  # 真实处理效应
        
        tau_basic_did = estimate_basic_did(df)
        tau_did_cov = estimate_covariate_did(df)
        tau_psm = estimate_psm(df)
        tau_psm_did = estimate_psm_did(df)
        
        # 存储结果
        results.append({
            'simulation': sim,
            'true_effect': tau_true,
            'basic_did': tau_basic_did,
            'did_cov': tau_did_cov,
            'psm': tau_psm,
            'psm_did': tau_psm_did
        })
        
        # 平衡性检查（只对第一次模拟）
        if sim == 0:
            balance_info = check_balance_pre_post(df)
            balance_results.append(balance_info)
    
    results_df = pd.DataFrame(results)
    
    # 计算统计量
    stats_df = calculate_statistics(results_df)
    
    return results_df, stats_df, balance_results


def check_balance_pre_post(df):
    """
    检查匹配前后的协变量平衡性（辅助函数）
    """
    df_pre = df[df['time'] == 0].copy()
    
    # 获取匹配后的样本
    X_ps = df_pre[['X']].values
    logit = LogisticRegression(C=1e8)
    logit.fit(X_ps, df_pre['D'])
    ps = logit.predict_proba(X_ps)[:, 1]
    df_pre['ps'] = ps
    
    treat_indices = df_pre[df_pre['D'] == 1].index
    control_indices = df_pre[df_pre['D'] == 0].index
    
    if len(treat_indices) > 0 and len(control_indices) > 0:
        treat_ps = df_pre.loc[treat_indices, 'ps'].values.reshape(-1, 1)
        control_ps = df_pre.loc[control_indices, 'ps'].values.reshape(-1, 1)
        
        nn = NearestNeighbors(n_neighbors=1)
        nn.fit(control_ps)
        distances, indices = nn.kneighbors(treat_ps)
        
        matched_control_indices = control_indices[indices.flatten()]
        
        # 匹配后样本
        matched_treat = df_pre.loc[treat_indices]
        matched_control = df_pre.loc[matched_control_indices]
        
        # 原始样本
        original_treat = df_pre[df_pre['D'] == 1]
        original_control = df_pre[df_pre['D'] == 0]
        
        # 计算标准化差异
        def std_diff(treat, control, var_name):
            pooled_std = np.sqrt((np.var(treat[var_name]) + np.var(control[var_name])) / 2)
            return (np.mean(treat[var_name]) - np.mean(control[var_name])) / pooled_std
        
        result = {
            'original_std_diff': std_diff(original_treat, original_control, 'X'),
            'matched_std_diff': std_diff(matched_treat, matched_control, 'X'),
            'original_ps_mean_diff': np.mean(original_treat['ps']) - np.mean(original_control['ps']),
            'matched_ps_mean_diff': np.mean(matched_treat['ps']) - np.mean(matched_control['ps'])
        }
    else:
        result = {
            'original_std_diff': np.nan,
            'matched_std_diff': np.nan,
            'original_ps_mean_diff': np.nan,
            'matched_ps_mean_diff': np.nan
        }
    
    return result


def calculate_statistics(results_df):
    """
    计算各方法的统计量
    """
    methods = ['basic_did', 'did_cov', 'psm', 'psm_did']
    stats = {}
    
    for method in methods:
        estimates = results_df[method].dropna().values
        true_effect = results_df['true_effect'].iloc[0]
        
        stats[method] = {
            'mean': np.mean(estimates),
            'bias': np.mean(estimates) - true_effect,
            'rmse': np.sqrt(np.mean((estimates - true_effect)**2)),
            'std': np.std(estimates),
            'median': np.median(estimates),
            'n_success': len(estimates),
            'n_total': len(results_df)
        }
    
    return pd.DataFrame(stats).T


# ============ 4. 可视化函数 ============

def plot_results(results_df, stats_df, scenario_name):
    """
    绘制结果图
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    methods = ['basic_did', 'did_cov', 'psm', 'psm_did']
    method_labels = ['基础 DID', '协变量 DID', '纯 PSM', 'PSM-DID']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # 1. 核密度估计图
    ax1 = axes[0, 0]
    for method, label, color in zip(methods, method_labels, colors):
        estimates = results_df[method].dropna().values
        if len(estimates) > 0:
            sns.kdeplot(estimates, ax=ax1, label=label, color=color, linewidth=2)
    
    ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='真实效应=1.0')
    ax1.set_xlabel('估计值', fontsize=12)
    ax1.set_ylabel('密度', fontsize=12)
    ax1.set_title(f'场景{scenario_name}: 估计值分布', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 2. 偏误比较
    ax2 = axes[0, 1]
    biases = []
    for method in methods:
        biases.append(stats_df.loc[method, 'bias'])
    
    bars = ax2.bar(method_labels, biases, color=colors, alpha=0.7, edgecolor='black')
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax2.set_ylabel('偏误 (Bias)', fontsize=12)
    ax2.set_title(f'场景{scenario_name}: 方法偏误比较', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 在柱状图上添加数值标签
    for bar, bias in zip(bars, biases):
        y_pos = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, y_pos, f'{bias:.3f}', 
                 ha='center', va='bottom' if y_pos >= 0 else 'top', fontsize=10)
    
    # 3. RMSE比较
    ax3 = axes[1, 0]
    rmses = []
    for method in methods:
        rmses.append(stats_df.loc[method, 'rmse'])
    
    bars3 = ax3.bar(method_labels, rmses, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_ylabel('RMSE', fontsize=12)
    ax3.set_title(f'场景{scenario_name}: RMSE比较', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, rmse in zip(bars3, rmses):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{rmse:.3f}', 
                 ha='center', va='bottom', fontsize=10)
    
    # 4. 箱线图
    ax4 = axes[1, 1]
    plot_data = [results_df[method].dropna().values for method in methods]
    bp = ax4.boxplot(plot_data, labels=method_labels, patch_artist=True)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax4.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='真实效应')
    ax4.set_ylabel('估计值', fontsize=12)
    ax4.set_title(f'场景{scenario_name}: 估计值箱线图', fontsize=14, fontweight='bold')
    ax4.legend(loc='best', fontsize=10)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def plot_balance_check(balance_results, scenario_name):
    """
    绘制平衡性检验图
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 从模拟结果中提取平衡性数据
    original_std_diffs = [r['original_std_diff'] for r in balance_results if not np.isnan(r['original_std_diff'])]
    matched_std_diffs = [r['matched_std_diff'] for r in balance_results if not np.isnan(r['matched_std_diff'])]
    
    # 倾向得分差异
    original_ps_diffs = [r['original_ps_mean_diff'] for r in balance_results if not np.isnan(r['original_ps_mean_diff'])]
    matched_ps_diffs = [r['matched_ps_mean_diff'] for r in balance_results if not np.isnan(r['matched_ps_mean_diff'])]
    
    labels = ['匹配前', '匹配后']
    
    # 标准化差异图
    ax1 = axes[0]
    avg_std_diffs = [np.mean(original_std_diffs), np.mean(matched_std_diffs)]
    ax1.bar(labels, avg_std_diffs, color=['#FF6B6B', '#4ECDC4'], alpha=0.7, edgecolor='black')
    ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax1.set_ylabel('标准化差异', fontsize=12)
    ax1.set_title(f'场景{scenario_name}: 协变量X平衡性', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 倾向得分差异图
    ax2 = axes[1]
    avg_ps_diffs = [np.mean(original_ps_diffs), np.mean(matched_ps_diffs)]
    ax2.bar(labels, avg_ps_diffs, color=['#FF6B6B', '#4ECDC4'], alpha=0.7, edgecolor='black')
    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.set_ylabel('倾向得分均值差异', fontsize=12)
    ax2.set_title(f'场景{scenario_name}: 倾向得分平衡性', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


def plot_propensity_scores(df, scenario_name):
    """
    绘制倾向得分共同支持图
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 使用第一时期数据
    df_pre = df[df['time'] == 0].copy()
    
    # 估计倾向得分
    X_ps = df_pre[['X']].values
    logit = LogisticRegression(C=1e8)
    logit.fit(X_ps, df_pre['D'])
    ps = logit.predict_proba(X_ps)[:, 1]
    df_pre['ps'] = ps
    
    # 分离处理组和控制组
    treat_ps = df_pre[df_pre['D'] == 1]['ps']
    control_ps = df_pre[df_pre['D'] == 0]['ps']
    
    # 1. 直方图
    ax1 = axes[0]
    ax1.hist(treat_ps, bins=30, alpha=0.5, label='处理组', color='#FF6B6B', density=True)
    ax1.hist(control_ps, bins=30, alpha=0.5, label='控制组', color='#4ECDC4', density=True)
    ax1.set_xlabel('倾向得分', fontsize=12)
    ax1.set_ylabel('密度', fontsize=12)
    ax1.set_title(f'场景{scenario_name}: 倾向得分分布', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 2. 累积分布图
    ax2 = axes[1]
    ax2.hist(treat_ps, bins=30, alpha=0.5, label='处理组', color='#FF6B6B', cumulative=True, density=True, histtype='step', linewidth=2)
    ax2.hist(control_ps, bins=30, alpha=0.5, label='控制组', color='#4ECDC4', cumulative=True, density=True, histtype='step', linewidth=2)
    ax2.set_xlabel('倾向得分', fontsize=12)
    ax2.set_ylabel('累积概率', fontsize=12)
    ax2.set_title(f'场景{scenario_name}: 倾向得分累积分布', fontsize=14, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# ============ 5. 主程序 ============

def main():
    """
    主程序：执行三个场景的模拟并生成图表
    """
    print("="*60)
    print("PSM-DID 蒙特卡洛模拟开始")
    print("="*60)
    
    # 模拟参数
    N = 1000  # 样本量
    n_simulations = 500  # 模拟次数
    
    all_results = {}
    all_stats = {}
    all_balance = {}
    
    # 执行三个场景的模拟
    for scenario in ['A', 'B', 'C']:
        print(f"\n执行场景 {scenario}...")
        
        results_df, stats_df, balance_results = monte_carlo_simulation(
            scenario=scenario, 
            N=N, 
            n_simulations=n_simulations
        )
        
        all_results[scenario] = results_df
        all_stats[scenario] = stats_df
        all_balance[scenario] = balance_results
        
        # 打印结果
        print(f"\n场景 {scenario} 结果:")
        print("-"*40)
        print(stats_df.round(4))
        print("-"*40)
    
    # 生成图表
    print("\n生成图表...")
    
    # 1. 生成各场景的结果图和平衡性检验图
    for scenario in ['A', 'B', 'C']:
        # 结果图
        fig1 = plot_results(all_results[scenario], all_stats[scenario], scenario)
        fig1.savefig(f'results_scenario_{scenario}.png', dpi=150, bbox_inches='tight')
        plt.close(fig1)
        
        # 平衡性检验图
        fig2 = plot_balance_check(all_balance[scenario], scenario)
        fig2.savefig(f'balance_scenario_{scenario}.png', dpi=150, bbox_inches='tight')
        plt.close(fig2)
        
        # 倾向得分图
        df_demo = generate_panel_data(N=N, seed=42, scenario=scenario)
        fig3 = plot_propensity_scores(df_demo, scenario)
        fig3.savefig(f'ps_distribution_scenario_{scenario}.png', dpi=150, bbox_inches='tight')
        plt.close(fig3)
    
    # 2. 生成比较三个场景的汇总图
    # 创建一个汇总结果DataFrame
    summary_data = []
    for scenario in ['A', 'B', 'C']:
        stats_df = all_stats[scenario]
        for method in stats_df.index:
            summary_data.append({
                'Scenario': f'场景 {scenario}',
                'Method': method,
                'Bias': stats_df.loc[method, 'bias'],
                'RMSE': stats_df.loc[method, 'rmse'],
                'Std': stats_df.loc[method, 'std']
            })
    
    summary_df = pd.DataFrame(summary_data)
    
    # 绘制汇总偏误图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    methods = ['basic_did', 'did_cov', 'psm', 'psm_did']
    method_labels = ['基础 DID', '协变量 DID', '纯 PSM', 'PSM-DID']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    scenarios = ['场景 A', '场景 B', '场景 C']
    x = np.arange(len(methods))
    width = 0.25
    
    for i, scenario in enumerate(scenarios):
        sub_df = summary_df[summary_df['Scenario'] == scenario]
        biases = [sub_df[sub_df['Method'] == m]['Bias'].values[0] for m in methods]
        ax.bar(x + i*width, biases, width, label=scenario, alpha=0.7)
    
    ax.set_xlabel('方法', fontsize=12)
    ax.set_ylabel('偏误 (Bias)', fontsize=12)
    ax.set_title('三个场景的偏误比较', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(method_labels, fontsize=10)
    ax.legend(loc='best', fontsize=10)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('summary_bias_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 绘制汇总RMSE图
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, scenario in enumerate(scenarios):
        sub_df = summary_df[summary_df['Scenario'] == scenario]
        rmses = [sub_df[sub_df['Method'] == m]['RMSE'].values[0] for m in methods]
        ax.bar(x + i*width, rmses, width, label=scenario, alpha=0.7)
    
    ax.set_xlabel('方法', fontsize=12)
    ax.set_ylabel('RMSE', fontsize=12)
    ax.set_title('三个场景的RMSE比较', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(method_labels, fontsize=10)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('summary_rmse_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. 打印最终统计表
    print("\n" + "="*60)
    print("最终结果汇总")
    print("="*60)
    
    for scenario in ['A', 'B', 'C']:
        print(f"\n场景 {scenario}:")
        print(all_stats[scenario].round(4))
        print("\n")
    
    print("所有图表已保存到当前目录。")
    print("模拟完成！")
    
    return all_results, all_stats


# ============ 6. 程序入口 ============

if __name__ == "__main__":
    # 运行主程序
    all_results, all_stats = main()
```

## 第二部分：代码关键点说明

### 1. 数据生成过程（DGP）设计

| 场景            | 核心特征       | 代码实现                                       |
| --------------- | -------------- | ---------------------------------------------- |
| A (基准)        | 无条件平行趋势 | `Y0 = alpha + 0.5*X + time_effect + ε`         |
| B (PSM-DID优势) | 趋势依赖X      | `Y0 = alpha + β*X + time_effect + β*X*t + ε`   |
| C (PSM-DID失败) | 不可观测混淆   | `Y0 = alpha + 0.5*X + time_effect + θ*U*t + ε` |

### 2. 四种估计方法

```python
# 1. 基础 DID
tau_did = (Y_treat_post - Y_treat_pre) - (Y_control_post - Y_control_pre)

# 2. 协变量 DID
Y ~ D + post + (D×post) + X   # 交互项系数即为DID估计量

# 3. 纯 PSM
PS_match(Y_post - Y_pre, on=X)  # 匹配后比较结果变化

# 4. PSM-DID
PS_match(treatment on X_pre) → 在匹配样本上做DID
```

## 第三部分：运行指南

```bash
# 安装所需包
pip install numpy pandas scipy scikit-learn matplotlib seaborn tqdm

# 运行代码
python psm_did_simulation.py
```

## 第四部分：预期输出

运行后将在当前目录生成以下文件：

1. **结果图（9张）**：
   - `results_scenario_A.png`（含核密度图、偏误、RMSE、箱线图）
   - `results_scenario_B.png`
   - `results_scenario_C.png`
   - `balance_scenario_A/B/C.png`（平衡性检验）
   - `ps_distribution_scenario_A/B/C.png`（倾向得分分布）
   - `summary_bias_comparison.png`（三场景偏误汇总）
   - `summary_rmse_comparison.png`（三场景RMSE汇总）

2. **控制台输出**：各场景下四种方法的偏误、RMSE、标准差等统计量

**典型预期结果**：
- 场景A：基础DID偏误最小（~0），PSM可能略有偏
- 场景B：PSM-DID优于基础DID，匹配后偏误显著降低
- 场景C：所有方法都有偏，PSM-DID无法消除不可观测混淆

请运行代码并根据实际输出结果来撰写报告中的结果分析部分。如果需要调整某个场景的参数（如样本量、效应大小、混淆程度），请随时告诉我。

我：

AI：非常好，看起来你希望我继续深入分析或优化这个代码。让我提供几个方向，你可以选择感兴趣的：

## 方向一：代码优化与扩展建议

### 1. 添加更丰富的场景设计

```python
# 在 generate_panel_data 函数中添加新场景
def generate_panel_data(N, T=2, seed=None, scenario='A', params=None):
    # ... 现有代码 ...
    
    # 新增场景D：时间趋势非线性
    if scenario == 'D':
        # 非线性趋势依赖X
        trend_effect = params['beta_x'] * np.sin(X) * t  # 非线性
        Y0 = alpha + 0.5 * X + time_effect + trend_effect + ...
        
    # 新增场景E：多重协变量
    if scenario == 'E':
        # 两个协变量，一个可观测一个不可观测
        X1 = np.random.normal(0, 1, N)
        X2 = np.random.normal(0, 1, N)
        # 处理选择依赖X1和X2
        # 但PSM只用X1匹配
```

### 2. 添加更多诊断指标

```python
def calculate_additional_metrics(results_df):
    """
    计算额外诊断指标
    """
    metrics = {}
    
    for method in ['basic_did', 'did_cov', 'psm', 'psm_did']:
        estimates = results_df[method].dropna()
        true_effect = 1.0
        
        # 中位数偏误
        metrics[f'{method}_median_bias'] = np.median(estimates) - true_effect
        
        # 置信区间覆盖率（95%）
        ci_lower = np.percentile(estimates, 2.5)
        ci_upper = np.percentile(estimates, 97.5)
        metrics[f'{method}_ci_coverage'] = (ci_lower <= true_effect <= ci_upper)
        
        # IQR
        metrics[f'{method}_iqr'] = np.percentile(estimates, 75) - np.percentile(estimates, 25)
        
        # 偏度和峰度
        metrics[f'{method}_skewness'] = stats.skew(estimates)
        metrics[f'{method}_kurtosis'] = stats.kurtosis(estimates)
    
    return metrics
```

## 方向二：代码效率优化

### 1. 并行化处理（加快500次模拟）

```python
from joblib import Parallel, delayed

def parallel_monte_carlo(scenario='A', N=1000, n_simulations=500, n_jobs=-1):
    """
    并行化蒙特卡洛模拟
    """
    def single_simulation(sim):
        df = generate_panel_data(N=N, seed=sim, scenario=scenario)
        
        return {
            'simulation': sim,
            'true_effect': 1.0,
            'basic_did': estimate_basic_did(df),
            'did_cov': estimate_covariate_did(df),
            'psm': estimate_psm(df),
            'psm_did': estimate_psm_did(df)
        }
    
    # 并行执行
    results = Parallel(n_jobs=n_jobs)(
        delayed(single_simulation)(sim) 
        for sim in range(n_simulations)
    )
    
    return pd.DataFrame(results)
```

### 2. 结果缓存机制

```python
import pickle
import os

def save_simulation_results(results, stats, scenario, filename_prefix='simulation_results'):
    """
    保存模拟结果到文件
    """
    output = {
        'results': results,
        'stats': stats,
        'timestamp': pd.Timestamp.now()
    }
    
    filename = f'{filename_prefix}_scenario_{scenario}.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(output, f)
    
    print(f"结果已保存到 {filename}")

def load_simulation_results(scenario, filename_prefix='simulation_results'):
    """
    加载之前保存的模拟结果
    """
    filename = f'{filename_prefix}_scenario_{scenario}.pkl'
    
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        print(f"文件 {filename} 不存在")
        return None
```

## 方向三：更详细的输出和报告

### 1. 生成LaTeX表格格式的输出

```python
def generate_latex_table(all_stats):
    """
    生成LaTeX格式的表格
    """
    latex_str = """
\\begin{table}[htbp]
\\centering
\\caption{蒙特卡洛模拟结果汇总}
\\begin{tabular}{lcccc}
\\toprule
场景 & 方法 & Bias & RMSE & Std \\\\
\\midrule
"""
    
    for scenario in ['A', 'B', 'C']:
        for method in ['basic_did', 'did_cov', 'psm', 'psm_did']:
            row = all_stats[scenario].loc[method]
            method_names = {
                'basic_did': '基础DID',
                'did_cov': '协变量DID',
                'psm': '纯PSM',
                'psm_did': 'PSM-DID'
            }
            latex_str += f"场景{scenario} & {method_names[method]} & {row['bias']:.4f} & {row['rmse']:.4f} & {row['std']:.4f} \\\\\n"
    
    latex_str += """
\\bottomrule
\\end{tabular}
\\end{table}
"""
    
    return latex_str
```

### 2. 生成总结报告

```python
def generate_summary_report(all_stats):
    """
    生成文本总结报告
    """
    report = []
    report.append("="*60)
    report.append("PSM-DID蒙特卡洛模拟总结报告")
    report.append("="*60)
    
    for scenario in ['A', 'B', 'C']:
        report.append(f"\n场景 {scenario}:")
        report.append("-"*40)
        
        # 找出每个场景下表现最好的方法
        best_bias_method = all_stats[scenario]['bias'].abs().idxmin()
        best_rmse_method = all_stats[scenario]['rmse'].idxmin()
        
        report.append(f"最小偏误方法: {best_bias_method} ({all_stats[scenario].loc[best_bias_method, 'bias']:.4f})")
        report.append(f"最小RMSE方法: {best_rmse_method} ({all_stats[scenario].loc[best_rmse_method, 'rmse']:.4f})")
        report.append(f"方法表现排序 (按RMSE):")
        
        # 按RMSE排序
        sorted_methods = all_stats[scenario].sort_values('rmse')
        for method, row in sorted_methods.iterrows():
            report.append(f"  {method}: RMSE={row['rmse']:.4f}, Bias={row['bias']:.4f}")
        
        # 理论解释
        if scenario == 'A':
            report.append("\n理论解释：满足无条件平行趋势，基础DID表现最佳")
        elif scenario == 'B':
            report.append("\n理论解释：趋势依赖X，PSM-DID通过匹配恢复平行趋势")
        elif scenario == 'C':
            report.append("\n理论解释：不可观测时间变化混淆导致所有方法失效")
        
        report.append("-"*40)
    
    # 整体结论
    report.append("\n" + "="*60)
    report.append("整体结论")
    report.append("="*60)
    report.append("1. PSM-DID在处理选择依赖可观测特征且趋势差异由这些特征驱动时表现最佳")
    report.append("2. 当存在不可观测的时间变化混淆时，PSM-DID无法解决问题")
    report.append("3. DID在处理组和控制组满足平行趋势假设时是最优选择")
    
    return "\n".join(report)
```

## 方向四：交互式分析功能

```python
def interactive_parameter_exploration():
    """
    交互式参数探索（适合Jupyter Notebook）
    """
    import ipywidgets as widgets
    from IPython.display import display
    
    # 创建交互控件
    scenario_dropdown = widgets.Dropdown(
        options=['A', 'B', 'C'],
        value='A',
        description='场景:'
    )
    
    N_slider = widgets.IntSlider(
        value=1000,
        min=100,
        max=5000,
        step=100,
        description='样本量:'
    )
    
    tau_slider = widgets.FloatSlider(
        value=1.0,
        min=-2.0,
        max=2.0,
        step=0.1,
        description='处理效应:'
    )
    
    def update_plot(scenario, N, tau):
        # 更新参数并重新运行
        params = {
            'tau': tau,
            'beta_x': 0.5,
            'alpha_sd': 1.0,
            'epsilon_sd': 0.5
        }
        
        df = generate_panel_data(N, scenario=scenario, params=params)
        results_df, stats_df, _ = monte_carlo_simulation(
            scenario=scenario, 
            N=N, 
            n_simulations=100
        )
        
        # 更新图表
        plot_results(results_df, stats_df, scenario)
    
    # 创建交互界面
    widgets.interactive(update_plot, 
                       scenario=scenario_dropdown, 
                       N=N_slider, 
                       tau=tau_slider)
```

请告诉我你想要深入哪个方向，或者是否有其他具体问题需要解答？比如：

1. **理论验证**：需要我解释特定场景下的模拟结果与理论预期的一致性？
2. **代码调试**：运行中发现错误或结果不符合预期？
3. **结果解读**：对生成的图表或统计量有疑问？
4. **代码定制**：需要修改某个参数或增加特定功能？




