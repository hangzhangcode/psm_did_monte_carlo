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
