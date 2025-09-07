# Java版本BIPOP-CMA-ES基准测试项目

## 📋 项目概述

这是Python版本`benchmark_baselines.py`的Java实现，用于在BBOB测试函数F20-F24上执行BIPOP-CMA-ES算法的基准测试。

## 🏗️ 项目架构

### 核心类结构

```
com.hse.li.swarm.eval/
├── Main.java                    # 主入口类
├── AlgorithmEvaluator.java     # 算法评估器
├── ObjectiveFunction.java      # 目标函数接口
├── BBOBFunction.java           # BBOB测试函数实现
├── ResultLogger.java           # 结果记录器
├── ParallelExecutor.java       # 并行执行管理器
└── OptimizationTask.java       # 优化任务参数类
```

### 类功能说明

1. **Main.java** - 主基准测试类
   - 对应Python中的`benchmark_baselines.py`
   - 负责生成测试任务和协调执行

2. **AlgorithmEvaluator.java** - 算法评估器
   - 对应Python中的`Algorithm_Evaluator`类
   - 实现BIPOP-CMA-ES算法逻辑

3. **BBOBFunction.java** - BBOB测试函数
   - 对应Python中的`ioh.get_problem`
   - 实现F20-F24测试函数

4. **ResultLogger.java** - 结果记录器
   - 对应Python中的IOH logger
   - 负责记录和保存测试结果

5. **ParallelExecutor.java** - 并行执行器
   - 对应Python中的`runParallelFunction`
   - 管理多线程并行执行

## 🚀 运行配置

### 测试参数
- **函数范围**: F20-F24 (5个函数)
- **实例范围**: I1-I10 (10个实例)
- **维度**: 10D
- **重复次数**: 5次
- **总任务数**: 5 × 10 × 1 × 5 = 250个任务

### 输出结构
```
Data/
└── Baselines/
    ├── modcma_bipop_F20_I1_10D/
    │   └── IOHprofiler_f20_Sphere.csv
    ├── modcma_bipop_F20_I2_10D/
    │   └── IOHprofiler_f20_Sphere.csv
    └── ...
```

## 📦 依赖库

### Maven依赖
- **Apache Commons Math 3.6.1** - 数学计算和优化算法
- **Apache Commons Lang 3.12.0** - 工具类
- **Apache Commons CSV 1.9.0** - CSV文件处理
- **SLF4J + Logback** - 日志记录
- **Jackson** - JSON处理

## 🔧 编译和运行

### 1. 编译项目
```bash
cd swarm-java
mvn clean compile
```

### 2. 运行基准测试
```bash
mvn exec:java -Dexec.mainClass="com.hse.li.swarm.eval.Main"
```

### 3. 打包项目
```bash
mvn clean package
```

## 📊 输出说明

### 日志输出
- **控制台**: 实时显示执行进度
- **文件**: `logs/benchmark.log` 详细日志

### 结果文件
- **CSV格式**: 包含run, evaluation, fitness, solution列
- **位置**: `Data/Baselines/[任务名]/IOHprofiler_f[函数ID]_Sphere.csv`

## ⚠️ 注意事项

### 算法实现
- 当前BIPOP-CMA-ES实现为简化版本
- 实际项目中可能需要更复杂的算法实现
- 建议使用专业的优化算法库

### 性能考虑
- 默认最大线程数: 32
- 可根据机器配置调整`MAX_THREADS`
- 建议在性能较好的机器上运行

### 扩展性
- 易于添加新的测试函数
- 支持添加新的优化算法
- 可配置测试参数

## 🔄 与Python版本对比

| 功能 | Python版本 | Java版本 |
|------|------------|----------|
| 算法实现 | modcma库 | 简化实现 |
| 并行执行 | multiprocessing | ExecutorService |
| 结果记录 | IOH logger | CSV文件 |
| 配置管理 | 硬编码 | 常量定义 |
| 日志记录 | print | SLF4J |

## 📝 开发说明

### 代码特点
- **面向对象设计**: 清晰的类结构和职责分离
- **异常处理**: 完善的错误处理机制
- **日志记录**: 详细的执行日志
- **可扩展性**: 易于添加新功能

### 改进建议
1. 实现完整的BIPOP-CMA-ES算法
2. 添加更多BBOB测试函数
3. 支持配置文件管理
4. 添加性能监控
5. 实现结果可视化

## 🎯 下一步计划

1. **测试Java实现** - 验证功能正确性
2. **性能优化** - 提升执行效率
3. **算法完善** - 实现完整算法
4. **结果分析** - 添加结果分析功能

