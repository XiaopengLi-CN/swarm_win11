#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_output_folders.py - 分析修改后的benchmark脚本结果保存位置
"""

def analyze_output_folders():
    """
    分析修改后的benchmark脚本结果保存位置
    """
    print("=" * 80)
    print("🔍 修改后的benchmark脚本结果保存位置分析")
    print("=" * 80)
    
    print("\n📊 关键变量分析:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 脚本                    │ DATA_FOLDER  │ 结果保存位置        │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ benchmark_baselines.py  │ '' (空字符串) │ ./Baselines/        │")
    print("│ benchmark_optymizer.py   │ '' (空字符串) │ ./OPYTIMIZER/       │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🔍 详细分析:")
    
    print("\n1️⃣ benchmark_baselines.py:")
    print("   - DATA_FOLDER = '' (空字符串)")
    print("   - 结果保存位置: f'{DATA_FOLDER}/Baselines/'")
    print("   - 实际路径: './Baselines/'")
    print("   - 文件夹结构: Baselines/modcma_bipop_F{fid}_I{iid}_{dim}D/")
    print("   - 文件示例: Baselines/modcma_bipop_F20_I1_10D/IOHprofiler_f20_Sphere.dat")
    
    print("\n2️⃣ benchmark_optymizer.py:")
    print("   - DATA_FOLDER = '' (空字符串)")
    print("   - 结果保存位置: f'{DATA_FOLDER}/OPYTIMIZER/'")
    print("   - 实际路径: './OPYTIMIZER/'")
    print("   - 文件夹结构: OPYTIMIZER/{algname}_F{fid}_I{iid}_{dim}D/")
    print("   - 文件示例: OPYTIMIZER/CS_F20_I1_10D/IOHprofiler_f20_Sphere.dat")
    
    print("\n📁 完整的文件夹结构:")
    print("```")
    print("项目根目录/")
    print("├── Baselines/")
    print("│   ├── modcma_bipop_F20_I1_10D/")
    print("│   │   └── IOHprofiler_f20_Sphere.dat")
    print("│   ├── modcma_bipop_F20_I2_10D/")
    print("│   │   └── IOHprofiler_f20_Sphere.dat")
    print("│   ├── ... (F20-F24, I1-I10)")
    print("│   └── modcma_bipop_F24_I10_10D/")
    print("│       └── IOHprofiler_f24_Sphere.dat")
    print("└── OPYTIMIZER/")
    print("    ├── CS_F20_I1_10D/")
    print("    │   └── IOHprofiler_f20_Sphere.dat")
    print("    ├── CS_F20_I2_10D/")
    print("    │   └── IOHprofiler_f20_Sphere.dat")
    print("    ├── DE_F20_I1_10D/")
    print("    │   └── IOHprofiler_f20_Sphere.dat")
    print("    ├── ... (CS/DE, F20-F24, I1-I10)")
    print("    └── DE_F24_I10_10D/")
    print("        └── IOHprofiler_f24_Sphere.dat")
    print("```")

def analyze_file_naming():
    """
    分析文件命名规则
    """
    print("\n🔍 文件命名规则分析:")
    
    print("\n📝 benchmark_baselines.py:")
    print("   - 算法名: modcma_bipop")
    print("   - 函数ID: F20-F24")
    print("   - 实例ID: I1-I10")
    print("   - 维度: 10D")
    print("   - 文件夹名: modcma_bipop_F{fid}_I{iid}_{dim}D")
    print("   - 数据文件名: IOHprofiler_f{fid}_Sphere.dat")
    
    print("\n📝 benchmark_optymizer.py:")
    print("   - 算法名: CS, DE")
    print("   - 函数ID: F20-F24")
    print("   - 实例ID: I1-I10")
    print("   - 维度: 10D")
    print("   - 文件夹名: {algname}_F{fid}_I{iid}_{dim}D")
    print("   - 数据文件名: IOHprofiler_f{fid}_Sphere.dat")
    
    print("\n📊 文件数量统计:")
    print("   - Baselines: 1个算法 × 5个函数 × 10个实例 × 1个维度 = 50个文件夹")
    print("   - OPYTIMIZER: 2个算法 × 5个函数 × 10个实例 × 1个维度 = 100个文件夹")
    print("   - 总计: 150个文件夹，每个包含1个.dat文件")

def analyze_data_flow():
    """
    分析数据流向
    """
    print("\n🔄 数据流向分析:")
    
    print("\n1️⃣ 数据生成阶段:")
    print("   benchmark_baselines.py → ./Baselines/")
    print("   benchmark_optymizer.py → ./OPYTIMIZER/")
    
    print("\n2️⃣ 数据预处理阶段:")
    print("   simple_process.py 读取:")
    print("   - ./Baselines/*/*/IOHprofiler_f*.dat")
    print("   - ./OPYTIMIZER/*/*/IOHprofiler_f*.dat")
    print("   输出:")
    print("   - ./FBUDGET_Baselines.csv")
    print("   - ./FBUDGET_OPYTIMIZER.csv")
    print("   - ./FBUDGET_all.csv")
    
    print("\n3️⃣ 数据后处理阶段:")
    print("   dt_fb.py 读取:")
    print("   - ./FBUDGET_Baselines.csv")
    print("   - ./FBUDGET_OPYTIMIZER.csv")
    print("   输出:")
    print("   - ./dt_fb.csv")
    
    print("\n4️⃣ 结果比较阶段:")
    print("   compare_results.py 读取:")
    print("   - ./dt_fb.csv")
    print("   - ./f20-f24.xlsx")
    print("   输出:")
    print("   - ./ranking_comparison_results.csv")

def check_folder_creation():
    """
    检查文件夹创建逻辑
    """
    print("\n🔍 文件夹创建逻辑:")
    
    print("\n📝 IOH Logger创建:")
    print("   benchmark_baselines.py:")
    print("   ```python")
    print("   logger = ioh.logger.Analyzer(root=f'{DATA_FOLDER}/Baselines/',")
    print("                                folder_name=f'{algname}_F{fid}_I{iid}_{dim}D',")
    print("                                algorithm_name=f'{algname}')")
    print("   ```")
    print("   ")
    print("   benchmark_optymizer.py:")
    print("   ```python")
    print("   logger = ioh.logger.Analyzer(root=f'{DATA_FOLDER}/OPYTIMIZER/',")
    print("                                folder_name=f'{algname}_F{fid}_I{iid}_{dim}D',")
    print("                                algorithm_name=f'{algname}')")
    print("   ```")
    
    print("\n✅ 自动创建:")
    print("   - IOH Logger会自动创建所需的文件夹结构")
    print("   - 不需要手动创建文件夹")
    print("   - 如果文件夹不存在，会自动创建")

def provide_summary():
    """
    提供总结
    """
    print("\n📋 总结:")
    
    print("\n🎯 修改后的结果保存位置:")
    print("1. benchmark_baselines.py → ./Baselines/")
    print("2. benchmark_optymizer.py → ./OPYTIMIZER/")
    
    print("\n📁 文件夹结构:")
    print("   - Baselines/: 50个文件夹，包含modcma_bipop算法结果")
    print("   - OPYTIMIZER/: 100个文件夹，包含CS和DE算法结果")
    
    print("\n📄 文件内容:")
    print("   - 每个文件夹包含1个IOHprofiler_f{fid}_Sphere.dat文件")
    print("   - 文件包含5次独立运行的优化结果")
    print("   - 数据格式符合IOHprofiler标准")
    
    print("\n🔄 后续处理:")
    print("   - simple_process.py会读取这些.dat文件")
    print("   - 生成CSV格式的汇总数据")
    print("   - dt_fb.py进一步处理生成最终结果")

if __name__ == "__main__":
    analyze_output_folders()
    analyze_file_naming()
    analyze_data_flow()
    check_folder_creation()
    provide_summary()
    
    print("\n" + "=" * 80)
    print("总结: 修改后的脚本结果保存在./Baselines/和./OPYTIMIZER/文件夹下")
    print("=" * 80)
