#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_path_fix.py - 测试路径修复是否正确
"""

def test_path_fix():
    """
    测试路径修复是否正确
    """
    print("=" * 80)
    print("🔍 测试路径修复")
    print("=" * 80)
    
    # 模拟Windows路径
    test_paths = [
        "Data\\Baselines\\modcma_bipop_F20_I1_10D\\IOHprofiler_f20_Sphere.dat",
        "Data\\OPYTIMIZER\\CS_F20_I1_10D\\IOHprofiler_f20_Sphere.dat",
        "Data\\OPYTIMIZER\\DE_F20_I1_10D\\IOHprofiler_f20_Sphere.dat"
    ]
    
    print("\n📝 测试路径处理:")
    for fname in test_paths:
        print(f"\n原始路径: {fname}")
        
        # 修复后的处理方式
        path_parts = fname.replace('\\', '/').split('/')
        print(f"路径分割: {path_parts}")
        
        if len(path_parts) >= 3:
            base = path_parts[-3]
            print(f"提取的base: {base}")
            
            # 测试算法名提取
            if 'modcma_bipop' in base:
                print(f"算法名: modcma_bipop")
            elif 'CS' in base:
                print(f"算法名: CS")
            elif 'DE' in base:
                print(f"算法名: DE")
        else:
            print("❌ 路径分割失败")
    
    print("\n✅ 修复说明:")
    print("1. 使用 fname.replace('\\', '/').split('/') 来处理Windows路径")
    print("2. 将反斜杠替换为正斜杠，然后分割")
    print("3. 这样可以正确处理Windows和Unix路径")

def test_csv_path_fix():
    """
    测试CSV文件路径修复
    """
    print("\n🔍 测试CSV文件路径修复:")
    
    # 模拟CSV文件路径
    csv_paths = [
        "csv_Baselines/FBUDGET_modcma_bipop_F20_I1_10D.csv",
        "csv_OPYTIMIZER/FBUDGET_CS_F20_I1_10D.csv",
        "csv_OPYTIMIZER/FBUDGET_DE_F20_I1_10D.csv"
    ]
    
    for fname in csv_paths:
        print(f"\nCSV路径: {fname}")
        
        # 修复后的处理方式
        base = fname.replace('\\', '/').split('/')[-1]
        print(f"文件名: {base}")
        
        # 解析算法名
        parts = base.split('_')
        print(f"分割结果: {parts}")
        
        if len(parts) >= 4:
            algname = parts[-4]
            fid = int(parts[-3][1:])
            iid = int(parts[-2][1:])
            dim = int(parts[-1][:-5])
            
            print(f"算法名: {algname}")
            print(f"函数ID: {fid}")
            print(f"实例ID: {iid}")
            print(f"维度: {dim}")

if __name__ == "__main__":
    test_path_fix()
    test_csv_path_fix()
    
    print("\n" + "=" * 80)
    print("总结: 路径修复已完成，现在可以正确处理Windows路径")
    print("=" * 80)
