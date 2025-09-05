#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instance_explanation.py - 解释BBOB函数实例的含义
"""

import ioh
import numpy as np

def explain_bbob_instances():
    """
    解释BBOB函数实例的含义
    """
    print("=" * 80)
    print("🔍 BBOB函数实例(Instance)详细解释")
    print("=" * 80)
    
    print("\n📍 代码中的设置:")
    print("第84行: iids = range(1,11)  # 测试I1-I10，共10个实例")
    print("说明: 每个函数有10个不同的实例")
    
    print("\n🎯 什么是BBOB函数实例?")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ BBOB函数实例是同一个函数的变体                        │")
    print("│ ├─ 相同的函数类型 (如F20 Schwefel函数)                │")
    print("│ ├─ 相同的维度 (如10D)                                  │")
    print("│ ├─ 相同的搜索空间范围                                  │")
    print("│ ├─ 相同的全局最优值 (通常为0)                          │")
    print("│ ├─ 不同的变换参数 (旋转、缩放、平移等)                 │")
    print("│ └─ 不同的局部最优解分布                                │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🔍 实例的作用:")
    print("✅ 测试算法鲁棒性:")
    print("   - 同一函数的不同变换")
    print("   - 验证算法对不同问题变体的适应性")
    print("   - 避免算法过拟合特定问题")
    print("")
    print("✅ 提供统计可靠性:")
    print("   - 10个实例提供更多样本")
    print("   - 可以计算平均值和标准差")
    print("   - 减少单次运行的偶然性")
    print("")
    print("✅ 符合BBOB标准:")
    print("   - BBOB基准测试的标准做法")
    print("   - 便于与其他算法比较")
    print("   - 提供公平的评估环境")

def demonstrate_instances():
    """
    演示不同实例的差异
    """
    print("\n🧪 实例差异演示:")
    
    fid = 20  # F20 (Schwefel函数)
    dim = 10
    
    print(f"测试函数: F{fid}, 维度: {dim}D")
    print("比较不同实例的差异:")
    
    # 测试点
    test_point = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], 
                           [6.0], [7.0], [8.0], [9.0], [10.0]])
    
    print(f"\n测试点: {test_point.flatten()}")
    print("\n不同实例的函数值:")
    
    for iid in range(1, 6):  # 只测试前5个实例
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        result = func(test_point)
        print(f"  实例I{iid}: {result[0]:.6f}")
        func.reset()
    
    print("\n观察:")
    print("- 相同输入点在不同实例下产生不同函数值")
    print("- 这说明实例确实有不同的变换参数")
    print("- 但函数的基本性质保持不变")

def explain_instance_generation():
    """
    解释实例生成机制
    """
    print("\n🔬 实例生成机制:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ BBOB实例通过以下变换生成:                               │")
    print("│ ├─ 坐标旋转: 改变坐标轴方向                            │")
    print("│ ├─ 坐标缩放: 改变搜索空间形状                          │")
    print("│ ├─ 坐标平移: 改变最优解位置                            │")
    print("│ ├─ 函数缩放: 改变函数值范围                            │")
    print("│ └─ 噪声添加: 增加问题难度                              │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n📊 实例特点:")
    print("✅ 保持不变的:")
    print("   - 函数类型和基本性质")
    print("   - 全局最优值")
    print("   - 搜索空间维度")
    print("   - 问题难度级别")
    print("")
    print("✅ 发生变化的:")
    print("   - 最优解的具体位置")
    print("   - 局部最优解分布")
    print("   - 函数景观的形状")
    print("   - 搜索路径的有效性")

def explain_testing_significance():
    """
    解释测试意义
    """
    print("\n💡 测试10个实例的意义:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 1. 算法鲁棒性测试                                       │")
    print("│    ├─ 验证算法对不同问题变体的适应性                   │")
    print("│    ├─ 避免算法过拟合特定问题                           │")
    print("│    └─ 确保算法的通用性                                 │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 2. 统计可靠性                                          │")
    print("│    ├─ 10个实例提供足够样本                             │")
    print("│    ├─ 可以计算平均值、标准差、置信区间                 │")
    print("│    └─ 减少单次运行的偶然性                             │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 3. 标准比较                                            │")
    print("│    ├─ 符合BBOB基准测试标准                             │")
    print("│    ├─ 便于与其他算法比较                               │")
    print("│    └─ 提供公平的评估环境                                │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 4. 全面评估                                            │")
    print("│    ├─ 覆盖函数的不同变体                               │")
    print("│    ├─ 测试算法的不同方面                               │")
    print("│    └─ 提供更全面的性能评估                             │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n📈 实际测试流程:")
    print("对于每个函数F20-F24:")
    print("1. 测试10个实例 (I1-I10)")
    print("2. 每个实例运行5次 (不同随机种子)")
    print("3. 总共50次运行")
    print("4. 计算统计量 (平均值、标准差等)")
    print("5. 评估算法在该函数上的整体表现")

if __name__ == "__main__":
    explain_bbob_instances()
    demonstrate_instances()
    explain_instance_generation()
    explain_testing_significance()
    
    print("\n" + "=" * 80)
    print("总结: 10个实例是同一函数的10个不同变体，用于测试算法鲁棒性")
    print("=" * 80)
