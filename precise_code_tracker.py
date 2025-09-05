#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
precise_code_tracker.py - 精确的代码调用统计工具
统计运行benchmark_baselines.py时调用的所有文件和代码
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
import json

class PreciseCodeTracker:
    def __init__(self, output_file="precise_code_analysis.txt"):
        self.output_file = output_file
        self.call_count = 0
        self.tracked_files = {}  # 文件路径 -> 调用信息
        self.tracked_functions = {}  # 函数名 -> 调用信息
        self.lock = threading.Lock()
        
        # 创建输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== 精确代码调用分析报告 ===\n")
            f.write(f"开始时间: {datetime.now()}\n")
            f.write(f"跟踪文件: benchmark_baselines.py\n")
            f.write("=" * 60 + "\n\n")
    
    def log_call(self, func, *args, **kwargs):
        """记录函数调用"""
        with self.lock:
            self.call_count += 1
            
            # 获取函数信息
            func_file = self.get_function_file(func)
            func_name = self.get_function_name(func)
            func_line = self.get_function_line(func)
            
            # 获取调用栈
            stack = traceback.extract_stack()
            
            # 记录文件调用
            if func_file:
                if func_file not in self.tracked_files:
                    self.tracked_files[func_file] = {
                        'calls': 0,
                        'functions': set(),
                        'lines_executed': set(),
                        'first_call': self.call_count,
                        'last_call': self.call_count
                    }
                
                self.tracked_files[func_file]['calls'] += 1
                self.tracked_files[func_file]['functions'].add(func_name)
                self.tracked_files[func_file]['lines_executed'].add(func_line)
                self.tracked_files[func_file]['last_call'] = self.call_count
            
            # 记录函数调用
            if func_name not in self.tracked_functions:
                self.tracked_functions[func_name] = {
                    'calls': 0,
                    'file': func_file,
                    'line': func_line,
                    'first_call': self.call_count,
                    'last_call': self.call_count
                }
            
            self.tracked_functions[func_name]['calls'] += 1
            self.tracked_functions[func_name]['last_call'] = self.call_count
            
            # 记录详细调用信息
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n--- 调用 #{self.call_count} ---\n")
                f.write(f"时间: {datetime.now()}\n")
                f.write(f"函数: {func_name}\n")
                f.write(f"文件: {func_file}\n")
                f.write(f"行号: {func_line}\n")
                f.write(f"参数: args={args}, kwargs={kwargs}\n")
                
                # 记录调用栈
                f.write(f"调用栈:\n")
                for i, (filename, lineno, name, line) in enumerate(stack[:-1]):
                    f.write(f"  {i}: {filename}:{lineno} in {name} - {line}\n")
                
                f.write("-" * 40 + "\n")
    
    def get_function_file(self, func):
        """获取函数所在文件"""
        try:
            return inspect.getfile(func)
        except Exception:
            return None
    
    def get_function_name(self, func):
        """获取函数名"""
        try:
            return f"{func.__module__}.{func.__name__}"
        except Exception:
            return str(func)
    
    def get_function_line(self, func):
        """获取函数定义行号"""
        try:
            return inspect.getsourcelines(func)[1]
        except Exception:
            return 0
    
    def finalize_report(self):
        """完成报告"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n=== 调用统计总结 ===\n")
            f.write(f"结束时间: {datetime.now()}\n")
            f.write(f"总调用次数: {self.call_count}\n")
            f.write(f"涉及文件数量: {len(self.tracked_files)}\n")
            f.write(f"涉及函数数量: {len(self.tracked_functions)}\n")
            
            # 按调用次数排序文件
            sorted_files = sorted(self.tracked_files.items(), 
                                key=lambda x: x[1]['calls'], reverse=True)
            
            f.write(f"\n=== 文件调用统计 ===\n")
            for file_path, info in sorted_files:
                f.write(f"\n文件: {file_path}\n")
                f.write(f"  调用次数: {info['calls']}\n")
                f.write(f"  涉及函数数: {len(info['functions'])}\n")
                f.write(f"  执行行数: {len(info['lines_executed'])}\n")
                f.write(f"  首次调用: #{info['first_call']}\n")
                f.write(f"  最后调用: #{info['last_call']}\n")
                f.write(f"  函数列表:\n")
                for func in sorted(info['functions']):
                    f.write(f"    - {func}\n")
            
            # 按调用次数排序函数
            sorted_functions = sorted(self.tracked_functions.items(), 
                                   key=lambda x: x[1]['calls'], reverse=True)
            
            f.write(f"\n=== 函数调用统计 ===\n")
            for func_name, info in sorted_functions[:20]:  # 只显示前20个
                f.write(f"\n函数: {func_name}\n")
                f.write(f"  调用次数: {info['calls']}\n")
                f.write(f"  文件: {info['file']}\n")
                f.write(f"  行号: {info['line']}\n")
                f.write(f"  首次调用: #{info['first_call']}\n")
                f.write(f"  最后调用: #{info['last_call']}\n")
            
            f.write("=" * 60 + "\n")
        
        # 创建JSON格式的详细数据
        self.save_json_report()
    
    def save_json_report(self):
        """保存JSON格式的详细报告"""
        report_data = {
            'summary': {
                'total_calls': self.call_count,
                'files_count': len(self.tracked_files),
                'functions_count': len(self.tracked_functions),
                'start_time': str(datetime.now()),
                'end_time': str(datetime.now())
            },
            'files': {
                file_path: {
                    'calls': info['calls'],
                    'functions': list(info['functions']),
                    'lines_executed': list(info['lines_executed']),
                    'first_call': info['first_call'],
                    'last_call': info['last_call']
                }
                for file_path, info in self.tracked_files.items()
            },
            'functions': {
                func_name: {
                    'calls': info['calls'],
                    'file': info['file'],
                    'line': info['line'],
                    'first_call': info['first_call'],
                    'last_call': info['last_call']
                }
                for func_name, info in self.tracked_functions.items()
            }
        }
        
        with open("code_analysis_data.json", 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print("JSON格式数据已保存到: code_analysis_data.json")

# 全局跟踪器实例
tracker = PreciseCodeTracker()

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

def auto_track_all_modules():
    """自动跟踪所有已加载的模块"""
    modules_to_track = [
        'ioh',
        'modcma',
        'numpy',
        'pandas',
        'multiprocessing',
        'os',
        'sys',
        'time',
        'copy',
        'itertools',
        'functools',
        'warnings'
    ]
    
    for module_name in modules_to_track:
        if module_name in sys.modules:
            track_module_functions(module_name)
    
    # 跟踪env_new中的所有模块
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
