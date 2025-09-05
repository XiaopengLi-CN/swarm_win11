#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
advanced_code_tracker.py - 高级代码调用跟踪器
更详细地记录所有代码调用，包括env_new中的文件
"""

import os
import sys
import inspect
import traceback
import linecache
import importlib
from datetime import datetime
from functools import wraps
import threading

class AdvancedCodeTracker:
    def __init__(self, output_file="benchmark_baselines.txt"):
        self.output_file = output_file
        self.call_stack = []
        self.call_count = 0
        self.tracked_modules = set()
        self.tracked_files = set()
        self.lock = threading.Lock()
        
        # 创建输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 高级代码调用跟踪报告 ===\n")
            f.write(f"开始时间: {datetime.now()}\n")
            f.write(f"跟踪文件: benchmark_baselines.py\n")
            f.write(f"目标: 记录所有env_new中的代码调用\n")
            f.write("=" * 60 + "\n\n")
    
    def log_call(self, func, *args, **kwargs):
        """记录函数调用"""
        with self.lock:
            self.call_count += 1
            
            # 获取调用栈信息
            frame = inspect.currentframe().f_back
            caller_info = self.get_frame_info(frame)
            func_info = self.get_function_info(func)
            
            # 检查是否是env_new中的文件
            func_file = self.get_function_file(func)
            if func_file and 'env_new' in func_file:
                self.tracked_files.add(func_file)
            
            # 记录到文件
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n--- 调用 #{self.call_count} ---\n")
                f.write(f"时间: {datetime.now()}\n")
                f.write(f"函数: {func_info}\n")
                f.write(f"函数文件: {func_file}\n")
                f.write(f"调用者: {caller_info}\n")
                f.write(f"参数: args={args}, kwargs={kwargs}\n")
                
                # 记录函数源代码
                try:
                    source_lines = inspect.getsourcelines(func)
                    f.write(f"源代码:\n")
                    for i, line in enumerate(source_lines[0], source_lines[1]):
                        f.write(f"  {i}: {line.rstrip()}\n")
                except Exception as e:
                    f.write(f"无法获取源代码: {e}\n")
                
                # 记录调用栈
                f.write(f"调用栈:\n")
                stack = traceback.extract_stack()
                for i, (filename, lineno, name, line) in enumerate(stack[:-1]):
                    f.write(f"  {i}: {filename}:{lineno} in {name} - {line}\n")
                
                f.write("-" * 40 + "\n")
    
    def get_frame_info(self, frame):
        """获取帧信息"""
        if frame is None:
            return "Unknown"
        
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        func_name = frame.f_code.co_name
        
        # 检查是否是env_new中的文件
        if 'env_new' in filename:
            self.tracked_files.add(filename)
        
        return f"{filename}:{lineno} in {func_name}"
    
    def get_function_info(self, func):
        """获取函数信息"""
        try:
            module = func.__module__
            name = func.__name__
            filename = inspect.getfile(func)
            lineno = inspect.getsourcelines(func)[1]
            
            return f"{module}.{name} at {filename}:{lineno}"
        except Exception as e:
            return f"Unknown function: {e}"
    
    def get_function_file(self, func):
        """获取函数所在文件"""
        try:
            return inspect.getfile(func)
        except Exception:
            return None
    
    def track_module(self, module_name):
        """跟踪特定模块"""
        self.tracked_modules.add(module_name)
    
    def finalize_report(self):
        """完成报告"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n=== 跟踪总结 ===\n")
            f.write(f"结束时间: {datetime.now()}\n")
            f.write(f"总调用次数: {self.call_count}\n")
            f.write(f"跟踪的模块:\n")
            for module in sorted(self.tracked_modules):
                f.write(f"  - {module}\n")
            f.write(f"\n跟踪的env_new文件:\n")
            for file in sorted(self.tracked_files):
                if 'env_new' in file:
                    f.write(f"  - {file}\n")
            f.write("=" * 60 + "\n")

# 全局跟踪器实例
tracker = AdvancedCodeTracker()

def track_function(func):
    """装饰器：跟踪函数调用"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracker.log_call(func, *args, **kwargs)
        return func(*args, **kwargs)
    return wrapper

def track_class(cls):
    """装饰器：跟踪类的所有方法"""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if not name.startswith('_'):
            setattr(cls, name, track_function(method))
    return cls

def track_module_functions(module_name):
    """跟踪模块中的所有函数"""
    try:
        module = sys.modules.get(module_name)
        if module:
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj):
                    setattr(module, name, track_function(obj))
                elif inspect.isclass(obj):
                    setattr(module, name, track_class(obj))
    except Exception as e:
        print(f"跟踪模块 {module_name} 时出错: {e}")

def auto_track_env_new():
    """自动跟踪env_new中的模块"""
    env_new_path = "env_new/Lib/site-packages"
    if os.path.exists(env_new_path):
        for root, dirs, files in os.walk(env_new_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    module_path = os.path.relpath(file_path, env_new_path)
                    module_name = module_path.replace(os.sep, '.').replace('.py', '')
                    
                    try:
                        if module_name in sys.modules:
                            track_module_functions(module_name)
                    except Exception as e:
                        print(f"跟踪模块 {module_name} 时出错: {e}")

# 自动跟踪常用模块
def auto_track_modules():
    """自动跟踪常用模块"""
    modules_to_track = [
        'ioh',
        'modcma',
        'numpy',
        'pandas',
        'multiprocessing'
    ]
    
    for module_name in modules_to_track:
        if module_name in sys.modules:
            track_module_functions(module_name)
    
    # 跟踪env_new中的模块
    auto_track_env_new()
