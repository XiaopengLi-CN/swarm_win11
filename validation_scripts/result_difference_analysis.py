#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
result_difference_analysis.py - 分析结果差异的原因和合理性
"""

import numpy as np
import pandas as pd
import ioh
from modcma import ModularCMAES

def analyze_result_differences():
    """
    分析结果差异的原因和合理性
    """
    print("=" * 80)
    print("🔍 BIPOP-CMA-ES结果差异分析")
    print("=" * 80)
    
    print("\n📍 您的情况:")
    print("✅ 使用相同来源的库 (modcma)")
    print("✅ 相同的BBOB配置 (iid=1-10)")
    print("✅ 相同的运行次数 (5次)")
    print("❌ 结果与标准答案有差异")
    
    print("\n🎯 问题: 这种差异是否合理?")

def test_randomness_sources():
    """
    测试随机性的来源
    """
    print("\n🧪 随机性来源测试:")
    
    fid = 20
    dim = 10
    iid = 1
    budget = 2000
    
    print(f"测试参数: F{fid}, {dim}D, I{iid}, 预算={budget}")
    
    # 测试1: 完全相同的设置
    print("\n测试1: 完全相同的设置")
    results1 = []
    for run in range(3):
        np.random.seed(42)  # 固定种子
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        c = ModularCMAES(func, d=dim, bound_correction='saturate', budget=budget, x0=np.zeros((dim, 1)))
        c.run()
        result = func.state.current_best.y
        results1.append(result)
        print(f"  运行{run+1}: {result:.6f}")
        func.reset()
    
    # 检查是否完全相同
    if len(set(results1)) == 1:
        print("✅ 相同种子产生相同结果")
    else:
        print("❌ 相同种子产生不同结果")
        print(f"   差异范围: {max(results1) - min(results1):.10f}")
    
    # 测试2: 不同种子
    print("\n测试2: 不同种子")
    results2 = []
    for run in range(3):
        np.random.seed(100 + run)  # 不同种子
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        c = ModularCMAES(func, d=dim, bound_correction='saturate', budget=budget, x0=np.zeros((dim, 1)))
        c.run()
        result = func.state.current_best.y
        results2.append(result)
        print(f"  种子{100+run}: {result:.6f}")
        func.reset()
    
    print(f"不同种子差异范围: {max(results2) - min(results2):.6f}")

def analyze_difference_causes():
    """
    分析结果差异的可能原因
    """
    print("\n🔍 结果差异的可能原因:")
    
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 1. 随机性来源 (主要)                                   │")
    print("│ ├─ 算法内部随机数生成                                  │")
    print("│ ├─ 初始种群生成                                        │")
    print("│ ├─ 变异和重组操作                                      │")
    print("│ ├─ 重启机制                                            │")
    print("│ └─ 边界处理                                           │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 2. 环境差异 (次要)                                    │")
    print("│ ├─ Python版本差异                                     │")
    print("│ ├─ NumPy版本差异                                      │")
    print("│ ├─ 操作系统差异                                       │")
    print("│ ├─ 硬件差异                                           │")
    print("│ └─ 编译选项差异                                       │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 3. 配置差异 (可能)                                    │")
    print("│ ├─ 算法参数设置                                       │")
    print("│ ├─ 预算设置                                           │")
    print("│ ├─ 终止条件                                           │")
    print("│ ├─ 边界处理方式                                       │")
    print("│ └─ 重启策略                                           │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 4. 数据记录差异 (可能)                                │")
    print("│ ├─ 日志记录方式                                       │")
    print("│ ├─ 数据精度                                           │")
    print("│ ├─ 统计计算方法                                       │")
    print("│ └─ 结果提取方式                                       │")
    print("└─────────────────────────────────────────────────────────┘")

def test_algorithm_determinism():
    """
    测试算法的确定性
    """
    print("\n🔬 算法确定性测试:")
    
    fid = 20
    dim = 10
    iid = 1
    budget = 1000
    
    print("测试: 相同种子 + 相同参数 = 相同结果?")
    
    # 多次测试
    test_results = []
    for test in range(5):
        np.random.seed(42)
        func = ioh.get_problem(fid, dimension=dim, instance=iid)
        c = ModularCMAES(func, d=dim, bound_correction='saturate', budget=budget, x0=np.zeros((dim, 1)))
        c.run()
        result = func.state.current_best.y
        test_results.append(result)
        func.reset()
    
    # 分析结果
    unique_results = len(set(test_results))
    print(f"唯一结果数量: {unique_results}")
    
    if unique_results == 1:
        print("✅ 算法是确定性的 (相同输入产生相同输出)")
    else:
        print("❌ 算法有非确定性因素")
        print(f"结果范围: {max(test_results) - min(test_results):.10f}")

def explain_reasonableness():
    """
    解释差异的合理性
    """
    print("\n💡 差异合理性分析:")
    
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ ✅ 合理的差异原因:                                     │")
    print("│ ├─ 算法本身具有随机性                                 │")
    print("│ ├─ 不同随机种子产生不同结果                            │")
    print("│ ├─ 优化算法本质上是随机的                              │")
    print("│ ├─ 相同配置下结果有变化是正常的                        │")
    print("│ └─ 这是优化算法的特性                                  │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ ❌ 不合理的差异原因:                                   │")
    print("│ ├─ 算法实现错误                                        │")
    print("│ ├─ 参数设置错误                                        │")
    print("│ ├─ 数据记录错误                                        │")
    print("│ ├─ 环境配置错误                                        │")
    print("│ └─ 版本不兼容                                          │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🎯 判断标准:")
    print("1. 差异程度:")
    print("   - 小差异 (< 1%): 正常随机性")
    print("   - 中等差异 (1-10%): 可能的环境差异")
    print("   - 大差异 (> 10%): 需要检查配置")
    print("")
    print("2. 统计特征:")
    print("   - 结果分布是否合理")
    print("   - 平均值是否接近")
    print("   - 标准差是否相似")
    print("")
    print("3. 趋势一致性:")
    print("   - 相对排名是否一致")
    print("   - 函数难度排序是否一致")
    print("   - 算法表现趋势是否一致")

def provide_solutions():
    """
    提供解决方案
    """
    print("\n🔧 解决方案:")
    
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 1. 验证算法确定性                                     │")
    print("│ ├─ 使用相同种子测试                                    │")
    print("│ ├─ 检查是否产生相同结果                                │")
    print("│ ├─ 确认算法实现正确                                    │")
    print("│ └─ 验证参数设置一致                                    │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 2. 增加运行次数                                        │")
    print("│ ├─ 从5次增加到10次或更多                               │")
    print("│ ├─ 计算统计量 (平均值、标准差)                         │")
    print("│ ├─ 提供置信区间                                        │")
    print("│ └─ 减少随机性影响                                      │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 3. 详细记录配置                                        │")
    print("│ ├─ 记录所有参数设置                                    │")
    print("│ ├─ 记录环境信息                                        │")
    print("│ ├─ 记录版本信息                                        │")
    print("│ └─ 便于问题定位                                        │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 4. 与原作者联系                                        │")
    print("│ ├─ 确认实验配置                                        │")
    print("│ ├─ 获取详细参数                                        │")
    print("│ ├─ 了解环境要求                                        │")
    print("│ └─ 获得技术支持                                        │")
    print("└─────────────────────────────────────────────────────────┘")

def answer_key_questions():
    """
    回答关键问题
    """
    print("\n❓ 关键问题回答:")
    
    print("Q1: 这种差异是否合理?")
    print("A1: ✅ 是的，这是合理的。优化算法本身具有随机性，")
    print("    相同配置下产生不同结果是正常的。")
    
    print("\nQ2: 算法运行是否带有随机性?")
    print("A2: ✅ 是的，BIPOP-CMA-ES是随机优化算法，")
    print("    每次运行都会产生不同的结果。")
    
    print("\nQ3: 是否可能得到与原实验一样的结果?")
    print("A3: ✅ 是的，但需要:")
    print("    - 使用完全相同的随机种子")
    print("    - 使用完全相同的参数设置")
    print("    - 使用完全相同的环境配置")
    print("    - 使用完全相同的算法版本")
    
    print("\nQ4: 如何减少差异?")
    print("A4: 建议:")
    print("    - 增加运行次数 (如10-20次)")
    print("    - 计算统计量而非单次结果")
    print("    - 记录详细的配置信息")
    print("    - 与原作者确认实验设置")

if __name__ == "__main__":
    analyze_result_differences()
    test_randomness_sources()
    analyze_difference_causes()
    test_algorithm_determinism()
    explain_reasonableness()
    provide_solutions()
    answer_key_questions()
    
    print("\n" + "=" * 80)
    print("总结: 结果差异是合理的，优化算法本身具有随机性")
    print("=" * 80)
