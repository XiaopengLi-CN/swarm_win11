#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dt_fb_comparison_analysis.py - 分析Vizualization_teacher.ipynb与dt_fb.py的差异
"""

def analyze_dt_fb_differences():
    """
    分析两个处理脚本的差异
    """
    print("=" * 80)
    print("🔍 Vizualization_teacher.ipynb vs dt_fb.py 差异分析")
    print("=" * 80)
    
    print("\n📊 主要差异对比:")
    print("┌─────────────────────────────────────────────────────────┐")
    print("│ 项目                    │ 教师代码                    │ 当前代码                    │")
    print("├─────────────────────────────────────────────────────────┤")
    print("│ 数据源                   │ FBUDGET_{libname}.csv      │ FBUDGET_all.csv             │")
    print("│ 处理方式                 │ 循环处理多个库文件          │ 直接处理合并文件            │")
    print("│ 库信息添加               │ 从文件名推断               │ 从algname推断               │")
    print("│ 删除列                   │ ['fname', 'run', 'iid']    │ ['fname', 'run', 'iid']     │")
    print("│ fx变换                   │ np.log10(np.clip(...))     │ np.log10(np.clip(...))      │")
    print("│ 分组聚合                 │ groupby + agg('mean')      │ groupby + agg('mean')       │")
    print("│ 输出文件                 │ dt_fb.csv                  │ dt_fb.csv                  │")
    print("└─────────────────────────────────────────────────────────┘")
    
    print("\n🔍 详细差异分析:")
    
    print("\n1️⃣ 数据源差异:")
    print("   教师代码:")
    print("   ```python")
    print("   for libname in libnames:")
    print("       dt = pd.read_csv(f'{DIRNAME_CSV}/FBUDGET_{libname}.csv', index_col=0)")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   dt = pd.read_csv('CSV_Results/FBUDGET_all.csv')")
    print("   ```")
    print("   影响: 数据源不同，但内容应该相同")
    
    print("\n2️⃣ 库信息添加:")
    print("   教师代码:")
    print("   ```python")
    print("   dt['lib'] = libname")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   def get_lib(algname):")
    print("       if algname == 'modcma_bipop': return 'Baselines'")
    print("       elif algname in ['CS', 'DE']: return 'OPYTIMIZER'")
    print("   dt['lib'] = dt['algname'].apply(get_lib)")
    print("   ```")
    print("   影响: 库信息添加方式不同，但结果应该相同")
    
    print("\n3️⃣ 数据处理流程:")
    print("   教师代码:")
    print("   ```python")
    print("   dt = dt.drop(['fname', 'run', 'iid'], axis=1)")
    print("   dt['fx'] = np.log10(np.clip(dt['fx'], 1e-8, 1e16))")
    print("   dt['lib'] = libname")
    print("   dt_fb = dt.groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean').reset_index()")
    print("   ```")
    print("   当前代码:")
    print("   ```python")
    print("   dt = dt.drop(['fname', 'run', 'iid'], axis=1)")
    print("   dt['fx'] = np.log10(np.clip(dt['fx'], 1e-8, 1e16))")
    print("   dt['lib'] = dt['algname'].apply(get_lib)")
    print("   dt_fb = dt.groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean').reset_index()")
    print("   ```")
    print("   影响: 处理流程基本相同，只是库信息添加方式不同")

def identify_critical_differences():
    """
    识别影响结果的关键差异
    """
    print("\n🎯 影响结果的关键差异:")
    
    print("\n❌ 关键差异1: 数据源不同")
    print("   教师代码: 分别读取FBUDGET_Baselines.csv和FBUDGET_OPYTIMIZER.csv")
    print("   当前代码: 直接读取FBUDGET_all.csv")
    print("   影响: 数据源不同可能导致处理顺序或精度差异")
    
    print("\n❌ 关键差异2: 库信息添加方式不同")
    print("   教师代码: 从文件名直接获取库名")
    print("   当前代码: 从算法名推断库名")
    print("   影响: 可能在某些边界情况下产生不同的库名")
    
    print("\n✅ 相同的地方:")
    print("   - 删除的列相同: ['fname', 'run', 'iid']")
    print("   - fx变换相同: np.log10(np.clip(dt['fx'], 1e-8, 1e16))")
    print("   - 分组聚合相同: groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean')")
    print("   - 输出文件相同: dt_fb.csv")

def provide_modification_plan():
    """
    提供修改计划
    """
    print("\n🔧 修改计划:")
    
    print("\n1️⃣ 修改数据源:")
    print("   使用分库文件而不是合并文件")
    print("   ```python")
    print("   libnames = ['Baselines', 'OPYTIMIZER']")
    print("   dts = []")
    print("   for libname in libnames:")
    print("       dt = pd.read_csv(f'CSV_Results/FBUDGET_{libname}.csv', index_col=0)")
    print("       dt['lib'] = libname")
    print("       dts.append(dt)")
    print("   dt = pd.concat(dts)")
    print("   ```")
    
    print("\n2️⃣ 修改库信息添加:")
    print("   直接从文件名获取库名")
    print("   ```python")
    print("   dt['lib'] = libname")
    print("   ```")
    
    print("\n3️⃣ 保持其他处理不变:")
    print("   - 删除列: ['fname', 'run', 'iid']")
    print("   - fx变换: np.log10(np.clip(dt['fx'], 1e-8, 1e16))")
    print("   - 分组聚合: groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean')")

def explain_impact():
    """
    解释差异的影响
    """
    print("\n💡 差异影响分析:")
    
    print("\n🔍 数据源差异的影响:")
    print("1. 分库文件 vs 合并文件:")
    print("   - 分库文件处理更精确，保持原始结构")
    print("   - 合并文件可能在某些情况下丢失精度")
    print("   - 处理顺序可能不同")
    
    print("\n2. 库信息添加差异的影响:")
    print("   - 教师代码直接从文件名获取库名，更可靠")
    print("   - 当前代码从算法名推断，可能在某些情况下出错")
    print("   - 如果算法名映射不完整，可能导致库名错误")
    
    print("\n3. 处理流程差异的影响:")
    print("   - 教师代码的处理流程更标准")
    print("   - 当前代码的处理流程可能在某些边界情况下产生不同结果")
    
    print("\n🎯 结论:")
    print("这些差异可能导致:")
    print("1. 库名分配错误")
    print("2. 数据处理顺序不同")
    print("3. 最终结果格式不一致")

def check_teacher_code_details():
    """
    检查教师代码的具体细节
    """
    print("\n🔍 教师代码具体细节:")
    
    print("\n📝 Cell 12 - FBUDGET数据处理:")
    print("```python")
    print("dts = []")
    print("for libname in libnames:")
    print("    dt = pd.read_csv(f'{DIRNAME_CSV}/FBUDGET_{libname}.csv', index_col=0)")
    print("    dt = dt.drop(['fname', 'run', 'iid'], axis=1)")
    print("    dt['fx'] = np.log10(np.clip(dt['fx'], 1e-8, 1e16))")
    print("    dt['lib'] = libname")
    print("    dt_fb = dt.groupby(['budget_factor', 'algname', 'fid', 'dim', 'lib']).agg('mean').reset_index()")
    print("    dts.append(dt_fb)")
    print("dt_fb = pd.concat(dts)")
    print("```")
    
    print("\n📝 Cell 16 - 保存文件:")
    print("```python")
    print("dt_fb.to_csv('dt_fb.csv')")
    print("```")
    
    print("\n🎯 关键点:")
    print("1. 使用index_col=0读取CSV")
    print("2. 分别处理每个库的文件")
    print("3. 直接从libname变量获取库名")
    print("4. 最后合并所有库的数据")

if __name__ == "__main__":
    analyze_dt_fb_differences()
    identify_critical_differences()
    provide_modification_plan()
    explain_impact()
    check_teacher_code_details()
    
    print("\n" + "=" * 80)
    print("总结: dt_fb.py需要修改以与教师代码保持一致")
    print("=" * 80)
