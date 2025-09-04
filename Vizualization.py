#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vizualization.py - 数据处理和可视化脚本（简化版）
从 FBUDGET_all.csv 处理得到 dt_fb.csv，并生成固定预算性能热图
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置matplotlib参数
font = {'size': 24}
plt.rc('font', **font)

# Font-requirement for GECCO
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# 创建Figures目录
if not os.path.exists('Figures'):
    os.makedirs('Figures')

def process_fbudget_data():
    """
    处理FBUDGET_all.csv数据，生成dt_fb.csv
    对应notebook中的Cell 12
    """
    print("正在处理固定预算数据...")
    
    # 读取FBUDGET_all.csv
    dt = pd.read_csv("CSV_Results/FBUDGET_all.csv")
    
    # 删除不需要的列
    dt = dt.drop(['fname', 'run', 'iid'], axis=1)
    
    # 对fx进行对数变换和裁剪
    dt['fx'] = np.log10(np.clip(dt['fx'], 1e-8, 1e16))
    
    # 添加库信息（根据algname判断）
    def get_lib(algname):
        if algname == 'modcma_bipop':
            return 'Baselines'
        elif algname in ['CS', 'DE']:
            return 'OPYTIMIZER'
        else:
            return 'Unknown'
    
    dt['lib'] = dt['algname'].apply(get_lib)
    
    # 按预算因子、算法名、函数ID、维度、库进行分组并计算平均值
    dt_fb = dt.groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean').reset_index()
    
    # 保存处理后的数据
    dt_fb.to_csv("dt_fb.csv", index=False)
    print(f"已保存 dt_fb.csv，包含 {len(dt_fb)} 行数据")
    
    return dt_fb

def make_heatmap_bests_simple(dim, dt_fb):
    """
    生成固定预算性能热图（简化版，只使用matplotlib）
    对应notebook中的Cell 40-41
    """
    print(f"正在生成 {dim}D 维度的固定预算性能热图...")
    
    # 对每个预算因子进行处理
    budget_factors = [10, 50, 100, 500, 1000, 5000, 10000]
    algorithms = ['modcma_bipop', 'CS', 'DE']
    
    # 创建结果矩阵
    result_matrix = np.zeros((len(budget_factors), len(algorithms)))
    
    for i, bfac in enumerate(budget_factors):
        for j, alg in enumerate(algorithms):
            # 筛选特定预算因子、维度、算法的数据
            data = dt_fb.query(f'budget_factor == {bfac} & dim == {dim} & algname == "{alg}"')
            if len(data) > 0:
                result_matrix[i, j] = data['fx'].iloc[0]
            else:
                result_matrix[i, j] = np.nan
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 创建热图
    im = ax.imshow(result_matrix, cmap='viridis', aspect='auto')
    
    # 设置坐标轴标签
    ax.set_xticks(range(len(algorithms)))
    ax.set_xticklabels(algorithms, rotation=45)
    ax.set_yticks(range(len(budget_factors)))
    ax.set_yticklabels(budget_factors)
    
    # 添加数值标注
    for i in range(len(budget_factors)):
        for j in range(len(algorithms)):
            if not np.isnan(result_matrix[i, j]):
                text = ax.text(j, i, f'{result_matrix[i, j]:.2f}',
                             ha="center", va="center", color="white", fontsize=12)
    
    # 设置标题和标签
    ax.set_title(f'Fixed Budget Performance - {dim}D (F1 Sphere)', fontsize=16)
    ax.set_xlabel('Algorithms', fontsize=14)
    ax.set_ylabel('Budget Factor', fontsize=14)
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('log10(fx)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f"Figures/Bests_budget_{dim}D_simple.pdf")
    print(f"已保存 Figures/Bests_budget_{dim}D_simple.pdf")
    plt.close()

def create_comparison_plot(dt_fb):
    """
    创建三个算法在不同预算因子下的性能比较图
    """
    print("正在生成算法性能比较图...")
    
    budget_factors = [10, 50, 100, 500, 1000, 5000, 10000]
    algorithms = ['modcma_bipop', 'CS', 'DE']
    colors = ['red', 'blue', 'green']
    
    plt.figure(figsize=(10, 6))  # 调整为单个图的尺寸
    
    for i, alg in enumerate(algorithms):
            performance = []
            for bfac in budget_factors:
                data = dt_fb.query(f'budget_factor == {bfac} & dim == 10 & algname == "{alg}"')
                if len(data) > 0:
                    performance.append(data['fx'].iloc[0])
                else:
                    performance.append(np.nan)
            
            plt.plot(budget_factors, performance, 'o-', color=colors[i], label=alg, linewidth=2, markersize=6)
        
            plt.xscale('log')
    plt.xlabel('Budget Factor')
    plt.title('10D Performance Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("Figures/Algorithm_comparison_10D.pdf")
    print("已保存 Figures/Algorithm_comparison_10D.pdf")
    plt.close()

def main():
    """
    主函数：处理数据并生成可视化
    """
    print("开始数据处理和可视化...")
    
    # 1. 处理固定预算数据
    dt_fb = process_fbudget_data()
    
    # 2. 生成10维度的固定预算性能热图
    make_heatmap_bests_simple(10, dt_fb)
    
    # 3. 不再生成其他维度的热图，只保留10维度
    # for dim in [2, 5, 20]:
    #     make_heatmap_bests_simple(dim, dt_fb)
    
    # 4. 创建算法性能比较图
    create_comparison_plot(dt_fb)
    
    print("数据处理和可视化完成！")
    print("生成的文件：")
    print("- dt_fb.csv: 处理后的固定预算数据")
    print("- Figures/Bests_budget_10D_simple.pdf: 10维度固定预算性能热图")
    print("- Figures/Algorithm_comparison_10D.pdf: 10维度算法性能比较图")

if __name__ == "__main__":
    main()
