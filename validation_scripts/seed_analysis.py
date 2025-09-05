#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_analysis.py - 分析随机种子作用的具体位置
详细解释种子是作用在BBOB函数还是BIPOP算法上
"""

import numpy as np
import ioh
from modcma import ModularCMAES

def analyze_seed_impact():
    """
    分析随机种子作用的具体位置
    """
    print("=" * 80)
    print("随机种子作用位置分析")
    print("=" * 80)
    
    print("\n🔍 代码执行流程分析:")
    print("1. benchmark_baselines.py 第50行: np.random.seed(int(seed))")
    print("2. 创建 ModularCMAES 优化器")
    print("3. 调用 c.run() 开始优化")
    print("4. ModularCMAES 内部使用随机数生成")
    print("5. IOH函数评估（通常无随机性）")
    
    print("\n📍 随机种子的具体作用位置:")
    
    print("\n1️⃣ BIPOP-CMA-ES算法内部 (主要作用)")
    print("   位置: ModularCMAES.run() 方法")
    print("   用途:")
    print("   - 生成初始种群")
    print("   - 生成变异向量")
    print("   - 选择操作")
    print("   - 重组操作")
    print("   - 步长调整")
    print("   - 重启机制")
    
    print("\n2️⃣ 边界处理 (次要作用)")
    print("   位置: bound_correction='saturate'")
    print("   用途:")
    print("   - 处理超出边界的解")
    print("   - 重新采样")
    
    print("\n3️⃣ 采样器初始化 (次要作用)")
    print("   位置: Sobol/Halton采样器")
    print("   用途:")
    print("   - 初始化准随机序列")
    
    print("\n❌ IOH/BBOB函数 (无随机性)")
    print("   位置: ioh.get_problem()")
    print("   说明:")
    print("   - BBOB函数是确定性的")
    print("   - 给定相同输入，总是产生相同输出")
    print("   - 函数本身不产生随机性")
    
    print("\n" + "=" * 80)

def demonstrate_seed_impact():
    """
    演示种子对算法的影响
    """
    print("\n🧪 种子影响演示:")
    
    fid = 20  # F20 (Schwefel)
    dim = 10
    iid = 1
    
    print(f"测试函数: F{fid}, 维度: {dim}D, 实例: I{iid}")
    
    # 测试1: 相同种子
    print("\n测试1: 使用相同种子 (42)")
    np.random.seed(42)
    func1 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c1 = ModularCMAES(func1, d=dim, bound_correction='saturate', budget=10000)
    c1.run()
    result1 = func1.state.current_best.y
    print(f"结果1: {result1:.6f}")
    func1.reset()
    
    np.random.seed(42)
    func2 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c2 = ModularCMAES(func2, d=dim, bound_correction='saturate', budget=10000)
    c2.run()
    result2 = func2.state.current_best.y
    print(f"结果2: {result2:.6f}")
    func2.reset()
    
    print(f"差异: {abs(result1 - result2):.10f}")
    if abs(result1 - result2) < 1e-10:
        print("✅ 相同种子产生相同结果")
    else:
        print("❌ 相同种子产生不同结果")
    
    # 测试2: 不同种子
    print("\n测试2: 使用不同种子")
    np.random.seed(100)
    func3 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c3 = ModularCMAES(func3, d=dim, bound_correction='saturate', budget=10000)
    c3.run()
    result3 = func3.state.current_best.y
    print(f"种子100结果: {result3:.6f}")
    func3.reset()
    
    print(f"种子42 vs 种子100差异: {abs(result1 - result3):.6f}")
    
    # 测试3: IOH函数确定性
    print("\n测试3: IOH函数确定性验证")
    func4 = ioh.get_problem(fid, dimension=dim, instance=iid)
    test_point = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0], [9.0], [10.0]])
    
    # 多次调用相同点
    result_a = func4(test_point)
    result_b = func4(test_point)
    result_c = func4(test_point)
    
    print(f"相同输入点多次调用:")
    print(f"  结果A: {result_a[0]:.6f}")
    print(f"  结果B: {result_b[0]:.6f}")
    print(f"  结果C: {result_c[0]:.6f}")
    
    if abs(result_a[0] - result_b[0]) < 1e-10 and abs(result_b[0] - result_c[0]) < 1e-10:
        print("✅ IOH函数是确定性的")
    else:
        print("❌ IOH函数有随机性")
    
    func4.reset()

def analyze_modcma_randomness():
    """
    分析ModularCMAES内部的随机性来源
    """
    print("\n🔬 ModularCMAES内部随机性分析:")
    
    print("\n随机数使用位置:")
    print("1. 初始种群生成 (parameters.py:478)")
    print("   - 使用 np.random.uniform() 生成初始解")
    print("   - 影响: 算法的起始点")
    
    print("\n2. 变异操作 (modularcmaes.py:73)")
    print("   - 使用 np.random.lognormal() 生成步长")
    print("   - 影响: 搜索步长和方向")
    
    print("\n3. 边界处理 (modularcmaes.py:414)")
    print("   - 使用 np.random.uniform() 重新采样")
    print("   - 影响: 边界约束处理")
    
    print("\n4. 重启机制 (parameters.py:900,924)")
    print("   - 使用 np.random.uniform() 调整参数")
    print("   - 影响: 重启时的参数设置")
    
    print("\n5. 采样器初始化 (sampling.py:48,63)")
    print("   - Sobol/Halton采样器使用随机种子")
    print("   - 影响: 准随机序列的起始点")

def explain_seed_scope():
    """
    解释种子的作用范围
    """
    print("\n📊 种子作用范围总结:")
    
    print("\n✅ 种子影响的部分:")
    print("1. BIPOP-CMA-ES算法的所有随机操作")
    print("2. 初始种群生成")
    print("3. 变异和重组操作")
    print("4. 步长调整")
    print("5. 重启机制")
    print("6. 边界处理")
    print("7. 采样器初始化")
    
    print("\n❌ 种子不影响的部分:")
    print("1. IOH/BBOB函数本身")
    print("2. 函数评估结果")
    print("3. 问题定义和约束")
    print("4. 算法参数设置")
    
    print("\n🎯 结论:")
    print("随机种子主要作用在BIPOP-CMA-ES算法上，")
    print("控制算法的随机搜索行为，")
    print("而不影响BBOB测试函数的确定性。")

if __name__ == "__main__":
    analyze_seed_impact()
    demonstrate_seed_impact()
    analyze_modcma_randomness()
    explain_seed_scope()
    
    print("\n" + "=" * 80)
    print("总结: 种子作用在BIPOP-CMA-ES算法上，控制优化过程的随机性")
    print("=" * 80)
