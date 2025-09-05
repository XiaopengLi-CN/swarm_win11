#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_results_tolerance.py - 比较dt_fb.csv与f20-f24.xlsx的fx容差结果
"""

import pandas as pd
import numpy as np
import os

def load_and_validate_file(file_path):
    """
    加载并验证文件
    """
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return None
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"❌ 不支持的文件格式: {file_path}")
            return None
        
        print(f"✅ 成功加载 {file_path}，包含 {len(df)} 行数据")
        print(f"列名: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ 加载文件失败: {e}")
        return None

def compare_results_with_tolerance(dt_fb_file="dt_fb.csv", correct_file="f20-f24.xlsx", tolerance=0.5):
    """
    比较dt_fb.csv与f20-f24.xlsx的fx容差结果
    """
    print("=" * 80)
    print("🔍 fx容差比较工具")
    print("=" * 80)
    
    # 文件检查
    print("文件检查:")
    print(f"- {dt_fb_file}: {'✅ 存在' if os.path.exists(dt_fb_file) else '❌ 不存在'}")
    print(f"- {correct_file}: {'✅ 存在' if os.path.exists(correct_file) else '❌ 不存在'}")
    
    # 加载数据
    dt_fb = load_and_validate_file(dt_fb_file)
    correct = load_and_validate_file(correct_file)
    
    if dt_fb is None or correct is None:
        print("❌ 数据加载失败")
        return
    
    print(f"\n📊 数据概览:")
    print(f"{dt_fb_file}: {len(dt_fb)} 行")
    print(f"{correct_file}: {len(correct)} 行")
    
    # 检查必要列
    required_cols = ['budget_factor', 'algname', 'fid', 'dim', 'fx']
    missing_cols_dt_fb = [col for col in required_cols if col not in dt_fb.columns]
    missing_cols_correct = [col for col in required_cols if col not in correct.columns]
    
    if missing_cols_dt_fb or missing_cols_correct:
        print(f"❌ 缺少必要列:")
        if missing_cols_dt_fb:
            print(f"  {dt_fb_file}: {missing_cols_dt_fb}")
        if missing_cols_correct:
            print(f"  {correct_file}: {missing_cols_correct}")
        return
    
    print("✅ 所有必要列都存在")
    
    # 检查算法列表
    dt_fb_algs = sorted(dt_fb['algname'].unique())
    correct_algs = sorted(correct['algname'].unique())
    print(f"\n🔍 算法列表:")
    print(f"{dt_fb_file}中的算法: {dt_fb_algs}")
    print(f"{correct_file}中的算法: {correct_algs}")
    
    if dt_fb_algs == correct_algs:
        print("✅ 算法列表一致")
    else:
        print("❌ 算法列表不一致")
        return
    
    # 定义分组列
    group_cols = ['budget_factor', 'fid', 'dim']
    
    # 获取唯一组合
    dt_fb_combinations = dt_fb[group_cols].drop_duplicates()
    correct_combinations = correct[group_cols].drop_duplicates()
    
    print(f"\n📋 测试组合:")
    print(f"{dt_fb_file}: {len(dt_fb_combinations)} 个组合")
    print(f"{correct_file}: {len(correct_combinations)} 个组合")
    
    # 找到共同组合
    common_combinations = pd.merge(dt_fb_combinations, correct_combinations, on=group_cols)
    print(f"共同组合: {len(common_combinations)} 个")
    
    if len(common_combinations) == 0:
        print("❌ 没有找到共同的测试组合")
        return
    
    print(f"\n🔍 开始比较fx容差 (容差: {tolerance})...")
    print("=" * 80)
    
    tolerance_results = []
    within_tolerance_count = 0
    total_comparisons = 0
    
    for _, combo in common_combinations.iterrows():
        # 过滤数据
        dt_fb_subset = dt_fb[(dt_fb[group_cols] == combo).all(axis=1)].copy()
        correct_subset = correct[(correct[group_cols] == combo).all(axis=1)].copy()
        
        # 按算法名排序确保对应
        dt_fb_subset = dt_fb_subset.sort_values('algname').reset_index(drop=True)
        correct_subset = correct_subset.sort_values('algname').reset_index(drop=True)
        
        combo_str = "_".join([f"{col.replace('_factor', '')}{combo[col]}" for col in group_cols])
        
        # 比较每个算法的fx值
        all_within_tolerance = True
        comparison_details = []
        
        for i in range(len(dt_fb_subset)):
            if i < len(correct_subset):
                dt_fb_fx = dt_fb_subset.iloc[i]['fx']
                correct_fx = correct_subset.iloc[i]['fx']
                algname = dt_fb_subset.iloc[i]['algname']
                
                fx_diff = abs(dt_fb_fx - correct_fx)
                within_tolerance = fx_diff <= tolerance
                
                if not within_tolerance:
                    all_within_tolerance = False
                
                comparison_details.append({
                    'algname': algname,
                    'dt_fb_fx': dt_fb_fx,
                    'correct_fx': correct_fx,
                    'fx_diff': fx_diff,
                    'within_tolerance': within_tolerance
                })
        
        if all_within_tolerance:
            print(f"✅ {combo_str}: 所有算法fx值都在容差范围内")
            within_tolerance_count += 1
        else:
            print(f"❌ {combo_str}: 部分算法fx值超出容差范围")
            for detail in comparison_details:
                if not detail['within_tolerance']:
                    print(f"    {detail['algname']}: fx差异={detail['fx_diff']:.6f} (dt_fb={detail['dt_fb_fx']:.6f} vs 标准={detail['correct_fx']:.6f})")
        
        total_comparisons += 1
        
        tolerance_results.append({
            'combination': combo_str,
            **combo.to_dict(),
            'all_within_tolerance': all_within_tolerance,
            'comparison_details': comparison_details
        })
    
    # 保存详细结果
    detailed_results = []
    for result in tolerance_results:
        for detail in result['comparison_details']:
            detailed_results.append({
                'combination': result['combination'],
                'budget_factor': result['budget_factor'],
                'fid': result['fid'],
                'dim': result['dim'],
                'algname': detail['algname'],
                'dt_fb_fx': detail['dt_fb_fx'],
                'correct_fx': detail['correct_fx'],
                'fx_diff': detail['fx_diff'],
                'within_tolerance': detail['within_tolerance']
            })
    
    detailed_df = pd.DataFrame(detailed_results)
    detailed_df.to_csv("tolerance_comparison_results.csv", index=False)
    
    print("=" * 80)
    print("📊 fx容差比较总结")
    print("=" * 80)
    print(f"总测试组合数: {total_comparisons}")
    print(f"所有算法都在容差范围内的组合数: {within_tolerance_count}")
    print(f"容差一致性比例: {within_tolerance_count/total_comparisons*100:.2f}%")
    
    if within_tolerance_count == total_comparisons:
        print("✅ fx容差一致性完美")
    elif within_tolerance_count/total_comparisons >= 0.8:
        print("✅ fx容差一致性良好")
    elif within_tolerance_count/total_comparisons >= 0.6:
        print("⚠️ fx容差一致性一般")
    else:
        print("❌ fx容差一致性较差")
    
    print(f"\n详细容差比较结果已保存到: tolerance_comparison_results.csv")
    print("容差比较完成！")

def main():
    """
    主函数
    """
    print("=== fx容差比较工具 ===")
    
    # 比较不同容差
    tolerances = [0.1, 0.2, 0.5, 1.0]
    
    for tolerance in tolerances:
        print(f"\n{'='*60}")
        print(f"容差: {tolerance}")
        print(f"{'='*60}")
        compare_results_with_tolerance(tolerance=tolerance)

if __name__ == "__main__":
    main()
