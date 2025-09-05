#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_modcma_source.py - 直接提取modcma库的源代码
"""

import os
import shutil
from pathlib import Path

def extract_modcma_source():
    """提取modcma库的源代码"""
    
    # modcma库的路径
    modcma_path = "env_new/Lib/site-packages/modcma"
    output_path = "modcma_source"
    
    if not os.path.exists(modcma_path):
        print(f"错误: 找不到modcma库路径: {modcma_path}")
        return
    
    # 创建输出目录
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)
    
    # 复制所有Python文件
    copied_files = []
    for root, dirs, files in os.walk(modcma_path):
        for file in files:
            if file.endswith('.py'):
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, modcma_path)
                dst_file = os.path.join(output_path, rel_path)
                
                # 创建目标目录
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                
                # 复制文件
                shutil.copy2(src_file, dst_file)
                copied_files.append(rel_path)
    
    print(f"成功提取了 {len(copied_files)} 个Python文件:")
    for file in sorted(copied_files):
        print(f"  - {file}")
    
    # 创建文件列表
    with open(os.path.join(output_path, "file_list.txt"), 'w', encoding='utf-8') as f:
        f.write("=== modcma库文件列表 ===\n\n")
        for file in sorted(copied_files):
            f.write(f"{file}\n")
    
    print(f"\n文件列表已保存到: {output_path}/file_list.txt")
    
    return output_path, copied_files

def analyze_modcma_structure():
    """分析modcma库结构"""
    
    modcma_path = "env_new/Lib/site-packages/modcma"
    
    if not os.path.exists(modcma_path):
        print(f"错误: 找不到modcma库路径: {modcma_path}")
        return
    
    print("=== modcma库结构分析 ===\n")
    
    # 分析目录结构
    for root, dirs, files in os.walk(modcma_path):
        level = root.replace(modcma_path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f"{subindent}{file}")
    
    # 查找主要文件
    main_files = []
    for root, dirs, files in os.walk(modcma_path):
        for file in files:
            if file.endswith('.py'):
                rel_path = os.path.relpath(os.path.join(root, file), modcma_path)
                main_files.append(rel_path)
    
    print(f"\n=== 主要Python文件 ===")
    for file in sorted(main_files):
        print(f"  - {file}")

def create_translation_guide():
    """创建翻译指南"""
    
    guide_content = """
=== modcma库Java翻译指南 ===

## 1. 核心文件分析

### 主要文件:
- __init__.py - 模块初始化文件
- modularcmaes.py - 核心CMA-ES实现
- parameters.py - 参数定义
- utils.py - 工具函数

## 2. 翻译优先级

### 高优先级 (必须翻译):
1. modularcmaes.py - 核心算法实现
2. parameters.py - 参数配置
3. __init__.py - 模块接口

### 中优先级 (建议翻译):
1. utils.py - 工具函数
2. 其他辅助文件

### 低优先级 (可选翻译):
1. 测试文件
2. 文档文件

## 3. 翻译步骤

### 第一步: 分析核心类
- ModularCMAES类
- 构造函数参数
- run()方法
- 内部算法逻辑

### 第二步: 翻译数据结构
- 参数类
- 配置类
- 结果类

### 第三步: 翻译算法逻辑
- 种群初始化
- 选择操作
- 重组操作
- 变异操作
- 适应度评估

### 第四步: 测试验证
- 单元测试
- 集成测试
- 性能对比

## 4. 注意事项

1. 保持算法逻辑一致性
2. 注意数值精度
3. 处理随机数生成
4. 优化性能
5. 添加详细注释

## 5. 文件映射

Python文件 -> Java文件:
- modularcmaes.py -> ModularCMAES.java
- parameters.py -> Parameters.java
- utils.py -> Utils.java
- __init__.py -> ModCMAESModule.java
"""
    
    with open("modcma_translation_guide.txt", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("翻译指南已保存到: modcma_translation_guide.txt")

if __name__ == "__main__":
    print("开始提取modcma库源代码...")
    
    # 提取源代码
    output_path, files = extract_modcma_source()
    
    # 分析结构
    analyze_modcma_structure()
    
    # 创建翻译指南
    create_translation_guide()
    
    print("\n提取完成！")
