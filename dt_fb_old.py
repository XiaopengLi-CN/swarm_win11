#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dt_fb.py - 数据处理脚本
从 FBUDGET_all.csv 处理得到 dt_fb.csv
"""

import numpy as np
import pandas as pd
import os

def process_fbudget_data():
    """
    处理FBUDGET_all.csv数据，生成dt_fb.csv
    """
    print("正在处理固定预算数据...")
    
    # 检查输入文件是否存在
    if not os.path.exists("CSV_Results/FBUDGET_all.csv"):
        print("错误：找不到 CSV_Results/FBUDGET_all.csv 文件")
        return None
    
    # 读取FBUDGET_all.csv
    dt = pd.read_csv("CSV_Results/FBUDGET_all.csv")
    print(f"读取了 {len(dt)} 行原始数据")
    
    # 删除不需要的列
    dt = dt.drop(['fname', 'run', 'iid'], axis=1)
    
    # 对fx进行对数变换和裁剪
    dt['fx'] = np.log10(np.clip(dt['fx'], 1e-8, 1e16))
    
    # 添加库信息（根据algname判断）
    def get_lib(algname):
        if algname == 'modcma_bipop':
            return 'Baselines'
        elif algname in ['CS', 'DE']:
            return 'OPYTIMIZER'
        else:
            return 'Unknown'
    
    dt['lib'] = dt['algname'].apply(get_lib)
    
    # 按预算因子、算法名、函数ID、维度、库进行分组并计算平均值
    dt_fb = dt.groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean').reset_index()
    
    # 保存处理后的数据
    dt_fb.to_csv("dt_fb.csv", index=False)
    print(f"已保存 dt_fb.csv，包含 {len(dt_fb)} 行数据")
    
    # 显示数据统计信息
    print("\n数据统计信息：")
    print(f"预算因子范围: {dt_fb['budget_factor'].min()} - {dt_fb['budget_factor'].max()}")
    print(f"维度: {sorted(dt_fb['dim'].unique())}")
    print(f"算法: {sorted(dt_fb['algname'].unique())}")
    print(f"库: {sorted(dt_fb['lib'].unique())}")
    
    return dt_fb

def main():
    """
    主函数：处理数据
    """
    print("开始数据处理...")
    
    # 处理固定预算数据
    dt_fb = process_fbudget_data()
    
    if dt_fb is not None:
        print("\n数据处理完成！")
        print("生成的文件：")
        print("- dt_fb.csv: 处理后的固定预算数据")
    else:
        print("数据处理失败！")

if __name__ == "__main__":
    main()
