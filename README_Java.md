# Java版本群智能算法基准测试项目

## 项目简介
这是Python版本的群智能算法基准测试项目的Java翻译版本。目前实现了BIPOP-CMA-ES算法的基准测试。

## 项目结构
```
src/main/java/com/swarm/
├── algorithms/           # 算法实现
│   ├── BIPOPCMAES.java   # BIPOP-CMA-ES算法
│   ├── OptimizationAlgorithm.java  # 算法接口
│   └── OptimizationResult.java     # 优化结果类
├── benchmark/            # 基准测试框架
│   ├── BenchmarkBaselines.java     # 主程序
│   ├── AlgorithmEvaluator.java     # 算法评估器
│   ├── IOHLogger.java              # IOH日志记录器
│   ├── ObjectiveFunction.java      # 目标函数接口
│   ├── FunctionMetadata.java       # 函数元数据
│   └── SphereFunction.java         # Sphere函数实现
├── data/                 # 数据处理
├── utils/                # 工具类
└── config/              # 配置管理
```

## 环境要求
- Java 11 或更高版本
- Maven 3.6 或更高版本

## 构建和运行

### 1. 编译项目
```bash
mvn clean compile
```

### 2. 运行基准测试
```bash
mvn exec:java -Dexec.mainClass="com.swarm.benchmark.BenchmarkBaselines"
```

### 3. 运行测试
```bash
mvn test
```

## 实验设置
- **函数**: F1 (Sphere)
- **实例**: 10个实例 (I1-I10)
- **维度**: 10D
- **运行次数**: 每个实例5次独立运行
- **评估预算**: B = 10000 * d
- **算法**: BIPOP-CMA-ES

## 输出
- 实验结果保存在 `Data/Baselines/` 目录下
- 日志文件保存在 `benchmark.log`
- 每个实验生成一个 `.dat` 文件，格式与IOHprofiler兼容

## 依赖库
- Apache Commons Math 3.6.1 - 数学计算
- Apache Commons CSV 1.9.0 - CSV文件处理
- Log4j2 2.17.2 - 日志记录
- JUnit 5.8.2 - 单元测试

## 与Python版本的对应关系
| Python组件 | Java组件 |
|------------|----------|
| benchmark_baselines.py | BenchmarkBaselines.java |
| Algorithm_Evaluator | AlgorithmEvaluator.java |
| ioh.logger.Analyzer | IOHLogger.java |
| ioh.get_problem | SphereFunction.java |
| modcma.ModularCMAES | BIPOPCMAES.java |
| numpy | Apache Commons Math |
| pandas | Apache Commons CSV |

## 开发计划
- [x] BIPOP-CMA-ES算法实现
- [x] Sphere函数实现
- [x] IOH兼容的日志记录
- [x] 并行实验执行
- [ ] CS算法实现
- [ ] DE算法实现
- [ ] 数据处理脚本
- [ ] 结果比较功能
