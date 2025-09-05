#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_default_seed.py - 测试numpy默认随机种子行为
"""

import numpy as np
import os
import time

def test_numpy_default_seed():
    """
    测试numpy的默认随机种子行为
    """
    print("=== NumPy默认随机种子测试 ===")
    
    # 1. 检查当前随机状态
    print("\n1. 当前随机状态:")
    state = np.random.get_state()
    print(f"   随机状态类型: {type(state)}")
    print(f"   状态元组长度: {len(state)}")
    print(f"   第一个元素(MT19937): {state[0]}")
    print(f"   第二个元素(状态数组): 长度={len(state[1])}, 第一个值={state[1][0]}")
    print(f"   第三个元素(位置): {state[2]}")
    print(f"   第四个元素(高斯状态): {state[3]}")
    print(f"   第五个元素(高斯值): {state[4]}")
    
    # 2. 生成一些随机数
    print("\n2. 生成随机数:")
    for i in range(5):
        print(f"   随机数 {i+1}: {np.random.random()}")
    
    # 3. 重新导入numpy测试
    print("\n3. 重新导入numpy后的随机状态:")
    import importlib
    importlib.reload(np)
    print(f"   重新导入后的第一个随机数: {np.random.random()}")
    
    # 4. 测试进程ID和时间的影响
    print("\n4. 系统信息:")
    print(f"   进程ID: {os.getpid()}")
    print(f"   当前时间戳: {time.time()}")
    print(f"   时间戳整数部分: {int(time.time())}")
    
    # 5. 测试多次重新导入
    print("\n5. 多次重新导入测试:")
    for i in range(3):
        importlib.reload(np)
        print(f"   第{i+1}次重新导入: {np.random.random()}")
    
    # 6. 检查numpy版本和随机数生成器
    print(f"\n6. NumPy信息:")
    print(f"   NumPy版本: {np.__version__}")
    print(f"   随机数生成器: {type(np.random.bit_generator)}")
    
    # 7. 测试不同Python会话的随机性
    print(f"\n7. 当前会话的随机数序列:")
    np.random.seed(None)  # 重置为默认状态
    for i in range(5):
        print(f"   随机数 {i+1}: {np.random.random()}")

def test_seed_none_behavior():
    """
    测试np.random.seed(None)的行为
    """
    print("\n=== 测试seed(None)行为 ===")
    
    # 保存当前状态
    original_state = np.random.get_state()
    print("1. 保存原始状态")
    
    # 设置种子为None
    np.random.seed(None)
    print("2. 设置seed(None)后的状态:")
    state_after_none = np.random.get_state()
    print(f"   状态是否改变: {not np.array_equal(original_state[1], state_after_none[1])}")
    print(f"   第一个随机数: {np.random.random()}")
    
    # 再次设置seed(None)
    np.random.seed(None)
    print("3. 再次设置seed(None)后的状态:")
    state_after_none2 = np.random.get_state()
    print(f"   状态是否改变: {not np.array_equal(state_after_none[1], state_after_none2[1])}")
    print(f"   第一个随机数: {np.random.random()}")

def test_system_randomness():
    """
    测试系统级随机性
    """
    print("\n=== 系统级随机性测试 ===")
    
    # 1. 使用系统随机数
    import random
    print("1. Python标准库random模块:")
    print(f"   第一个随机数: {random.random()}")
    print(f"   第二个随机数: {random.random()}")
    
    # 2. 使用os.urandom
    print("\n2. 系统随机字节:")
    random_bytes = os.urandom(4)
    print(f"   随机字节: {random_bytes}")
    print(f"   转换为整数: {int.from_bytes(random_bytes, 'big')}")
    
    # 3. 使用时间作为种子
    print("\n3. 使用时间戳作为种子:")
    time_seed = int(time.time() * 1000000) % (2**32)
    np.random.seed(time_seed)
    print(f"   时间种子: {time_seed}")
    print(f"   第一个随机数: {np.random.random()}")

if __name__ == "__main__":
    test_numpy_default_seed()
    test_seed_none_behavior()
    test_system_randomness()
    
    print(f"\n=== 总结 ===")
    print("1. NumPy默认使用系统时间或进程信息作为随机种子")
    print("2. 每次Python会话启动时，随机状态可能不同")
    print("3. seed(None)会重置为系统随机状态")
    print("4. 不设置种子时，结果具有随机性")
