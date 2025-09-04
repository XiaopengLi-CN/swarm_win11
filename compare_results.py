#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_results.py - 结果比较脚本
比较dt_fb.csv和correct answer.csv文件，检查结果是否符合预期
"""

import numpy as np
import pandas as pd
import os

def load_and_validate_csv(filename):
    """
    加载并验证CSV文件
    """
    if not os.path.exists(filename):
        print(f"错误：找不到文件 {filename}")
        return None
    
    try:
        df = pd.read_csv(filename)
        print(f"成功加载 {filename}，包含 {len(df)} 行数据")
        print(f"列名: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"加载文件 {filename} 时出错: {e}")
        return None

def compare_results(dt_fb_file="dt_fb.csv", correct_file="correct answer.csv", tolerance=0.1):
    """
    比较两个CSV文件的结果
    
    参数:
    - dt_fb_file: dt_fb.csv文件路径
    - correct_file: correct answer.csv文件路径
    - tolerance: fx值的容差（默认0.1）
    """
    print("开始比较结果...")
    print(f"容差设置: {tolerance}")
    
    # 加载两个文件
    dt_fb = load_and_validate_csv(dt_fb_file)
    correct = load_and_validate_csv(correct_file)
    
    if dt_fb is None or correct is None:
        print("文件加载失败，无法进行比较")
        return
    
    # 检查必需的列
    required_columns = ['budget_factor', 'algname', 'fid', 'dim', 'lib', 'fx', 'budget']
    
    for col in required_columns:
        if col not in dt_fb.columns:
            print(f"错误：dt_fb.csv 缺少列 '{col}'")
            return
        if col not in correct.columns:
            print(f"错误：correct answer.csv 缺少列 '{col}'")
            return
    
    print("\n文件结构验证通过")
    
    # 合并两个数据框进行比较
    # 使用除了'fx'之外的所有列作为合并键
    merge_columns = ['budget_factor', 'algname', 'fid', 'dim', 'lib', 'budget']
    
    print(f"\n使用以下列作为匹配键: {merge_columns}")
    
    # 合并数据
    merged = pd.merge(dt_fb, correct, 
                     on=merge_columns, 
                     suffixes=('_dt_fb', '_correct'),
                     how='outer',
                     indicator=True)
    
    print(f"合并后数据包含 {len(merged)} 行")
    
    # 分析合并结果
    print("\n合并结果分析:")
    print(f"- 只在dt_fb.csv中存在: {len(merged[merged['_merge'] == 'left_only'])} 行")
    print(f"- 只在correct answer.csv中存在: {len(merged[merged['_merge'] == 'right_only'])} 行")
    print(f"- 两个文件都存在: {len(merged[merged['_merge'] == 'both'])} 行")
    
    # 只比较两个文件都存在的行
    both_exist = merged[merged['_merge'] == 'both'].copy()
    
    if len(both_exist) == 0:
        print("\n警告：没有找到匹配的行进行比较")
        return
    
    print(f"\n开始比较 {len(both_exist)} 行数据...")
    
    # 计算fx值的差异
    both_exist['fx_diff'] = abs(both_exist['fx_dt_fb'] - both_exist['fx_correct'])
    both_exist['within_tolerance'] = both_exist['fx_diff'] <= tolerance
    
    # 统计结果
    total_comparisons = len(both_exist)
    within_tolerance = both_exist['within_tolerance'].sum()
    outside_tolerance = total_comparisons - within_tolerance
    
    print(f"\n比较结果统计:")
    print(f"- 总比较行数: {total_comparisons}")
    print(f"- 符合容差要求 (≤{tolerance}): {within_tolerance} 行 ({within_tolerance/total_comparisons*100:.1f}%)")
    print(f"- 超出容差要求 (> {tolerance}): {outside_tolerance} 行 ({outside_tolerance/total_comparisons*100:.1f}%)")
    
    # 显示超出容差的行
    if outside_tolerance > 0:
        print(f"\n超出容差的行 (fx_diff > {tolerance}):")
        outliers = both_exist[~both_exist['within_tolerance']].copy()
        outliers = outliers.sort_values('fx_diff', ascending=False)
        
        # 显示前10个最大的差异
        display_columns = merge_columns + ['fx_dt_fb', 'fx_correct', 'fx_diff']
        print(outliers[display_columns].head(10).to_string(index=False))
    
    # 保存详细比较结果
    output_file = "comparison_results.csv"
    both_exist.to_csv(output_file, index=False)
    print(f"\n详细比较结果已保存到: {output_file}")
    
    # 生成摘要报告
    summary = {
        'total_comparisons': total_comparisons,
        'within_tolerance': within_tolerance,
        'outside_tolerance': outside_tolerance,
        'tolerance': tolerance,
        'success_rate': within_tolerance/total_comparisons*100
    }
    
    print(f"\n摘要报告:")
    print(f"- 成功率: {summary['success_rate']:.1f}%")
    print(f"- 失败率: {100-summary['success_rate']:.1f}%")
    
    if summary['success_rate'] >= 95:
        print("✅ 结果质量优秀！")
    elif summary['success_rate'] >= 90:
        print("⚠️  结果质量良好，但有一些差异")
    elif summary['success_rate'] >= 80:
        print("❌ 结果质量一般，存在较多差异")
    else:
        print("❌ 结果质量较差，存在大量差异")
    
    return summary

def main():
    """
    主函数
    """
    print("=== 结果比较工具 ===")
    
    # 检查文件是否存在
    dt_fb_exists = os.path.exists("dt_fb.csv")
    correct_exists = os.path.exists("correct answer.csv")
    
    print(f"文件检查:")
    print(f"- dt_fb.csv: {'✅ 存在' if dt_fb_exists else '❌ 不存在'}")
    print(f"- correct answer.csv: {'✅ 存在' if correct_exists else '❌ 不存在'}")
    
    if not dt_fb_exists:
        print("\n请先运行 dt_fb.py 生成 dt_fb.csv 文件")
        return
    
    if not correct_exists:
        print("\n请确保 correct answer.csv 文件存在")
        return
    
    # 执行比较
    summary = compare_results()
    
    if summary:
        print(f"\n比较完成！详细结果请查看 comparison_results.csv")

if __name__ == "__main__":
    main()
