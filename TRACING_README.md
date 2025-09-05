# 代码执行跟踪工具包

这个工具包可以帮助您详细记录 `benchmark_baselines.py` 运行过程中每一步执行的代码，包括：

- 函数调用轨迹
- 模块导入过程  
- 代码执行路径
- 参数和返回值
- 执行时间统计
- 异常信息

## 工具包组成

### 1. 基础跟踪器 (`code_execution_tracer.py`)
- **功能**: 跟踪函数调用、模块导入、记录参数和返回值
- **适用场景**: 了解程序的主要执行流程
- **特点**: 性能开销较小，信息详细但不冗余

### 2. 高级跟踪器 (`advanced_code_tracer.py`)
- **功能**: 使用 `sys.settrace` 跟踪每一行代码的执行
- **适用场景**: 深度分析代码执行过程，调试复杂问题
- **特点**: 信息极其详细，但性能开销较大

### 3. 集成版本
- `benchmark_baselines_traced.py`: 使用基础跟踪器的版本
- `benchmark_baselines_advanced_traced.py`: 使用高级跟踪器的版本

## 使用方法

### 方法1: 直接运行集成版本

```bash
# 使用基础跟踪器
python benchmark_baselines_traced.py

# 使用高级跟踪器（更详细）
python benchmark_baselines_advanced_traced.py
```

### 方法2: 在现有代码中集成跟踪

```python
from code_execution_tracer import start_tracing, stop_tracing, trace_function

# 开始跟踪
tracer = start_tracing("my_trace.log")

@trace_function
def my_function(x, y):
    return x + y

# 您的代码...

# 停止跟踪
stop_tracing("my_summary.json")
```

### 方法3: 跟踪特定类或模块

```python
from code_execution_tracer import trace_class

@trace_class
class MyClass:
    def method1(self):
        pass
    
    def method2(self):
        pass
```

## 输出文件说明

运行跟踪后，会生成以下文件：

### 日志文件
- `execution_trace.log`: 详细的执行日志
- `advanced_execution_trace.log`: 高级跟踪日志（包含每行代码）

### 摘要文件
- `execution_summary.json`: 执行摘要（JSON格式）
- `advanced_execution_summary.json`: 高级跟踪摘要

### 摘要内容包括：
- 总执行时间
- 函数调用统计
- 模块导入列表
- 最频繁执行的代码行
- 错误信息
- 执行流程图

## 性能考虑

- **基础跟踪器**: 性能开销约5-10%
- **高级跟踪器**: 性能开销约20-50%，但信息更详细
- 建议在调试时使用，生产环境可关闭

## 示例输出

### 基础跟踪日志示例：
```
[0.000123] [12345] [INFO] 开始代码执行跟踪
[0.000456] [12345] [INFO] 导入模块: numpy
[0.001234] [12345] [INFO] 调用函数: benchmark_baselines.runParallelFunction (文件: benchmark_baselines.py:26)
[0.001567] [12345] [INFO] 函数完成: benchmark_baselines.runParallelFunction (耗时: 0.000333s)
```

### 高级跟踪日志示例：
```
[0.000123] [12345] CALL: benchmark_baselines.py:26 in runParallelFunction() -> arguments = list(arguments)
[0.000124] [12345] LINE: benchmark_baselines.py:27 -> p = Pool(min(MAX_THREADS, len(arguments)))
[0.000125] [12345] LINE: benchmark_baselines.py:28 -> results = p.map(runFunction, arguments)
[0.000126] [12345] LINE: benchmark_baselines.py:29 -> p.close()
[0.000127] [12345] RETURN: benchmark_baselines.py:30 in runParallelFunction() (arg: [result1, result2, ...])
```

## 故障排除

### 常见问题：

1. **跟踪器无法启动**
   - 检查Python版本（需要3.6+）
   - 确保有写入权限

2. **日志文件过大**
   - 使用基础跟踪器而不是高级跟踪器
   - 减少跟踪的代码范围

3. **性能影响过大**
   - 关闭不必要的跟踪选项
   - 只在需要调试时使用

## 扩展功能

您可以根据需要扩展跟踪器：

1. **添加自定义事件类型**
2. **集成性能分析工具**
3. **添加可视化功能**
4. **支持分布式跟踪**

## 注意事项

- 跟踪器会显著影响程序性能，建议只在调试时使用
- 生成的日志文件可能很大，注意磁盘空间
- 在多线程环境中，每个线程的跟踪是独立的
- 某些系统调用可能无法被跟踪

## 联系支持

如有问题或建议，请查看生成的日志文件或联系开发团队。
