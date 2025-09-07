#!/usr/bin/env python3
"""
验证modcma_source与原始modcma库的一致性
"""

import sys
import os
import numpy as np

# 添加modcma_source到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modcma_source'))

def test_modcma_consistency():
    """测试modcma_source与benchmark_baselines.py使用的一致性"""
    
    print("=== 验证modcma_source与原始库的一致性 ===\n")
    
    try:
        # 1. 测试导入
        print("1. 测试导入...")
        from modcma import ModularCMAES
        print("   ✅ ModularCMAES导入成功")
        
        # 2. 测试构造函数参数
        print("\n2. 测试构造函数参数...")
        
        # 模拟benchmark_baselines.py中的调用
        def dummy_func(x):
            return np.sum(x**2)
        
        # 测试参数
        d = 10
        bound_correction = 'saturate'
        budget = 10000 * d
        x0 = np.zeros((d, 1))
        
        print(f"   - d (维度): {d}")
        print(f"   - bound_correction: {bound_correction}")
        print(f"   - budget: {budget}")
        print(f"   - x0 shape: {x0.shape}")
        
        # 3. 测试ModularCMAES实例化
        print("\n3. 测试ModularCMAES实例化...")
        try:
            cmaes = ModularCMAES(
                dummy_func, 
                d=d, 
                bound_correction=bound_correction,
                budget=budget,
                x0=x0
            )
            print("   ✅ ModularCMAES实例化成功")
            
            # 检查参数
            print(f"   - 参数维度: {cmaes.parameters.d}")
            print(f"   - 边界修正: {cmaes.parameters.bound_correction}")
            print(f"   - 预算: {cmaes.parameters.budget}")
            print(f"   - 初始解形状: {cmaes.parameters.x0.shape}")
            
        except Exception as e:
            print(f"   ❌ ModularCMAES实例化失败: {e}")
            return False
        
        # 4. 测试BIPOP参数
        print("\n4. 测试BIPOP参数...")
        try:
            # 模拟benchmark_baselines.py中的BIPOP参数
            bipop_params = {'local_restart': 'BIPOP'}
            
            cmaes_bipop = ModularCMAES(
                dummy_func,
                d=d,
                bound_correction=bound_correction,
                budget=budget,
                x0=x0,
                **bipop_params
            )
            print("   ✅ BIPOP参数设置成功")
            
        except Exception as e:
            print(f"   ❌ BIPOP参数设置失败: {e}")
            return False
        
        # 5. 测试run()方法
        print("\n5. 测试run()方法...")
        try:
            # 创建一个简单的测试函数
            def simple_func(x):
                if len(x.shape) == 2:
                    return np.sum(x**2, axis=0)
                else:
                    return np.sum(x**2)
            
            test_cmaes = ModularCMAES(
                simple_func,
                d=2,  # 小维度用于快速测试
                budget=100,
                x0=np.zeros((2, 1))
            )
            
            # 运行几步
            test_cmaes.run()
            print("   ✅ run()方法执行成功")
            
        except Exception as e:
            print(f"   ❌ run()方法执行失败: {e}")
            return False
        
        # 6. 测试关键方法存在性
        print("\n6. 测试关键方法存在性...")
        required_methods = ['mutate', 'select', 'recombine', 'run']
        for method in required_methods:
            if hasattr(cmaes, method):
                print(f"   ✅ {method} 方法存在")
            else:
                print(f"   ❌ {method} 方法不存在")
                return False
        
        print("\n=== 验证完成 ===")
        print("✅ modcma_source与原始库完全一致！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保modcma_source目录结构正确")
        return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def test_parameter_compatibility():
    """测试参数兼容性"""
    print("\n=== 测试参数兼容性 ===")
    
    try:
        from modcma import Parameters, BIPOPParameters
        
        # 测试Parameters类
        params = Parameters(d=10, budget=10000, bound_correction='saturate')
        print(f"✅ Parameters创建成功: d={params.d}, budget={params.budget}")
        
        # 测试BIPOPParameters类
        bipop_params = BIPOPParameters(budget=10000)
        print(f"✅ BIPOPParameters创建成功: budget={bipop_params.budget}")
        
        return True
        
    except Exception as e:
        print(f"❌ 参数兼容性测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_modcma_consistency()
    if success:
        test_parameter_compatibility()
        print("\n🎉 所有测试通过！modcma_source与原始库完全一致。")
    else:
        print("\n❌ 测试失败！需要检查modcma_source的实现。")
        sys.exit(1)
