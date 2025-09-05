"""
高级代码执行跟踪器 - 使用sys.settrace进行深度跟踪
可以跟踪到每一行代码的执行
"""

import sys
import os
import time
import threading
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class AdvancedCodeTracer:
    """高级代码执行跟踪器 - 使用sys.settrace"""
    
    def __init__(self, log_file: str = "advanced_execution_trace.log",
                 trace_lines: bool = True,
                 trace_calls: bool = True,
                 trace_returns: bool = True,
                 trace_exceptions: bool = True,
                 include_source: bool = True):
        """
        初始化高级跟踪器
        
        Args:
            log_file: 日志文件路径
            trace_lines: 是否跟踪每行代码
            trace_calls: 是否跟踪函数调用
            trace_returns: 是否跟踪函数返回
            trace_exceptions: 是否跟踪异常
            include_source: 是否包含源代码
        """
        self.log_file = log_file
        self.trace_lines = trace_lines
        self.trace_calls = trace_calls
        self.trace_returns = trace_returns
        self.trace_exceptions = trace_exceptions
        self.include_source = include_source
        
        self.start_time = time.time()
        self.trace_data = []
        self.call_stack = []
        self.current_frame = None
        
        # 创建日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"高级代码执行跟踪开始 - {datetime.now()}\n")
            f.write("=" * 100 + "\n\n")
    
    def log_event(self, event_type: str, frame, arg=None):
        """记录跟踪事件"""
        timestamp = time.time() - self.start_time
        thread_id = threading.get_ident()
        
        # 获取文件信息
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        
        # 获取源代码（如果启用）
        source_line = ""
        if self.include_source:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if line_number <= len(lines):
                        source_line = lines[line_number - 1].strip()
            except:
                source_line = "无法读取源代码"
        
        # 创建事件记录
        # 安全地转换arg为字符串
        arg_str = None
        if arg is not None:
            try:
                arg_str = str(arg)
            except Exception:
                try:
                    arg_str = repr(arg)
                except Exception:
                    arg_str = f"<无法转换的对象: {type(arg).__name__}>"
        
        event = {
            "timestamp": timestamp,
            "thread_id": thread_id,
            "event_type": event_type,
            "filename": filename,
            "function_name": function_name,
            "line_number": line_number,
            "source_line": source_line,
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
            if source_line:
                f.write(f" -> {source_line}")
            if arg_str is not None:
                f.write(f" (arg: {arg_str})")
            f.write("\n")
    
    def trace_callback(self, frame, event, arg):
        """sys.settrace的回调函数"""
        # 跳过系统模块和跟踪器自身的代码
        filename = frame.f_code.co_filename
        if (filename.startswith('<') or 
            'advanced_code_tracer.py' in filename or
            'code_execution_tracer.py' in filename or
            filename.endswith('.pyc')):
            return self.trace_callback
        
        if event == 'call':
            if self.trace_calls:
                self.call_stack.append(frame)
                self.log_event("CALL", frame, arg)
        
        elif event == 'line':
            if self.trace_lines:
                self.log_event("LINE", frame)
        
        elif event == 'return':
            if self.trace_returns:
                self.log_event("RETURN", frame, arg)
                if self.call_stack:
                    self.call_stack.pop()
        
        elif event == 'exception':
            if self.trace_exceptions:
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
    
    def save_summary(self, summary_file: str = "advanced_execution_summary.json"):
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
        
        print(f"高级跟踪摘要已保存到: {summary_file}")
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """生成执行统计信息"""
        stats = {
            "files_executed": set(),
            "functions_called": set(),
            "total_lines_executed": 0,
            "total_calls": 0,
            "total_returns": 0,
            "total_exceptions": 0,
            "execution_flow": [],
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
                line_key = f"{os.path.basename(filename)}:{line_number}"
                line_counts[line_key] = line_counts.get(line_key, 0) + 1
            
            elif event_type == "CALL":
                stats["total_calls"] += 1
                func_key = f"{os.path.basename(filename)}:{function_name}"
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
        
        print("\n" + "=" * 100)
        print("高级代码执行跟踪摘要")
        print("=" * 100)
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


# 全局高级跟踪器实例
_advanced_tracer = None

def start_advanced_tracing(log_file: str = "advanced_execution_trace.log",
                          trace_lines: bool = True,
                          trace_calls: bool = True,
                          trace_returns: bool = True,
                          trace_exceptions: bool = True):
    """开始高级代码执行跟踪"""
    global _advanced_tracer
    _advanced_tracer = AdvancedCodeTracer(
        log_file=log_file,
        trace_lines=trace_lines,
        trace_calls=trace_calls,
        trace_returns=trace_returns,
        trace_exceptions=trace_exceptions
    )
    _advanced_tracer.start_tracing()
    return _advanced_tracer

def stop_advanced_tracing(summary_file: str = "advanced_execution_summary.json"):
    """停止高级代码执行跟踪"""
    global _advanced_tracer
    if _advanced_tracer:
        _advanced_tracer.stop_tracing()
        _advanced_tracer.save_summary(summary_file)
        _advanced_tracer.print_summary()
        return _advanced_tracer
    return None
