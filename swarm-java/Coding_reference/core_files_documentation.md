# benchmark_baselines.py 核心文件详细文档

## 概述

本文档详细列出了`benchmark_baselines.py`运行时调用的11个核心文件。
这些文件是Java翻译的重点目标，按重要性和功能分类。

## 文件统计

| 类别 | 文件数量 | 重要性 |
|------|----------|--------|
| modcma核心文件 | 6 | 算法实现 |
| ioh核心文件 | 3 | 实验框架 |
| numpy核心文件 | 4 | 数值计算 |
| **总计** | **11** | **核心依赖** |

## modcma核心文件

### 1. __init__.py

**文件路径**: `env_new/Lib/site-packages/modcma/__init__.py`

**功能描述**: modcma库的主入口文件，定义模块接口

**重要性**: 高 - 模块导入入口

**状态**: ✅ 文件存在

**文件大小**: 779 字节

---

### 2. modularcmaes.py

**文件路径**: `env_new/Lib/site-packages/modcma/modularcmaes.py`

**功能描述**: ModularCMAES算法的主要实现文件

**重要性**: 最高 - 核心算法实现

**状态**: ✅ 文件存在

**文件大小**: 18,516 字节

---

### 3. parameters.py

**文件路径**: `env_new/Lib/site-packages/modcma/parameters.py`

**功能描述**: CMA-ES算法参数定义和配置

**重要性**: 高 - 参数管理

**状态**: ✅ 文件存在

**文件大小**: 37,492 字节

---

### 4. population.py

**文件路径**: `env_new/Lib/site-packages/modcma/population.py`

**功能描述**: 种群管理和操作相关功能

**重要性**: 高 - 种群操作

**状态**: ✅ 文件存在

**文件大小**: 3,981 字节

---

### 5. sampling.py

**文件路径**: `env_new/Lib/site-packages/modcma/sampling.py`

**功能描述**: 采样策略和分布相关功能

**重要性**: 高 - 采样算法

**状态**: ✅ 文件存在

**文件大小**: 4,107 字节

---

### 6. utils.py

**文件路径**: `env_new/Lib/site-packages/modcma/utils.py`

**功能描述**: 工具函数和辅助功能

**重要性**: 中 - 辅助功能

**状态**: ✅ 文件存在

**文件大小**: 8,412 字节

---

## ioh核心文件

### 1. __init__.py

**文件路径**: `env_new/Lib/site-packages/ioh/__init__.py`

**功能描述**: ioh库的主入口文件，提供get_problem等核心接口

**重要性**: 最高 - 问题获取接口

**状态**: ✅ 文件存在

**文件大小**: 22,580 字节

---

### 2. __init__.py

**文件路径**: `env_new/Lib/site-packages/ioh/logger/__init__.py`

**功能描述**: ioh日志系统的主入口

**重要性**: 高 - 日志系统入口

**状态**: ❌ 文件不存在

---

### 3. analyzer.py

**文件路径**: `env_new/Lib/site-packages/ioh/logger/analyzer.py`

**功能描述**: Analyzer日志记录器的具体实现

**重要性**: 最高 - 实验数据记录

**状态**: ❌ 文件不存在

---

## numpy核心文件

### 1. __init__.py

**文件路径**: `env_new/Lib/site-packages/numpy/__init__.py`

**功能描述**: numpy库的主入口文件

**重要性**: 高 - 数值计算基础

**状态**: ✅ 文件存在

**文件大小**: 17,542 字节

---

### 2. __init__.py

**文件路径**: `env_new/Lib/site-packages/numpy/core/__init__.py`

**功能描述**: numpy核心模块入口

**重要性**: 高 - 核心模块

**状态**: ✅ 文件存在

**文件大小**: 5,960 字节

---

### 3. numeric.py

**文件路径**: `env_new/Lib/site-packages/numpy/core/numeric.py`

**功能描述**: numpy.zeros等数值函数实现

**重要性**: 高 - 数值函数

**状态**: ✅ 文件存在

**文件大小**: 79,544 字节

---

### 4. __init__.py

**文件路径**: `env_new/Lib/site-packages/numpy/random/__init__.py`

**功能描述**: numpy随机数生成器

**重要性**: 高 - 随机数生成

**状态**: ✅ 文件存在

**文件大小**: 7,721 字节

---

