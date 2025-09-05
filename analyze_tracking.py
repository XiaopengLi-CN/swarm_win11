#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_tracking.py - 分析代码跟踪结果
提取所有env_new中的文件调用
"""

import re
import os
from collections import defaultdict

def analyze_tracking_file(filename="benchmark_baselines.txt"):
    """分析跟踪文件"""
    
    env_new_files = set()
    env_new_functions = defaultdict(list)
    call_count = 0
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割每个调用记录
    calls = content.split('--- 调用 #')
    
    for call in calls[1:]:  # 跳过第一个空的部分
        call_count += 1
        
        # 提取函数文件信息
        file_match = re.search(r'函数文件: (.+)', call)
        if file_match:
            file_path = file_match.group(1)
            if 'env_new' in file_path:
                env_new_files.add(file_path)
                
                # 提取函数信息
                func_match = re.search(r'函数: (.+) at', call)
                if func_match:
                    func_info = func_match.group(1)
                    env_new_functions[file_path].append(func_info)
    
    return env_new_files, env_new_functions, call_count

def create_detailed_report():
    """创建详细报告"""
    
    env_new_files, env_new_functions, total_calls = analyze_tracking_file()
    
    print("=== 代码跟踪分析报告 ===\n")
    print(f"总调用次数: {total_calls}")
    print(f"env_new中的文件数量: {len(env_new_files)}")
    print(f"env_new中的函数调用次数: {sum(len(funcs) for funcs in env_new_functions.values())}")
    
    print("\n=== env_new中的文件列表 ===")
    for file_path in sorted(env_new_files):
        print(f"\n文件: {file_path}")
        print(f"  调用次数: {len(env_new_functions[file_path])}")
        print("  函数列表:")
        for func in env_new_functions[file_path]:
            print(f"    - {func}")
    
    # 保存详细报告
    with open("tracking_analysis_report.txt", 'w', encoding='utf-8') as f:
        f.write("=== 代码跟踪分析报告 ===\n\n")
        f.write(f"总调用次数: {total_calls}\n")
        f.write(f"env_new中的文件数量: {len(env_new_files)}\n")
        f.write(f"env_new中的函数调用次数: {sum(len(funcs) for funcs in env_new_functions.values())}\n")
        
        f.write("\n=== env_new中的文件列表 ===\n")
        for file_path in sorted(env_new_files):
            f.write(f"\n文件: {file_path}\n")
            f.write(f"  调用次数: {len(env_new_functions[file_path])}\n")
            f.write("  函数列表:\n")
            for func in env_new_functions[file_path]:
                f.write(f"    - {func}\n")
    
    print(f"\n详细报告已保存到: tracking_analysis_report.txt")
    
    return env_new_files, env_new_functions

def extract_key_files():
    """提取关键文件"""
    
    env_new_files, env_new_functions, _ = analyze_tracking_file()
    
    # 按调用次数排序
    file_call_counts = {file: len(funcs) for file, funcs in env_new_functions.items()}
    sorted_files = sorted(file_call_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("\n=== 按调用次数排序的文件 ===")
    for file_path, call_count in sorted_files:
        print(f"{call_count:4d} 次调用: {file_path}")
    
    # 保存关键文件列表
    with open("key_files_for_translation.txt", 'w', encoding='utf-8') as f:
        f.write("=== 需要翻译的关键文件 ===\n\n")
        f.write("按调用次数排序:\n\n")
        for file_path, call_count in sorted_files:
            f.write(f"{call_count:4d} 次调用: {file_path}\n")
    
    print(f"\n关键文件列表已保存到: key_files_for_translation.txt")
    
    return sorted_files

if __name__ == "__main__":
    print("开始分析代码跟踪结果...")
    
    # 创建详细报告
    env_new_files, env_new_functions = create_detailed_report()
    
    # 提取关键文件
    key_files = extract_key_files()
    
    print("\n分析完成！")
