"""
简化版代码执行跟踪器 - 专门用于跟踪benchmark_baselines.py
避免跟踪系统模块，减少错误
"""

import sys
import os
import time
import threading
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class SimpleBenchmarkTracer:
    """简化的benchmark跟踪器"""
    
    def __init__(self, log_file: str = "benchmark_simple_trace.log"):
        """初始化跟踪器"""
        self.log_file = log_file
        self.start_time = time.time()
        self.trace_data = []
        self.call_stack = []
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"Benchmark代码执行跟踪开始 - {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
    
    def log_event(self, event_type: str, frame, arg=None):
        """记录跟踪事件"""
        timestamp = time.time() - self.start_time
        thread_id = threading.get_ident()
        
        # 获取文件信息
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        
        # 只跟踪项目相关的文件
        if not self._should_trace_file(filename):
            return
        
        # 安全地处理参数
        arg_str = self._safe_str(arg)
        
        # 创建事件记录
        event = {
            "timestamp": timestamp,
            "thread_id": thread_id,
            "event_type": event_type,
            "filename": os.path.basename(filename),
            "full_filename": filename,
            "function_name": function_name,
            "line_number": line_number,
            "call_stack_depth": len(self.call_stack),
            "arg": arg_str,
            "datetime": datetime.now().isoformat()
        }
        
        self.trace_data.append(event)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            indent = "  " * len(self.call_stack)
            f.write(f"[{timestamp:.6f}] [{thread_id}] {indent}{event_type}: ")
            f.write(f"{os.path.basename(filename)}:{line_number} in {function_name}()")
            if arg_str is not None:
                f.write(f" (arg: {arg_str})")
            f.write("\n")
    
    def _should_trace_file(self, filename: str) -> bool:
        """判断是否应该跟踪该文件"""
        # 跳过系统文件
        if filename.startswith('<'):
            return False
        
        # 跳过跟踪器自身
        if 'tracer' in filename.lower():
            return False
        
        # 跳过Python标准库
        if 'site-packages' in filename and 'modcma' not in filename:
            return False
        
        # 只跟踪项目相关文件
        project_keywords = [
            'benchmark_baselines',
            'modcma',
            'ioh',
            'numpy',
            'pandas'
        ]
        
        return any(keyword in filename.lower() for keyword in project_keywords)
    
    def _safe_str(self, obj) -> str:
        """安全地将对象转换为字符串"""
        if obj is None:
            return None
        
        try:
            return str(obj)
        except Exception:
            try:
                return repr(obj)
            except Exception:
                return f"<{type(obj).__name__}>"
    
    def trace_callback(self, frame, event, arg):
        """sys.settrace的回调函数"""
        if event == 'call':
            self.call_stack.append(frame)
            self.log_event("CALL", frame, arg)
        
        elif event == 'line':
            self.log_event("LINE", frame)
        
        elif event == 'return':
            self.log_event("RETURN", frame, arg)
            if self.call_stack:
                self.call_stack.pop()
        
        elif event == 'exception':
            self.log_event("EXCEPTION", frame, arg)
        
        return self.trace_callback
    
    def start_tracing(self):
        """开始跟踪"""
        sys.settrace(self.trace_callback)
        self.log_event("TRACE_START", sys._getframe())
    
    def stop_tracing(self):
        """停止跟踪"""
        sys.settrace(None)
        self.log_event("TRACE_STOP", sys._getframe())
    
    def save_summary(self, summary_file: str = "benchmark_simple_summary.json"):
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
        
        print(f"跟踪摘要已保存到: {summary_file}")
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """生成执行统计信息"""
        stats = {
            "files_executed": set(),
            "functions_called": set(),
            "total_lines_executed": 0,
            "total_calls": 0,
            "total_returns": 0,
            "total_exceptions": 0,
            "most_executed_lines": {},
            "most_called_functions": {}
        }
        
        line_counts = {}
        function_counts = {}
        
        for event in self.trace_data:
            event_type = event["event_type"]
            filename = event["filename"]
            function_name = event["function_name"]
            line_number = event["line_number"]
            
            stats["files_executed"].add(filename)
            stats["functions_called"].add(f"{filename}:{function_name}")
            
            if event_type == "LINE":
                stats["total_lines_executed"] += 1
                line_key = f"{filename}:{line_number}"
                line_counts[line_key] = line_counts.get(line_key, 0) + 1
            
            elif event_type == "CALL":
                stats["total_calls"] += 1
                func_key = f"{filename}:{function_name}"
                function_counts[func_key] = function_counts.get(func_key, 0) + 1
            
            elif event_type == "RETURN":
                stats["total_returns"] += 1
            
            elif event_type == "EXCEPTION":
                stats["total_exceptions"] += 1
        
        # 转换set为list以便JSON序列化
        stats["files_executed"] = list(stats["files_executed"])
        stats["functions_called"] = list(stats["functions_called"])
        
        # 获取最频繁执行的行和函数
        stats["most_executed_lines"] = dict(sorted(line_counts.items(), 
                                                 key=lambda x: x[1], reverse=True)[:20])
        stats["most_called_functions"] = dict(sorted(function_counts.items(), 
                                                   key=lambda x: x[1], reverse=True)[:20])
        
        return stats
    
    def print_summary(self):
        """打印执行摘要"""
        stats = self._generate_statistics()
        
        print("\n" + "=" * 80)
        print("Benchmark代码执行跟踪摘要")
        print("=" * 80)
        print(f"总执行时间: {time.time() - self.start_time:.6f} 秒")
        print(f"总事件数: {len(self.trace_data)}")
        print(f"执行的文件数: {len(stats['files_executed'])}")
        print(f"调用的函数数: {len(stats['functions_called'])}")
        print(f"执行的总行数: {stats['total_lines_executed']}")
        print(f"函数调用次数: {stats['total_calls']}")
        print(f"函数返回次数: {stats['total_returns']}")
        print(f"异常次数: {stats['total_exceptions']}")
        
        if stats['most_executed_lines']:
            print("\n最频繁执行的行:")
            for line, count in list(stats['most_executed_lines'].items())[:10]:
                print(f"  {line}: {count} 次")
        
        if stats['most_called_functions']:
            print("\n最频繁调用的函数:")
            for func, count in list(stats['most_called_functions'].items())[:10]:
                print(f"  {func}: {count} 次")
        
        print(f"\n执行的文件:")
        for file in stats['files_executed']:
            print(f"  {file}")


# 全局跟踪器实例
_simple_tracer = None

def start_simple_tracing(log_file: str = "benchmark_simple_trace.log"):
    """开始简化的代码执行跟踪"""
    global _simple_tracer
    _simple_tracer = SimpleBenchmarkTracer(log_file)
    _simple_tracer.start_tracing()
    return _simple_tracer

def stop_simple_tracing(summary_file: str = "benchmark_simple_summary.json"):
    """停止简化的代码执行跟踪"""
    global _simple_tracer
    if _simple_tracer:
        _simple_tracer.stop_tracing()
        _simple_tracer.save_summary(summary_file)
        _simple_tracer.print_summary()
        return _simple_tracer
    return None
