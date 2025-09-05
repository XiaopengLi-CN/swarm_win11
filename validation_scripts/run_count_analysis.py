#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_count_analysis.py - 分析benchmark_baselines.py中的运行次数设置
"""

def analyze_run_count():
    """
    分析benchmark_baselines.py中的运行次数设置
    """
    print("=" * 80)
    print("🔍 benchmark_baselines.py 运行次数分析")
    print("=" * 80)
    
    print("\n📍 代码分析:")
    print("1. 第74行: algorithm(func, 5)")
    print("2. 第49行: for seed in range(n_reps)")
    print("3. 第50行: np.random.seed(int(seed))")
    
    print("\n🎯 运行次数设置:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 每个参数组合运行5次独立运行                            │")
    print("│ ├─ seed = 0, 1, 2, 3, 4                                │")
    print("│ ├─ 每次使用不同的随机种子                               │")
    print("│ ├─ 每次运行都是独立的优化过程                           │")
    print("│ └─ 总共5次独立运行                                     │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n📊 参数组合分析:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 函数ID: F20, F21, F22, F23, F24 (5个函数)              │")
    print("│ 实例ID: I1, I2, I3, ..., I10 (10个实例)               │")
    print("│ 维度: 10D (1个维度)                                    │")
    print("│ 算法: modcma_bipop (1个算法)                          │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 总参数组合数: 5 × 10 × 1 × 1 = 50个组合               │")
    print("│ 每个组合运行次数: 5次                                  │")
    print("│ 总运行次数: 50 × 5 = 250次独立运行                     │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🔍 具体运行流程:")
    print("对于每个参数组合 (algname, fid, iid, dim):")
    print("1. 创建IOH函数和日志器")
    print("2. 调用 algorithm(func, 5)")
    print("3. 在Algorithm_Evaluator中:")
    print("   - for seed in range(5):  # seed = 0, 1, 2, 3, 4")
    print("   - np.random.seed(int(seed))")
    print("   - 创建ModularCMAES优化器")
    print("   - c.run()  # 运行优化")
    print("   - func.reset()  # 重置函数状态")
    print("4. 关闭日志器")
    
    print("\n💡 运行次数的意义:")
    print("✅ 统计意义:")
    print("   - 5次独立运行提供统计可靠性")
    print("   - 可以计算平均值、标准差等统计量")
    print("   - 减少随机性对结果的影响")
    print("")
    print("✅ 算法评估:")
    print("   - 评估算法在不同随机种子下的表现")
    print("   - 测试算法的鲁棒性和稳定性")
    print("   - 提供更全面的性能评估")
    print("")
    print("✅ 结果分析:")
    print("   - 可以分析结果的分布特征")
    print("   - 识别异常值和离群点")
    print("   - 提供置信区间估计")
    
    print("\n📈 数据输出:")
    print("每次运行都会产生:")
    print("- 最佳适应度值 (fx)")
    print("- 评估次数 (budget)")
    print("- 运行时间")
    print("- 收敛信息")
    print("")
    print("最终数据包含:")
    print("- 50个参数组合")
    print("- 每个组合5次运行")
    print("- 总共250条记录")
    
    print("\n🔧 修改建议:")
    print("如果想改变运行次数:")
    print("1. 修改第74行: algorithm(func, n)  # n为想要的运行次数")
    print("2. 或者添加命令行参数控制运行次数")
    print("3. 注意: 运行次数越多，总运行时间越长")
    
    print("\n" + "=" * 80)
    print("总结: 每个参数组合运行5次独立运行，总共250次运行")
    print("=" * 80)

if __name__ == "__main__":
    analyze_run_count()
