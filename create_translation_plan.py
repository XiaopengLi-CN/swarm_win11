#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_translation_plan.py - 创建详细的Java翻译计划
"""

import os
import re
from collections import defaultdict

def analyze_modcma_files():
    """分析modcma文件"""
    
    modcma_dir = "modcma_source"
    files_analysis = {}
    
    # 分析每个文件
    for file in os.listdir(modcma_dir):
        if file.endswith('.py'):
            file_path = os.path.join(modcma_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计行数
            lines = content.split('\n')
            line_count = len(lines)
            
            # 统计类数量
            class_count = len(re.findall(r'^class\s+\w+', content, re.MULTILINE))
            
            # 统计函数数量
            function_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
            
            # 统计导入数量
            import_count = len(re.findall(r'^import\s+|^from\s+', content, re.MULTILINE))
            
            files_analysis[file] = {
                'lines': line_count,
                'classes': class_count,
                'functions': function_count,
                'imports': import_count,
                'content': content[:500] + '...' if len(content) > 500 else content
            }
    
    return files_analysis

def create_detailed_translation_plan():
    """创建详细的翻译计划"""
    
    files_analysis = analyze_modcma_files()
    
    plan_content = """=== modcma库Java翻译详细计划 ===

## 1. 文件分析总结

"""
    
    total_lines = 0
    total_classes = 0
    total_functions = 0
    
    for file, analysis in files_analysis.items():
        plan_content += f"""
### {file}
- 行数: {analysis['lines']}
- 类数量: {analysis['classes']}
- 函数数量: {analysis['functions']}
- 导入数量: {analysis['imports']}
"""
        total_lines += analysis['lines']
        total_classes += analysis['classes']
        total_functions += analysis['functions']
    
    plan_content += f"""
## 2. 总体统计
- 总行数: {total_lines}
- 总类数: {total_classes}
- 总函数数: {total_functions}

## 3. 翻译优先级和计划

### 第一阶段: 核心文件 (必须翻译)
1. modularcmaes.py -> ModularCMAES.java
   - 核心算法实现
   - 主要类: ModularCMAES
   - 关键方法: __init__, run(), mutate(), select(), recombine()
   - 预计工作量: 高

2. parameters.py -> Parameters.java
   - 参数配置类
   - 主要类: Parameters, BIPOPParameters
   - 关键方法: 构造函数, 参数验证
   - 预计工作量: 中

3. __init__.py -> ModCMAESModule.java
   - 模块接口
   - 导出主要类和函数
   - 预计工作量: 低

### 第二阶段: 支持文件 (建议翻译)
4. population.py -> Population.java
   - 种群管理
   - 主要类: Population
   - 预计工作量: 中

5. sampling.py -> Sampling.java
   - 采样方法
   - 主要类: Halton, Sobol
   - 预计工作量: 中

6. utils.py -> Utils.java
   - 工具函数
   - 主要函数: timeit, ert
   - 预计工作量: 低

### 第三阶段: 扩展文件 (可选翻译)
7. asktellcmaes.py -> AskTellCMAES.java
   - Ask-Tell接口
   - 预计工作量: 中

8. __main__.py -> Main.java
   - 命令行接口
   - 预计工作量: 低

## 4. 翻译步骤详细计划

### 步骤1: 环境准备
- 创建Java项目结构
- 设置Maven依赖
- 配置开发环境

### 步骤2: 核心类翻译
1. 翻译Parameters类
   - 定义所有参数
   - 实现参数验证
   - 添加Java注解

2. 翻译ModularCMAES类
   - 实现构造函数
   - 翻译核心算法方法
   - 处理数值计算

### 步骤3: 支持类翻译
1. 翻译Population类
2. 翻译Sampling类
3. 翻译Utils类

### 步骤4: 接口和集成
1. 创建模块接口
2. 实现日志记录
3. 添加错误处理

### 步骤5: 测试和验证
1. 单元测试
2. 集成测试
3. 性能对比

## 5. 技术要点

### 数值计算
- 使用Apache Commons Math
- 处理矩阵运算
- 确保数值精度

### 随机数生成
- 使用Java Random类
- 实现相同的随机序列
- 处理种子设置

### 性能优化
- 使用并行计算
- 优化内存使用
- 减少对象创建

### 错误处理
- 添加参数验证
- 实现异常处理
- 提供错误信息

## 6. 文件映射表

| Python文件 | Java文件 | 优先级 | 预计工作量 |
|------------|----------|--------|------------|
| modularcmaes.py | ModularCMAES.java | 高 | 高 |
| parameters.py | Parameters.java | 高 | 中 |
| __init__.py | ModCMAESModule.java | 高 | 低 |
| population.py | Population.java | 中 | 中 |
| sampling.py | Sampling.java | 中 | 中 |
| utils.py | Utils.java | 中 | 低 |
| asktellcmaes.py | AskTellCMAES.java | 低 | 中 |
| __main__.py | Main.java | 低 | 低 |

## 7. 时间估算

### 第一阶段 (核心文件): 2-3天
- modularcmaes.py: 1-2天
- parameters.py: 0.5-1天
- __init__.py: 0.5天

### 第二阶段 (支持文件): 1-2天
- population.py: 0.5-1天
- sampling.py: 0.5-1天
- utils.py: 0.5天

### 第三阶段 (测试验证): 1-2天
- 单元测试: 0.5-1天
- 集成测试: 0.5-1天
- 性能优化: 0.5天

### 总计: 4-7天

## 8. 风险点

1. 数值精度差异
2. 随机数序列不同
3. 性能问题
4. 算法逻辑错误

## 9. 成功标准

1. 功能正确性: 与Python版本结果一致
2. 性能要求: 运行时间可接受
3. 代码质量: 清晰、可维护
4. 文档完整: 注释和文档齐全
"""
    
    with open("detailed_translation_plan.txt", 'w', encoding='utf-8') as f:
        f.write(plan_content)
    
    print("详细翻译计划已保存到: detailed_translation_plan.txt")
    
    return plan_content

def create_file_comparison():
    """创建文件对比表"""
    
    files_analysis = analyze_modcma_files()
    
    comparison_content = "=== 文件详细对比表 ===\n\n"
    
    for file, analysis in files_analysis.items():
        comparison_content += f"""
文件: {file}
行数: {analysis['lines']}
类数: {analysis['classes']}
函数数: {analysis['functions']}
导入数: {analysis['imports']}

内容预览:
{analysis['content']}

{'='*50}
"""
    
    with open("file_comparison.txt", 'w', encoding='utf-8') as f:
        f.write(comparison_content)
    
    print("文件对比表已保存到: file_comparison.txt")

if __name__ == "__main__":
    print("开始创建详细翻译计划...")
    
    # 创建详细翻译计划
    plan = create_detailed_translation_plan()
    
    # 创建文件对比表
    create_file_comparison()
    
    print("\n翻译计划创建完成！")
