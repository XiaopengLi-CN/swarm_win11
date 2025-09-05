#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deep_seed_analysis.py - 深入分析NumPy默认种子机制
"""

import numpy as np
import os
import time
import subprocess

def analyze_numpy_seed_mechanism():
    """
    深入分析NumPy的种子机制
    """
    print("=== NumPy种子机制深度分析 ===")
    
    # 1. 检查NumPy版本和随机数生成器
    print(f"\n1. NumPy版本信息:")
    print(f"   NumPy版本: {np.__version__}")
    print(f"   随机数生成器类型: {type(np.random.mtrand._rand)}")
    
    # 2. 检查默认种子的来源
    print(f"\n2. 默认种子分析:")
    
    # 获取当前状态
    current_state = np.random.get_state()
    print(f"   当前状态数组第一个值: {current_state[1][0]}")
    print(f"   当前状态数组第二个值: {current_state[1][1]}")
    
    # 3. 测试不同情况下的种子行为
    print(f"\n3. 不同种子设置测试:")
    
    # 测试1: 不设置种子
    print("   测试1 - 不设置种子:")
    np.random.seed(None)
    rand1 = np.random.random()
    print(f"     随机数: {rand1}")
    
    # 测试2: 设置固定种子
    print("   测试2 - 设置固定种子(123):")
    np.random.seed(123)
    rand2 = np.random.random()
    print(f"     随机数: {rand2}")
    
    # 测试3: 再次设置相同种子
    print("   测试3 - 再次设置相同种子(123):")
    np.random.seed(123)
    rand3 = np.random.random()
    print(f"     随机数: {rand3}")
    print(f"     是否相同: {rand2 == rand3}")
    
    # 测试4: 使用时间戳作为种子
    print("   测试4 - 使用时间戳作为种子:")
    time_seed = int(time.time())
    np.random.seed(time_seed)
    rand4 = np.random.random()
    print(f"     时间种子: {time_seed}")
    print(f"     随机数: {rand4}")
    
    # 测试5: 使用进程ID作为种子
    print("   测试5 - 使用进程ID作为种子:")
    pid_seed = os.getpid()
    np.random.seed(pid_seed)
    rand5 = np.random.random()
    print(f"     进程ID种子: {pid_seed}")
    print(f"     随机数: {rand5}")

def test_multiple_sessions():
    """
    测试多个Python会话的随机性
    """
    print(f"\n=== 多会话随机性测试 ===")
    
    # 创建多个独立的Python进程
    print("创建多个独立的Python进程测试随机性...")
    
    for i in range(3):
        print(f"\n会话 {i+1}:")
        
        # 创建Python脚本内容
        script_content = f"""
import numpy as np
import time
import os

print(f"进程ID: {{os.getpid()}}")
print(f"时间戳: {{int(time.time())}}")

# 不设置种子
np.random.seed(None)
rand1 = np.random.random()
print(f"不设置种子的随机数: {{rand1}}")

# 设置固定种子
np.random.seed(42)
rand2 = np.random.random()
print(f"固定种子42的随机数: {{rand2}}")

# 再次设置相同种子
np.random.seed(42)
rand3 = np.random.random()
print(f"再次设置种子42的随机数: {{rand3}}")
print(f"固定种子结果是否相同: {{rand2 == rand3}}")
"""
        
        # 写入临时脚本
        script_file = f"temp_session_{i}.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        try:
            # 运行脚本
            result = subprocess.run(['python', script_file], 
                                  capture_output=True, text=True, timeout=10)
            print(result.stdout)
            if result.stderr:
                print(f"错误: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("脚本执行超时")
        except Exception as e:
            print(f"执行错误: {e}")
        finally:
            # 清理临时文件
            try:
                os.remove(script_file)
            except:
                pass

def test_numpy_internals():
    """
    测试NumPy内部机制
    """
    print(f"\n=== NumPy内部机制测试 ===")
    
    # 1. 检查MT19937状态
    print("1. MT19937状态分析:")
    state = np.random.get_state()
    print(f"   生成器类型: {state[0]}")
    print(f"   状态数组长度: {len(state[1])}")
    print(f"   当前位置: {state[2]}")
    print(f"   高斯状态: {state[3]}")
    print(f"   高斯值: {state[4]}")
    
    # 2. 检查状态数组的前几个值
    print(f"\n2. 状态数组前10个值:")
    for i in range(min(10, len(state[1]))):
        print(f"   state[{i}] = {state[1][i]}")
    
    # 3. 测试状态重置
    print(f"\n3. 状态重置测试:")
    original_state = np.random.get_state()
    
    # 生成一些随机数
    for i in range(5):
        np.random.random()
    
    # 重置状态
    np.random.set_state(original_state)
    
    # 再次生成相同的随机数
    print("   重置后生成的随机数:")
    for i in range(5):
        print(f"   {np.random.random()}")

def analyze_seed_source():
    """
    分析种子的可能来源
    """
    print(f"\n=== 种子来源分析 ===")
    
    # 1. 系统信息
    print("1. 系统信息:")
    print(f"   进程ID: {os.getpid()}")
    print(f"   父进程ID: {os.getppid()}")
    print(f"   当前时间: {time.time()}")
    print(f"   时间戳(秒): {int(time.time())}")
    print(f"   时间戳(微秒): {int(time.time() * 1000000)}")
    
    # 2. 环境变量
    print(f"\n2. 相关环境变量:")
    env_vars = ['PYTHONHASHSEED', 'RANDOM_SEED', 'NP_SEED']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"   {var}: {value}")
    
    # 3. 测试不同时间点的种子
    print(f"\n3. 不同时间点的种子测试:")
    for i in range(3):
        time.sleep(0.1)  # 等待0.1秒
        np.random.seed(None)
        rand = np.random.random()
        print(f"   时间点{i+1}: {rand}")

if __name__ == "__main__":
    analyze_numpy_seed_mechanism()
    test_multiple_sessions()
    test_numpy_internals()
    analyze_seed_source()
    
    print(f"\n=== 最终结论 ===")
    print("1. NumPy默认使用系统级随机性（时间+进程ID等）")
    print("2. 不设置种子时，每次运行结果都不同")
    print("3. seed(None)会重新初始化随机状态")
    print("4. 这是随机优化算法的正常行为")
    print("5. 要获得可重复结果，必须设置固定种子")
