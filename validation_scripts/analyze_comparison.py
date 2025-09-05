#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_comparison.py - 详细分析比较结果
"""

import pandas as pd
import numpy as np

def analyze_comparison_results():
    """
    分析比较结果的详细报告
    """
    print("=== F20-F24结果比较分析报告 ===")
    
    # 加载比较结果
    df = pd.read_csv('comparison_results.csv')
    df['fx_diff'] = abs(df['fx_dt_fb'] - df['fx_correct'])
    
    print("\n1. 总体统计:")
    print(f"   总比较行数: {len(df)}")
    print(f"   平均差异: {df['fx_diff'].mean():.6f}")
    print(f"   中位数差异: {df['fx_diff'].median():.6f}")
    print(f"   标准差: {df['fx_diff'].std():.6f}")
    print(f"   最大差异: {df['fx_diff'].max():.6f}")
    print(f"   最小差异: {df['fx_diff'].min():.6f}")
    
    print("\n2. 不同容差下的成功率:")
    for tol in [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]:
        success_rate = (df['fx_diff'] <= tol).mean() * 100
        print(f"   容差 {tol:4.2f}: {success_rate:5.1f}%")
    
    print("\n3. 按算法分析:")
    for alg in ['modcma_bipop', 'CS', 'DE']:
        alg_data = df[df['algname'] == alg]
        print(f"\n   {alg}:")
        print(f"     行数: {len(alg_data)}")
        print(f"     平均差异: {alg_data['fx_diff'].mean():.6f}")
        print(f"     容差0.1成功率: {(alg_data['fx_diff'] <= 0.1).mean() * 100:.1f}%")
        print(f"     容差0.5成功率: {(alg_data['fx_diff'] <= 0.5).mean() * 100:.1f}%")
    
    print("\n4. 按函数分析:")
    for fid in sorted(df['fid'].unique()):
        func_data = df[df['fid'] == fid]
        print(f"\n   F{fid}:")
        print(f"     行数: {len(func_data)}")
        print(f"     平均差异: {func_data['fx_diff'].mean():.6f}")
        print(f"     容差0.1成功率: {(func_data['fx_diff'] <= 0.1).mean() * 100:.1f}%")
        print(f"     容差0.5成功率: {(func_data['fx_diff'] <= 0.5).mean() * 100:.1f}%")
    
    print("\n5. 差异最大的10个案例:")
    top_diff = df.nlargest(10, 'fx_diff')[['budget_factor', 'algname', 'fid', 'fx_dt_fb', 'fx_correct', 'fx_diff']]
    print(top_diff.to_string(index=False))
    
    print("\n6. 质量评估:")
    overall_success_01 = (df['fx_diff'] <= 0.1).mean() * 100
    overall_success_05 = (df['fx_diff'] <= 0.5).mean() * 100
    
    if overall_success_01 >= 95:
        print("   ✅ 容差0.1下结果质量优秀！")
    elif overall_success_01 >= 90:
        print("   ⚠️  容差0.1下结果质量良好")
    elif overall_success_01 >= 80:
        print("   ❌ 容差0.1下结果质量一般")
    else:
        print("   ❌ 容差0.1下结果质量较差")
    
    if overall_success_05 >= 95:
        print("   ✅ 容差0.5下结果质量优秀！")
    elif overall_success_05 >= 90:
        print("   ⚠️  容差0.5下结果质量良好")
    elif overall_success_05 >= 80:
        print("   ❌ 容差0.5下结果质量一般")
    else:
        print("   ❌ 容差0.5下结果质量较差")
    
    print(f"\n   建议使用容差: {'0.1' if overall_success_01 >= 80 else '0.5' if overall_success_05 >= 80 else '1.0'}")

if __name__ == "__main__":
    analyze_comparison_results()
