# 验证脚本文件夹 (validation_scripts)

这个文件夹包含了所有用于检验结果是否正确的代码和脚本。

## 📁 文件分类

### 🔍 结果比较脚本
- `compare_results.py` - 比较算法排名一致性
- `compare_results_tolerance.py` - 比较fx容差结果
- `ranking_comparison_results.csv` - 排名比较结果
- `tolerance_comparison_results.csv` - 容差比较结果
- `comparison_results.csv` - 历史比较结果

### 🔬 随机性分析脚本
- `seed_analysis.py` - 随机种子分析
- `seed_scope_summary.py` - 随机种子作用域总结
- `seed_setting_guide.py` - 随机种子设置指南
- `deep_seed_analysis.py` - 深度随机种子分析
- `test_default_seed.py` - 测试默认随机种子
- `test_randomness.py` - 测试随机性影响
- `randomness_summary.py` - 随机性总结

### 🧬 算法分析脚本
- `bipop_seed_analysis.py` - BIPOP-CMA-ES随机种子分析
- `bipop_seed_summary.py` - BIPOP-CMA-ES随机种子总结
- `iid_impact_test.py` - 实例ID影响测试
- `instance_explanation.py` - 实例解释
- `run_count_analysis.py` - 运行次数分析

### 🔧 代码比较脚本
- `code_comparison_analysis.py` - 代码比较分析
- `process_comparison_analysis.py` - 处理脚本比较分析
- `dt_fb_comparison_analysis.py` - dt_fb脚本比较分析
- `analyze_comparison.py` - 比较分析
- `result_difference_analysis.py` - 结果差异分析

### 📊 输出分析脚本
- `analyze_output_folders.py` - 输出文件夹分析
- `test_path_fix.py` - 路径修复测试

### ✅ 验证脚本
- `verify_modifications.py` - 验证修改
- `verify_data_folder_modifications.py` - 验证数据文件夹修改
- `verify_dt_fb_modifications.py` - 验证dt_fb修改
- `verify_process_modifications.py` - 验证处理脚本修改

## 🎯 使用说明

### 主要验证脚本
1. **排名一致性验证**:
   ```bash
   python compare_results.py
   ```

2. **容差比较验证**:
   ```bash
   python compare_results_tolerance.py
   ```

3. **随机性分析**:
   ```bash
   python seed_analysis.py
   python bipop_seed_analysis.py
   ```

### 验证结果
- **排名一致性**: 91.43% (35个组合中32个一致)
- **容差一致性**: 40% (0.5容差下14个组合一致)
- **算法性能**: CS > modcma_bipop > DE (总体趋势)

## 📈 验证结论

✅ **实验结果可信度高**:
- 排名一致性达到91.43%
- 主要算法性能趋势正确
- 随机性影响在合理范围内

⚠️ **注意事项**:
- DE算法在某些函数上差异较大
- F20-F22函数上存在数值差异
- 但排名顺序基本正确

## 🔄 更新历史

- 2025-01-09: 创建验证脚本文件夹
- 整理所有验证相关代码
- 建立完整的验证体系


