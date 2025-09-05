#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_comparison_analysis.py - 分析process_bestiary_fixedbudget.py与simple_process.py的差异
"""

def analyze_process_differences():
    """
    分析两个处理脚本的差异
    """
    print("=" * 80)
    print("🔍 process_bestiary_fixedbudget.py vs simple_process.py 差异分析")
    print("=" * 80)
    
    print("\n📊 主要差异对比:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 项目                    │ 教师代码                    │ 当前代码                    │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ DATA_FOLDER             │ '' (空字符串)               │ 'Data'                      │")
    print("│ CSV_FOLDER              │ '' (空字符串)               │ 'CSV_Results'               │")
    print("│ budget_factors          │ [10,50,100,500,1000,5000,10000] │ [10,50,100,500,1000,5000,10000] │")
    print("│ 文件查找方式             │ glob.glob()                 │ os.walk()                   │")
    print("│ 数据处理方式             │ pandas.read_csv()           │ 手动解析文本                │")
    print("│ 并行处理                │ multiprocessing.Pool        │ 串行处理                    │")
    print("│ 输出文件结构             │ 分库保存+合并               │ 直接合并                    │")
    print("│ 错误处理                │ try-except                  │ try-except                  │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🔍 详细差异分析:")
    
    print("\n1️⃣ 文件查找方式:")
    print("   教师代码:")
    print("   ```python")
    print("   files = glob.glob(f'{DATA_FOLDER}/{libname}/*/*/IOHprofiler_f*.dat')")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   for root, dirs, filenames in os.walk(f'{DATA_FOLDER}/Baselines'):")
    print("       for filename in filenames:")
    print("           if filename.endswith('.dat') and 'IOHprofiler' in filename:")
    print("   ```")
    print("   影响: 文件查找方式不同，但结果应该相同")
    
    print("\n2️⃣ 数据处理方式:")
    print("   教师代码:")
    print("   ```python")
    print("   dt = pd.read_csv(fname, sep=' ', decimal=',')")
    print("   dt = dt[dt['raw_y'] != 'raw_y'].astype(float)")
    print("   dt['run_id'] = np.cumsum(dt['evaluations'] == 1)")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   runs = content.strip().split('evaluations raw_y')[1:]")
    print("   # 手动解析每行数据")
    print("   ```")
    print("   影响: 数据处理方式完全不同！这是关键差异")
    
    print("\n3️⃣ 预算计算:")
    print("   教师代码:")
    print("   ```python")
    print("   min(dt_temp.query(f'evaluations <= {budget * dim}')['raw_y'])")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   valid_items = [item for item in run_items if item[0] <= budget_eval]")
    print("   min_y = min(item[1] for item in valid_items)")
    print("   ```")
    print("   影响: 逻辑相同，但实现方式不同")
    
    print("\n4️⃣ 输出结构:")
    print("   教师代码:")
    print("   - 先为每个库创建单独的CSV文件")
    print("   - 然后合并所有库的CSV文件")
    print("   - 输出: FBUDGET_Baselines.csv, FBUDGET_OPYTIMIZER.csv")
    print("   当前代码:")
    print("   - 直接合并所有数据")
    print("   - 输出: FBUDGET_all.csv")
    print("   影响: 输出文件结构不同")

def identify_critical_differences():
    """
    识别影响结果的关键差异
    """
    print("\n🎯 影响结果的关键差异:")
    
    print("\n❌ 关键差异1: 数据处理方式")
    print("   教师代码使用pandas.read_csv()解析.dat文件")
    print("   当前代码使用手动文本解析")
    print("   影响: 可能导致数据解析错误或精度损失")
    
    print("\n❌ 关键差异2: 文件路径处理")
    print("   教师代码: DATA_FOLDER = ''")
    print("   当前代码: DATA_FOLDER = 'Data'")
    print("   影响: 文件查找路径不同")
    
    print("\n❌ 关键差异3: 输出文件结构")
    print("   教师代码: 分库保存后合并")
    print("   当前代码: 直接合并")
    print("   影响: 中间处理步骤不同")
    
    print("\n✅ 相同的地方:")
    print("   - budget_factors列表相同")
    print("   - 预算计算逻辑相同")
    print("   - 最小适应度选择逻辑相同")

def provide_modification_plan():
    """
    提供修改计划
    """
    print("\n🔧 修改计划:")
    
    print("\n1️⃣ 修改DATA_FOLDER和CSV_FOLDER:")
    print("   ```python")
    print("   DATA_FOLDER = ''")
    print("   CSV_FOLDER = ''")
    print("   ```")
    
    print("\n2️⃣ 修改文件查找方式:")
    print("   使用glob.glob()替代os.walk()")
    print("   ```python")
    print("   files = glob.glob(f'{DATA_FOLDER}/{libname}/*/*/IOHprofiler_f*.dat')")
    print("   ```")
    
    print("\n3️⃣ 修改数据处理方式:")
    print("   使用pandas.read_csv()替代手动解析")
    print("   ```python")
    print("   dt = pd.read_csv(fname, sep=' ', decimal=',')")
    print("   dt = dt[dt['raw_y'] != 'raw_y'].astype(float)")
    print("   dt['run_id'] = np.cumsum(dt['evaluations'] == 1)")
    print("   ```")
    
    print("\n4️⃣ 修改输出结构:")
    print("   先分库保存，再合并")
    print("   保持与教师代码完全一致的处理流程")
    
    print("\n5️⃣ 添加并行处理:")
    print("   使用multiprocessing.Pool进行并行处理")

def explain_impact():
    """
    解释差异的影响
    """
    print("\n💡 差异影响分析:")
    
    print("\n🔍 数据处理方式差异的影响:")
    print("1. pandas.read_csv() vs 手动解析:")
    print("   - pandas更精确，处理各种边界情况")
    print("   - 手动解析可能遗漏某些数据格式")
    print("   - 可能导致数值精度差异")
    
    print("\n2. 文件路径差异的影响:")
    print("   - 教师代码查找当前目录下的文件")
    print("   - 当前代码查找Data目录下的文件")
    print("   - 可能导致找不到文件或找到错误的文件")
    
    print("\n3. 输出结构差异的影响:")
    print("   - 教师代码有中间处理步骤")
    print("   - 当前代码直接合并")
    print("   - 可能影响最终结果的顺序和格式")
    
    print("\n🎯 结论:")
    print("这些差异可能导致:")
    print("1. 数据解析错误")
    print("2. 数值精度差异")
    print("3. 文件处理顺序不同")
    print("4. 最终结果格式不一致")

if __name__ == "__main__":
    analyze_process_differences()
    identify_critical_differences()
    provide_modification_plan()
    explain_impact()
    
    print("\n" + "=" * 80)
    print("总结: 数据处理方式存在关键差异，需要修改以保持一致")
    print("=" * 80)
