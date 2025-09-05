#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iid_impact_test.py - 测试不同实例ID对结果的影响
"""

import numpy as np
import ioh
from modcma import ModularCMAES

def test_iid_impact():
    """
    测试不同实例ID对优化结果的影响
    """
    print("=" * 80)
    print("🧪 测试不同实例ID对结果的影响")
    print("=" * 80)
    
    # 测试参数
    fid = 20  # F20 (Schwefel函数)
    dim = 10
    budget = 5000  # 较小的预算用于快速测试
    
    print(f"测试函数: F{fid}, 维度: {dim}D")
    print(f"预算: {budget}")
    print(f"随机种子: 固定为42")
    
    results = []
    
    # 测试不同的实例ID
    for iid in range(1, 6):  # 测试I1-I5
        print(f"\n测试实例I{iid}:")
        
        # 设置固定种子确保算法行为一致
        np.random.seed(42)
        
        # 创建函数
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        
        # 创建优化器
        c = ModularCMAES(
            func, 
            d=dim, 
            bound_correction='saturate',
            budget=budget,
            x0=np.zeros((dim, 1)),
            local_restart='BIPOP'
        )
        
        # 运行优化
        c.run()
        
        # 获取结果
        best_fitness = func.state.current_best.y
        evaluations = func.state.evaluations
        
        print(f"  最佳适应度: {best_fitness:.6f}")
        print(f"  评估次数: {evaluations}")
        
        results.append({
            'iid': iid,
            'best_fitness': best_fitness,
            'evaluations': evaluations
        })
        
        func.reset()
    
    # 分析结果
    print(f"\n📊 结果分析:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 实例ID │ 最佳适应度 │ 评估次数 │ 差异程度                │")
    print("├─────────────────────────────────────────────────────────┤")
    
    fitness_values = [r['best_fitness'] for r in results]
    min_fitness = min(fitness_values)
    max_fitness = max(fitness_values)
    fitness_range = max_fitness - min_fitness
    
    for r in results:
        diff_from_min = r['best_fitness'] - min_fitness
        print(f"│   I{r['iid']}   │ {r['best_fitness']:10.6f} │ {r['evaluations']:8d} │ {diff_from_min:8.6f}                │")
    
    print("└─────────────────────────────────────────────────────────┘")
    
    print(f"\n统计信息:")
    print(f"  适应度范围: {fitness_range:.6f}")
    print(f"  最小适应度: {min_fitness:.6f}")
    print(f"  最大适应度: {max_fitness:.6f}")
    print(f"  标准差: {np.std(fitness_values):.6f}")
    
    # 判断是否有显著差异
    if fitness_range > 1e-6:
        print(f"\n✅ 结论: 不同实例ID产生显著不同的结果")
        print(f"   差异范围: {fitness_range:.6f}")
        print(f"   说明实例变换确实影响了优化结果")
    else:
        print(f"\n❌ 结论: 不同实例ID产生相似的结果")
        print(f"   可能原因: 预算太小或函数特性")

def test_function_value_differences():
    """
    测试相同输入点在不同实例下的函数值差异
    """
    print(f"\n🔍 测试相同输入点在不同实例下的函数值:")
    
    fid = 20
    dim = 10
    
    # 测试点
    test_point = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], 
                           [6.0], [7.0], [8.0], [9.0], [10.0]])
    
    print(f"测试点: {test_point.flatten()}")
    print("\n不同实例的函数值:")
    
    values = []
    for iid in range(1, 6):
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        result = func(test_point)
        values.append(result[0])
        print(f"  实例I{iid}: {result[0]:.6f}")
        func.reset()
    
    # 分析函数值差异
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    print(f"\n函数值分析:")
    print(f"  最小值: {min_val:.6f}")
    print(f"  最大值: {max_val:.6f}")
    print(f"  范围: {range_val:.6f}")
    
    if range_val > 1e-6:
        print(f"✅ 不同实例对相同输入产生不同函数值")
        print(f"   说明实例变换确实改变了函数景观")
    else:
        print(f"❌ 不同实例对相同输入产生相似函数值")
        print(f"   可能原因: 测试点位置或函数特性")

def explain_iid_impact():
    """
    解释实例ID对结果的影响机制
    """
    print(f"\n💡 实例ID影响结果的机制:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 1. 函数景观变化                                        │")
    print("│    ├─ 最优解位置改变                                   │")
    print("│    ├─ 局部最优解分布改变                               │")
    print("│    ├─ 搜索路径有效性改变                                │")
    print("│    └─ 收敛难度改变                                     │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 2. 算法行为影响                                        │")
    print("│    ├─ 不同的起始搜索方向                                │")
    print("│    ├─ 不同的收敛路径                                   │")
    print("│    ├─ 不同的重启时机                                   │")
    print("│    └─ 不同的最终结果                                   │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 3. 统计意义                                            │")
    print("│    ├─ 提供更多样本点                                   │")
    print("│    ├─ 测试算法鲁棒性                                   │")
    print("│    ├─ 评估算法稳定性                                   │")
    print("│    └─ 减少偶然性影响                                   │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print(f"\n🎯 实际意义:")
    print("✅ 测试算法鲁棒性:")
    print("   - 验证算法对不同问题变体的适应性")
    print("   - 避免算法过拟合特定问题")
    print("   - 确保算法的通用性")
    print("")
    print("✅ 提供统计可靠性:")
    print("   - 10个实例提供更多样本")
    print("   - 可以计算平均值和标准差")
    print("   - 减少单次运行的偶然性")
    print("")
    print("✅ 符合标准做法:")
    print("   - BBOB基准测试的标准")
    print("   - 便于与其他算法比较")
    print("   - 提供公平的评估环境")

if __name__ == "__main__":
    test_iid_impact()
    test_function_value_differences()
    explain_iid_impact()
    
    print("\n" + "=" * 80)
    print("总结: 不同实例ID会产生不同的优化结果，这是BBOB测试的标准做法")
    print("=" * 80)
