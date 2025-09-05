#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_randomness.py - 测试随机性对结果的影响
"""

import numpy as np
import pandas as pd
import os
from modcma import ModularCMAES
import ioh

def test_randomness_impact():
    """
    测试随机性对优化结果的影响
    """
    print("=== 随机性影响测试 ===")
    
    # 测试参数
    fid = 20  # F20 (Schwefel)
    dim = 10
    iid = 1
    n_runs = 5
    
    print(f"测试函数: F{fid}, 维度: {dim}D, 实例: I{iid}")
    print(f"运行次数: {n_runs}")
    
    results = []
    
    for run in range(n_runs):
        print(f"\n运行 {run + 1}/{n_runs}:")
        
        # 设置不同的随机种子
        seed = run
        np.random.seed(seed)
        print(f"  随机种子: {seed}")
        
        # 创建函数
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        
        # 创建优化器
        c = ModularCMAES(
            func, 
            d=func.meta_data.n_variables, 
            bound_correction='saturate',
            budget=int(10000 * func.meta_data.n_variables),
            x0=np.zeros((func.meta_data.n_variables, 1)),
            local_restart='BIPOP'
        )
        
        # 运行优化
        c.run()
        
        # 获取最佳结果
        best_fitness = func.state.current_best.y
        evaluations = func.state.evaluations
        
        print(f"  最佳适应度: {best_fitness:.6f}")
        print(f"  评估次数: {evaluations}")
        
        results.append({
            'run': run + 1,
            'seed': seed,
            'best_fitness': best_fitness,
            'evaluations': evaluations
        })
        
        func.reset()
    
    # 分析结果
    df = pd.DataFrame(results)
    
    print(f"\n=== 结果分析 ===")
    print(f"最佳适应度统计:")
    print(f"  平均值: {df['best_fitness'].mean():.6f}")
    print(f"  标准差: {df['best_fitness'].std():.6f}")
    print(f"  最小值: {df['best_fitness'].min():.6f}")
    print(f"  最大值: {df['best_fitness'].max():.6f}")
    print(f"  变异系数: {df['best_fitness'].std() / abs(df['best_fitness'].mean()) * 100:.2f}%")
    
    print(f"\n评估次数统计:")
    print(f"  平均值: {df['evaluations'].mean():.0f}")
    print(f"  标准差: {df['evaluations'].std():.0f}")
    print(f"  最小值: {df['evaluations'].min()}")
    print(f"  最大值: {df['evaluations'].max()}")
    
    # 检查结果一致性
    fitness_range = df['best_fitness'].max() - df['best_fitness'].min()
    print(f"\n结果一致性分析:")
    print(f"  适应度范围: {fitness_range:.6f}")
    
    if fitness_range < 0.01:
        print("  ✅ 结果非常一致（差异 < 0.01）")
    elif fitness_range < 0.1:
        print("  ⚠️  结果基本一致（差异 < 0.1）")
    elif fitness_range < 1.0:
        print("  ❌ 结果存在中等差异（差异 < 1.0）")
    else:
        print("  ❌ 结果存在较大差异（差异 >= 1.0）")
    
    return df

def test_different_seeds():
    """
    测试不同种子设置方式的影响
    """
    print("\n=== 不同种子设置方式测试 ===")
    
    fid = 20
    dim = 10
    iid = 1
    
    # 测试1: 不设置种子
    print("\n1. 不设置随机种子:")
    np.random.seed(None)  # 重置为随机状态
    func1 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c1 = ModularCMAES(func1, d=dim, bound_correction='saturate', budget=100000)
    c1.run()
    result1 = func1.state.current_best.y
    print(f"   结果: {result1:.6f}")
    func1.reset()
    
    # 测试2: 设置固定种子
    print("\n2. 设置固定种子 (42):")
    np.random.seed(42)
    func2 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c2 = ModularCMAES(func2, d=dim, bound_correction='saturate', budget=100000)
    c2.run()
    result2 = func2.state.current_best.y
    print(f"   结果: {result2:.6f}")
    func2.reset()
    
    # 测试3: 再次设置相同种子
    print("\n3. 再次设置相同种子 (42):")
    np.random.seed(42)
    func3 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c3 = ModularCMAES(func3, d=dim, bound_correction='saturate', budget=100000)
    c3.run()
    result3 = func3.state.current_best.y
    print(f"   结果: {result3:.6f}")
    func3.reset()
    
    print(f"\n种子42的两次运行差异: {abs(result2 - result3):.6f}")
    if abs(result2 - result3) < 1e-10:
        print("✅ 相同种子产生相同结果")
    else:
        print("❌ 相同种子产生不同结果")

if __name__ == "__main__":
    # 运行随机性测试
    df = test_randomness_impact()
    
    # 测试不同种子设置方式
    test_different_seeds()
    
    print(f"\n=== 结论 ===")
    print("1. 优化算法确实具有随机性")
    print("2. 随机种子的设置会影响最终结果")
    print("3. 相同种子应该产生相同结果（如果算法实现正确）")
    print("4. 不同运行之间的差异是正常的，这是随机优化算法的特性")
