#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_fitness.py - 比较Java和Python版本的fitness值
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_java_fitness_from_log():
    """
    从Java运行日志中提取fitness值
    """
    # 从之前的运行日志中提取的Java版本fitness值
    java_fitness = {
        'I1': [0.234502],  # 从日志中提取的最终fitness值
        'I2': [0.158281],
        'I3': [0.099057],
        'I4': [0.127581],
        'I5': [0.122116],
        'I6': [0.104730],
        'I7': [0.121538],
        'I8': [0.236991],
        'I9': [0.171855],
        'I10': [0.134648]
    }
    return java_fitness

def extract_python_fitness_from_dat():
    """
    从Python版本的.dat文件中提取最终fitness值
    """
    python_fitness = {}
    
    for i in range(1, 11):
        instance = f'I{i}'
        dat_file = f'Data/Baselines/modcma_bipop_F1_I{i}_10D/data_f1_Sphere/IOHprofiler_f1_DIM10.dat'
        
        if os.path.exists(dat_file):
            # 读取最后一行获取最终fitness值
            with open(dat_file, 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:  # 跳过标题行
                    last_line = lines[-1].strip()
                    parts = last_line.split()
                    if len(parts) >= 2:
                        final_fitness = float(parts[1])
                        python_fitness[instance] = [final_fitness]
                    else:
                        python_fitness[instance] = [np.nan]
                else:
                    python_fitness[instance] = [np.nan]
        else:
            python_fitness[instance] = [np.nan]
    
    return python_fitness

def create_comparison_table():
    """
    创建对比表格
    """
    java_fitness = extract_java_fitness_from_log()
    python_fitness = extract_python_fitness_from_dat()
    
    # 创建对比数据框
    comparison_data = []
    instances = [f'I{i}' for i in range(1, 11)]
    
    for instance in instances:
        java_val = java_fitness.get(instance, [np.nan])[0]
        python_val = python_fitness.get(instance, [np.nan])[0]
        
        comparison_data.append({
            'Instance': instance,
            'Java_Fitness': java_val,
            'Python_Fitness': python_val,
            'Difference': java_val - python_val if not (np.isnan(java_val) or np.isnan(python_val)) else np.nan,
            'Relative_Diff_%': ((java_val - python_val) / python_val * 100) if not (np.isnan(java_val) or np.isnan(python_val) or python_val == 0) else np.nan
        })
    
    df = pd.DataFrame(comparison_data)
    return df

def analyze_results():
    """
    分析结果
    """
    print("=== Java vs Python Fitness值对比分析 ===\n")
    
    df = create_comparison_table()
    print(df.to_string(index=False, float_format='%.6f'))
    
    print("\n=== 统计分析 ===")
    
    # 计算统计信息
    java_vals = df['Java_Fitness'].dropna()
    python_vals = df['Python_Fitness'].dropna()
    differences = df['Difference'].dropna()
    
    if len(java_vals) > 0 and len(python_vals) > 0:
        print(f"Java版本平均fitness: {java_vals.mean():.6f}")
        print(f"Python版本平均fitness: {python_vals.mean():.6f}")
        print(f"平均差异: {differences.mean():.6f}")
        print(f"差异标准差: {differences.std():.6f}")
        print(f"最大差异: {differences.max():.6f}")
        print(f"最小差异: {differences.min():.6f}")
        
        # 性能评估
        better_java = len(differences[differences < 0])
        better_python = len(differences[differences > 0])
        equal = len(differences[differences == 0])
        
        print(f"\n=== 性能对比 ===")
        print(f"Java版本表现更好: {better_java}个实例")
        print(f"Python版本表现更好: {better_python}个实例")
        print(f"表现相同: {equal}个实例")
        
        if better_java > better_python:
            print("结论: Java版本整体表现更好")
        elif better_python > better_java:
            print("结论: Python版本整体表现更好")
        else:
            print("结论: 两个版本表现相当")
    
    return df

def plot_comparison(df):
    """
    绘制对比图表
    """
    plt.figure(figsize=(12, 8))
    
    # 创建子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # 第一个子图：fitness值对比
    instances = df['Instance'].tolist()
    java_vals = df['Java_Fitness'].tolist()
    python_vals = df['Python_Fitness'].tolist()
    
    x = np.arange(len(instances))
    width = 0.35
    
    ax1.bar(x - width/2, java_vals, width, label='Java版本', alpha=0.8)
    ax1.bar(x + width/2, python_vals, width, label='Python版本', alpha=0.8)
    
    ax1.set_xlabel('实例')
    ax1.set_ylabel('Fitness值')
    ax1.set_title('Java vs Python版本Fitness值对比')
    ax1.set_xticks(x)
    ax1.set_xticklabels(instances)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 第二个子图：差异分析
    differences = df['Difference'].tolist()
    colors = ['red' if d > 0 else 'green' if d < 0 else 'blue' for d in differences]
    
    ax2.bar(instances, differences, color=colors, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax2.set_xlabel('实例')
    ax2.set_ylabel('差异 (Java - Python)')
    ax2.set_title('Fitness值差异分析 (正值表示Java更好)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fitness_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    主函数
    """
    print("开始分析Java和Python版本的fitness值...")
    
    # 分析结果
    df = analyze_results()
    
    # 保存结果到CSV
    df.to_csv('fitness_comparison.csv', index=False)
    print(f"\n结果已保存到: fitness_comparison.csv")
    
    # 绘制图表
    try:
        plot_comparison(df)
        print("图表已保存到: fitness_comparison.png")
    except Exception as e:
        print(f"绘制图表时出错: {e}")
    
    print("\n分析完成！")

if __name__ == "__main__":
    main()
