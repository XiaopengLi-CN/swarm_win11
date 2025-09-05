#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bipop_seed_analysis.py - 分析BIPOP-CMA-ES算法的默认随机种子设置
"""

import numpy as np
from modcma import ModularCMAES
import ioh

def analyze_bipop_default_seed():
    """
    分析BIPOP-CMA-ES算法的默认随机种子设置
    """
    print("=" * 80)
    print("🔍 BIPOP-CMA-ES算法默认随机种子分析")
    print("=" * 80)
    
    print("\n📍 代码分析结果:")
    
    print("\n1️⃣ ModularCMAES构造函数:")
    print("   位置: modcma_source/modularcmaes.py:37-46")
    print("   代码:")
    print("   ```python")
    print("   def __init__(self, fitness_func: Callable, *args, parameters=None, **kwargs):")
    print("       self._fitness_func = fitness_func")
    print("       self.parameters = (")
    print("           parameters")
    print("           if isinstance(parameters, Parameters)")
    print("           else Parameters(*args, **kwargs)")
    print("       )")
    print("   ```")
    print("   说明: 构造函数本身不设置种子，而是创建Parameters对象")
    
    print("\n2️⃣ Parameters类:")
    print("   位置: modcma_source/parameters.py:306-313")
    print("   代码:")
    print("   ```python")
    print("   def __init__(self, *args, **kwargs) -> None:")
    print("       super().__init__(*args, **kwargs)")
    print("       self.init_selection_parameters()")
    print("       self.init_fixed_parameters()")
    print("       self.init_adaptation_parameters()")
    print("       self.init_dynamic_parameters()")
    print("       self.init_local_restart_parameters()")
    print("   ```")
    print("   说明: Parameters类没有seed字段，不设置默认种子")
    
    print("\n3️⃣ evaluate_bbob函数:")
    print("   位置: modcma_source/modularcmaes.py:432-480")
    print("   代码:")
    print("   ```python")
    print("   def evaluate_bbob(")
    print("       fid: int,")
    print("       dim: int,")
    print("       iterations: int = 50,")
    print("       label: str = '',")
    print("       logging: bool = False,")
    print("       data_folder: str = None,")
    print("       seed: int = 42,  # 默认种子")
    print("       instance: int = 1,")
    print("       target_precision: float = 1e-8,")
    print("       return_optimizer: bool = False,")
    print("       **kwargs,")
    print("   ):")
    print("   ```")
    print("   说明: evaluate_bbob函数有默认种子42")
    
    print("\n4️⃣ __main__.py:")
    print("   位置: modcma_source/__main__.py:27")
    print("   代码:")
    print("   ```python")
    print("   parser.add_argument('-s', '--seed', type=int, required=False, default=42)")
    print("   ```")
    print("   说明: 命令行接口默认种子也是42")
    
    print("\n5️⃣ 种子设置逻辑:")
    print("   位置: modcma_source/modularcmaes.py:479-480")
    print("   代码:")
    print("   ```python")
    print("   if seed:")
    print("       np.random.seed(seed)")
    print("   ```")
    print("   说明: 只有当seed不为None/0时才设置种子")
    
    print("\n" + "=" * 80)

def test_default_seed_behavior():
    """
    测试默认种子行为
    """
    print("\n🧪 默认种子行为测试:")
    
    fid = 20
    dim = 10
    iid = 1
    
    print(f"测试函数: F{fid}, 维度: {dim}D, 实例: I{iid}")
    
    # 测试1: 不设置种子（使用NumPy默认行为）
    print("\n测试1: 不设置任何种子 - 快速测试")
    np.random.seed(None)  # 重置为随机状态
    
    func1 = ioh.get_problem(fid, dimension=dim, instance=iid)
    c1 = ModularCMAES(func1, d=dim, bound_correction='saturate', budget=1000)  # 减少预算
    c1.run()
    result1 = func1.state.current_best.y
    print(f"结果1: {result1:.6f}")
    func1.reset()
    
    # 测试2: 使用evaluate_bbob的默认种子（快速测试）
    print("\n测试2: 使用evaluate_bbob默认种子(42) - 快速测试")
    from modcma.modularcmaes import evaluate_bbob
    
    # 注意：evaluate_bbob会设置种子42，使用较少迭代次数
    result2 = evaluate_bbob(fid=fid, dim=dim, iterations=10, seed=42)
    print(f"结果2: {result2}")  # 先看看返回什么类型
    print(f"结果2类型: {type(result2)}")
    
    # 测试3: 再次使用相同种子
    print("\n测试3: 再次使用相同种子(42)")
    result3 = evaluate_bbob(fid=fid, dim=dim, iterations=10, seed=42)
    print(f"结果3: {result3}")
    print(f"结果3类型: {type(result3)}")
    
    # 比较结果
    if isinstance(result2, (tuple, list)) and isinstance(result3, (tuple, list)):
        # 比较第一个数组（评估次数）
        diff_evaluations = np.abs(result2[0] - result3[0]).max()
        # 比较第二个数组（适应度值）
        diff_fitness = np.abs(result2[1] - result3[1]).max()
        
        print(f"\n种子42的两次运行差异:")
        print(f"  评估次数最大差异: {diff_evaluations:.10f}")
        print(f"  适应度值最大差异: {diff_fitness:.10f}")
        
        if diff_evaluations < 1e-10 and diff_fitness < 1e-10:
            print("✅ 相同种子产生相同结果")
        else:
            print("❌ 相同种子产生不同结果")
    else:
        print(f"\n种子42的两次运行差异: {abs(result2 - result3):.10f}")
        if abs(result2 - result3) < 1e-10:
            print("✅ 相同种子产生相同结果")
        else:
            print("❌ 相同种子产生不同结果")

def analyze_sampling_seeds():
    """
    分析采样器的种子设置
    """
    print("\n🔬 采样器种子分析:")
    
    print("\n1️⃣ Sobol采样器:")
    print("   位置: modcma_source/sampling.py:48")
    print("   代码:")
    print("   ```python")
    print("   super().__init__(stats.qmc.Sobol(d, seed=np.random.randint(1e9)))")
    print("   ```")
    print("   说明: 使用np.random.randint(1e9)生成随机种子")
    
    print("\n2️⃣ Halton采样器:")
    print("   位置: modcma_source/sampling.py:63")
    print("   代码:")
    print("   ```python")
    print("   super().__init__(stats.qmc.Halton(d, seed=np.random.randint(1e9)))")
    print("   ```")
    print("   说明: 使用np.random.randint(1e9)生成随机种子")
    
    print("\n3️⃣ 默认采样器:")
    print("   位置: modcma_source/parameters.py:271")
    print("   代码:")
    print("   ```python")
    print("   base_sampler: ('gaussian', 'sobol', 'halton') = 'gaussian'")
    print("   ```")
    print("   说明: 默认使用高斯采样器，不需要种子")

def explain_default_seed_mechanism():
    """
    解释默认种子机制
    """
    print("\n📊 默认种子机制总结:")
    
    print("\n🎯 关键发现:")
    print("1. ModularCMAES构造函数本身不设置种子")
    print("2. Parameters类没有seed字段")
    print("3. evaluate_bbob函数默认种子是42")
    print("4. 命令行接口默认种子也是42")
    print("5. 采样器使用np.random.randint(1e9)生成种子")
    
    print("\n🔍 默认行为分析:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 情况1: 直接创建ModularCMAES                            │")
    print("│ ├─ 不设置任何种子                                       │")
    print("│ ├─ 使用NumPy的默认随机状态                             │")
    print("│ └─ 结果不可重复                                         │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 情况2: 使用evaluate_bbob函数                          │")
    print("│ ├─ 默认种子42                                          │")
    print("│ ├─ 结果可重复                                           │")
    print("│ └─ 可以通过seed参数修改                                │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 情况3: 手动设置np.random.seed()                        │")
    print("│ ├─ 在创建ModularCMAES之前设置                          │")
    print("│ ├─ 影响所有后续的随机数生成                            │")
    print("│ └─ 结果可重复                                           │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n💡 实际应用建议:")
    print("1. 如果使用evaluate_bbob函数，默认种子是42")
    print("2. 如果直接创建ModularCMAES，需要手动设置种子")
    print("3. 采样器会自动生成随机种子")
    print("4. 建议总是显式设置种子以确保可重复性")

if __name__ == "__main__":
    analyze_bipop_default_seed()
    test_default_seed_behavior()
    analyze_sampling_seeds()
    explain_default_seed_mechanism()
    
    print("\n" + "=" * 80)
    print("总结: BIPOP-CMA-ES默认种子机制分析完成")
    print("=" * 80)
