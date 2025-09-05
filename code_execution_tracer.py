"""
代码执行跟踪器 - 记录代码执行的每一步
支持多种跟踪模式：函数调用、模块导入、详细执行路径等
"""

import sys
import os
import traceback
import time
import threading
from functools import wraps
from typing import Dict, List, Any, Optional
import json
import inspect
from datetime import datetime

class CodeExecutionTracer:
    """代码执行跟踪器"""
    
    def __init__(self, log_file: str = "execution_trace.log", 
                 detailed_mode: bool = True,
                 include_args: bool = True,
                 include_return_values: bool = True):
        """
        初始化跟踪器
        
        Args:
            log_file: 日志文件路径
            detailed_mode: 是否启用详细模式
            include_args: 是否记录函数参数
            include_return_values: 是否记录返回值
        """
        self.log_file = log_file
        self.detailed_mode = detailed_mode
        self.include_args = include_args
        self.include_return_values = include_return_values
        self.trace_data = []
        self.start_time = time.time()
        self.thread_local = threading.local()
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"代码执行跟踪开始 - {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志消息"""
        timestamp = time.time() - self.start_time
        thread_id = threading.get_ident()
        
        log_entry = {
            "timestamp": timestamp,
            "thread_id": thread_id,
            "level": level,
            "message": message,
            "datetime": datetime.now().isoformat()
        }
        
        self.trace_data.append(log_entry)
        
        # 写入文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp:.6f}] [{thread_id}] [{level}] {message}\n")
    
    def trace_function(self, func):
        """装饰器：跟踪函数调用"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数信息
            func_name = f"{func.__module__}.{func.__qualname__}"
            file_path = inspect.getfile(func)
            line_number = inspect.getsourcelines(func)[1]
            
            # 记录函数调用开始
            args_str = ""
            if self.include_args and self.detailed_mode:
                args_str = f" args={args}, kwargs={kwargs}"
            
            self.log(f"调用函数: {func_name} (文件: {file_path}:{line_number}){args_str}")
            
            # 执行函数
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # 记录函数调用结束
                return_str = ""
                if self.include_return_values and self.detailed_mode:
                    return_str = f" 返回值: {result}"
                
                self.log(f"函数完成: {func_name} (耗时: {execution_time:.6f}s){return_str}")
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.log(f"函数异常: {func_name} (耗时: {execution_time:.6f}s) 异常: {str(e)}", "ERROR")
                raise
        
        return wrapper
    
    def trace_module_imports(self):
        """跟踪模块导入"""
        original_import = __builtins__['__import__']
        
        def traced_import(name, globals=None, locals=None, fromlist=(), level=0):
            # 记录导入信息
            self.log(f"导入模块: {name}")
            
            # 执行原始导入
            module = original_import(name, globals, locals, fromlist, level)
            
            # 记录导入完成
            if hasattr(module, '__file__'):
                self.log(f"模块导入完成: {name} (文件: {module.__file__})")
            else:
                self.log(f"模块导入完成: {name} (内置模块)")
            
            return module
        
        __builtins__['__import__'] = traced_import
    
    def trace_class_methods(self, cls):
        """跟踪类的所有方法"""
        for name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
            if not name.startswith('_'):
                setattr(cls, name, self.trace_function(method))
        return cls
    
    def trace_all_methods(self, obj):
        """跟踪对象的所有方法"""
        for name in dir(obj):
            attr = getattr(obj, name)
            if callable(attr) and not name.startswith('_'):
                setattr(obj, name, self.trace_function(attr))
        return obj
    
    def save_trace_summary(self, summary_file: str = "execution_summary.json"):
        """保存跟踪摘要"""
        summary = {
            "execution_info": {
                "start_time": self.start_time,
                "end_time": time.time(),
                "total_duration": time.time() - self.start_time,
                "total_events": len(self.trace_data)
            },
            "trace_data": self.trace_data,
            "statistics": self._generate_statistics()
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        self.log(f"跟踪摘要已保存到: {summary_file}")
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """生成执行统计信息"""
        stats = {
            "function_calls": {},
            "module_imports": [],
            "execution_times": [],
            "errors": []
        }
        
        for entry in self.trace_data:
            if "调用函数:" in entry["message"]:
                func_name = entry["message"].split("调用函数: ")[1].split(" (")[0]
                if func_name not in stats["function_calls"]:
                    stats["function_calls"][func_name] = 0
                stats["function_calls"][func_name] += 1
            
            elif "导入模块:" in entry["message"]:
                module_name = entry["message"].split("导入模块: ")[1]
                stats["module_imports"].append(module_name)
            
            elif "函数异常:" in entry["message"]:
                stats["errors"].append(entry["message"])
        
        return stats
    
    def print_summary(self):
        """打印执行摘要"""
        stats = self._generate_statistics()
        
        print("\n" + "=" * 80)
        print("代码执行跟踪摘要")
        print("=" * 80)
        print(f"总执行时间: {time.time() - self.start_time:.6f} 秒")
        print(f"总事件数: {len(self.trace_data)}")
        print(f"函数调用次数: {len(stats['function_calls'])}")
        print(f"模块导入次数: {len(stats['module_imports'])}")
        print(f"错误数量: {len(stats['errors'])}")
        
        if stats['function_calls']:
            print("\n最频繁调用的函数:")
            sorted_calls = sorted(stats['function_calls'].items(), 
                                key=lambda x: x[1], reverse=True)
            for func_name, count in sorted_calls[:10]:
                print(f"  {func_name}: {count} 次")
        
        if stats['module_imports']:
            print(f"\n导入的模块 ({len(stats['module_imports'])} 个):")
            for module in set(stats['module_imports']):
                print(f"  {module}")
        
        if stats['errors']:
            print(f"\n错误信息 ({len(stats['errors'])} 个):")
            for error in stats['errors']:
                print(f"  {error}")


# 全局跟踪器实例
_tracer = None

def get_tracer() -> CodeExecutionTracer:
    """获取全局跟踪器实例"""
    global _tracer
    if _tracer is None:
        _tracer = CodeExecutionTracer()
    return _tracer

def start_tracing(log_file: str = "execution_trace.log", 
                  detailed_mode: bool = True,
                  trace_imports: bool = True):
    """开始代码执行跟踪"""
    global _tracer
    _tracer = CodeExecutionTracer(log_file, detailed_mode)
    
    if trace_imports:
        _tracer.trace_module_imports()
    
    _tracer.log("开始代码执行跟踪")
    return _tracer

def stop_tracing(summary_file: str = "execution_summary.json"):
    """停止代码执行跟踪并保存摘要"""
    global _tracer
    if _tracer:
        _tracer.log("结束代码执行跟踪")
        _tracer.save_trace_summary(summary_file)
        _tracer.print_summary()
        return _tracer
    return None

def trace_function(func):
    """装饰器：跟踪函数调用"""
    tracer = get_tracer()
    return tracer.trace_function(func)

def trace_class(cls):
    """装饰器：跟踪类的所有方法"""
    tracer = get_tracer()
    return tracer.trace_class_methods(cls)
