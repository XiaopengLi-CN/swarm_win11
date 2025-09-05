#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_results.py - 结果比较脚本
比较dt_fb.csv和f20-f24.xlsx文件，检查算法排名是否一致
"""

import numpy as np
import pandas as pd
import os

def load_and_validate_file(filename):
    """
    加载并验证CSV或Excel文件
    """
    if not os.path.exists(filename):
        print(f"错误：找不到文件 {filename}")
        return None
    
    try:
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(filename)
        else:
            df = pd.read_csv(filename)
        print(f"成功加载 {filename}，包含 {len(df)} 行数据")
        print(f"列名: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"加载文件 {filename} 时出错: {e}")
        return None

def compare_algorithm_rankings(dt_fb_file="dt_fb.csv", correct_file="f20-f24.xlsx"):
    """
    比较算法排名是否一致
    
    参数:
    - dt_fb_file: dt_fb.csv文件路径
    - correct_file: f20-f24.xlsx文件路径
    """
    print("=" * 80)
    print("🔍 算法排名一致性比较")
    print("=" * 80)
    
    # 加载两个文件
    dt_fb = load_and_validate_file(dt_fb_file)
    correct = load_and_validate_file(correct_file)
    
    if dt_fb is None or correct is None:
        print("文件加载失败，无法进行比较")
        return
    
    print(f"\n📊 数据概览:")
    print(f"dt_fb.csv: {len(dt_fb)} 行")
    print(f"f20-f24.xlsx: {len(correct)} 行")
    
    # 检查必要的列
    required_cols = ['budget_factor', 'fid', 'dim', 'budget', 'algname', 'fx']
    for col in required_cols:
        if col not in dt_fb.columns:
            print(f"错误：dt_fb.csv 缺少列 '{col}'")
            return
        if col not in correct.columns:
            print(f"错误：f20-f24.xlsx 缺少列 '{col}'")
            return
    
    print(f"\n✅ 所有必要列都存在")
    
    # 获取算法列表
    dt_fb_algs = sorted(dt_fb['algname'].unique())
    correct_algs = sorted(correct['algname'].unique())
    
    print(f"\n🔍 算法列表:")
    print(f"dt_fb.csv中的算法: {dt_fb_algs}")
    print(f"f20-f24.xlsx中的算法: {correct_algs}")
    
    # 检查算法是否一致
    if set(dt_fb_algs) != set(correct_algs):
        print(f"⚠️ 警告: 两个文件的算法列表不完全一致")
        common_algs = set(dt_fb_algs) & set(correct_algs)
        print(f"共同算法: {sorted(common_algs)}")
    else:
        print(f"✅ 算法列表一致")
    
    # 获取测试组合
    dt_fb_combinations = dt_fb[['budget_factor', 'fid', 'dim', 'budget']].drop_duplicates()
    correct_combinations = correct[['budget_factor', 'fid', 'dim', 'budget']].drop_duplicates()
    
    print(f"\n📋 测试组合:")
    print(f"dt_fb.csv: {len(dt_fb_combinations)} 个组合")
    print(f"f20-f24.xlsx: {len(correct_combinations)} 个组合")
    
    # 找到共同的测试组合
    common_combinations = pd.merge(
        dt_fb_combinations, 
        correct_combinations, 
        on=['budget_factor', 'fid', 'dim', 'budget'], 
        how='inner'
    )
    
    print(f"共同组合: {len(common_combinations)} 个")
    
    if len(common_combinations) == 0:
        print("❌ 没有找到共同的测试组合")
        return
    
    # 比较每个组合的算法排名
    ranking_matches = 0
    total_combinations = len(common_combinations)
    ranking_details = []
    
    print(f"\n🔍 开始比较排名...")
    print("=" * 80)
    
    for idx, row in common_combinations.iterrows():
        budget_factor = row['budget_factor']
        fid = row['fid']
        dim = row['dim']
        budget = row['budget']
        
        # 获取dt_fb中该组合的数据
        dt_fb_data = dt_fb[
            (dt_fb['budget_factor'] == budget_factor) & 
            (dt_fb['fid'] == fid) & 
            (dt_fb['dim'] == dim) & 
            (dt_fb['budget'] == budget)
        ].copy()
        
        # 获取correct中该组合的数据
        correct_data = correct[
            (correct['budget_factor'] == budget_factor) & 
            (correct['fid'] == fid) & 
            (correct['dim'] == dim) & 
            (correct['budget'] == budget)
        ].copy()
        
        # 检查是否有数据
        if len(dt_fb_data) == 0 or len(correct_data) == 0:
            print(f"⚠️ 组合 F{fid}_{dim}D_budget{budget} 缺少数据")
            continue
        
        # 计算排名 (fx越小排名越好，所以用rank ascending=True)
        dt_fb_data['rank'] = dt_fb_data['fx'].rank(ascending=True, method='min')
        correct_data['rank'] = correct_data['fx'].rank(ascending=True, method='min')
        
        # 创建排名字典
        dt_fb_ranks = dict(zip(dt_fb_data['algname'], dt_fb_data['rank']))
        correct_ranks = dict(zip(correct_data['algname'], correct_data['rank']))
        
        # 检查排名是否一致
        common_algs = set(dt_fb_ranks.keys()) & set(correct_ranks.keys())
        
        if len(common_algs) < 2:
            print(f"⚠️ 组合 F{fid}_{dim}D_budget{budget} 共同算法少于2个")
            continue
        
        # 比较排名
        ranks_match = True
        for alg in common_algs:
            if dt_fb_ranks[alg] != correct_ranks[alg]:
                ranks_match = False
                break
        
        if ranks_match:
            ranking_matches += 1
        
        # 记录详细信息
        detail = {
            'combination': f"F{fid}_{dim}D_budget{budget}",
            'budget_factor': budget_factor,
            'fid': fid,
            'dim': dim,
            'budget': budget,
            'ranks_match': ranks_match,
            'dt_fb_ranks': dt_fb_ranks,
            'correct_ranks': correct_ranks,
            'dt_fb_fx': dict(zip(dt_fb_data['algname'], dt_fb_data['fx'])),
            'correct_fx': dict(zip(correct_data['algname'], correct_data['fx']))
        }
        ranking_details.append(detail)
        
        # 打印结果
        status = "✅" if ranks_match else "❌"
        print(f"{status} F{fid}_{dim}D_budget{budget}: ", end="")
        
        if ranks_match:
            print("排名一致")
        else:
            print("排名不一致")
            for alg in sorted(common_algs):
                dt_rank = dt_fb_ranks[alg]
                cor_rank = correct_ranks[alg]
                dt_fx = dt_fb_data[dt_fb_data['algname']==alg]['fx'].iloc[0]
                cor_fx = correct_data[correct_data['algname']==alg]['fx'].iloc[0]
                print(f"    {alg}: dt_fb排名{dt_rank}(fx={dt_fx:.6f}) vs 标准排名{cor_rank}(fx={cor_fx:.6f})")
    
    # 计算一致性比例
    consistency_rate = ranking_matches / total_combinations if total_combinations > 0 else 0
    
    print("\n" + "=" * 80)
    print("📊 排名一致性总结")
    print("=" * 80)
    print(f"总测试组合数: {total_combinations}")
    print(f"排名一致组合数: {ranking_matches}")
    print(f"排名不一致组合数: {total_combinations - ranking_matches}")
    print(f"一致性比例: {consistency_rate:.2%}")
    
    if consistency_rate >= 0.8:
        print("✅ 排名一致性良好")
    elif consistency_rate >= 0.6:
        print("⚠️ 排名一致性一般")
    else:
        print("❌ 排名一致性较差")
    
    # 保存详细结果
    if ranking_details:
        results_df = pd.DataFrame(ranking_details)
        results_df.to_csv("ranking_comparison_results.csv", index=False)
        print(f"\n详细排名比较结果已保存到: ranking_comparison_results.csv")
    
    return ranking_details, consistency_rate

def main():
    """
    主函数
    """
    print("=== 算法排名一致性比较工具 ===")
    
    # 检查文件是否存在
    dt_fb_exists = os.path.exists("dt_fb.csv")
    correct_exists = os.path.exists("f20-f24.xlsx")
    
    print(f"文件检查:")
    print(f"- dt_fb.csv: {'✅ 存在' if dt_fb_exists else '❌ 不存在'}")
    print(f"- f20-f24.xlsx: {'✅ 存在' if correct_exists else '❌ 不存在'}")
    
    if not dt_fb_exists:
        print("\n请先运行 dt_fb.py 生成 dt_fb.csv 文件")
        return
    
    if not correct_exists:
        print("\n请确保 f20-f24.xlsx 文件存在")
        return
    
    # 执行排名比较
    results = compare_algorithm_rankings()
    
    if results:
        print(f"\n排名比较完成！")
        print(f"详细结果请查看 ranking_comparison_results.csv")

if __name__ == "__main__":
    main()