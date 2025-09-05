"""
代码执行跟踪使用说明

本工具包提供了三种不同级别的代码执行跟踪方法：

1. 基础跟踪器 (code_execution_tracer.py)
   - 跟踪函数调用、模块导入
   - 记录函数参数和返回值
   - 适合了解程序的主要执行流程

2. 高级跟踪器 (advanced_code_tracer.py)  
   - 使用sys.settrace跟踪每一行代码
   - 记录详细的执行路径
   - 适合深度分析代码执行过程

3. 集成版本
   - benchmark_baselines_traced.py: 使用基础跟踪器
   - benchmark_baselines_advanced_traced.py: 使用高级跟踪器

使用方法：
"""

# 示例1: 使用基础跟踪器
def example_basic_tracing():
    """基础跟踪器使用示例"""
    from code_execution_tracer import start_tracing, stop_tracing, trace_function
    
    # 开始跟踪
    tracer = start_tracing("example_basic.log")
    
    @trace_function
    def example_function(x, y):
        return x + y
    
    # 执行一些代码
    result = example_function(1, 2)
    print(f"结果: {result}")
    
    # 停止跟踪
    stop_tracing("example_basic_summary.json")

# 示例2: 使用高级跟踪器
def example_advanced_tracing():
    """高级跟踪器使用示例"""
    from advanced_code_tracer import start_advanced_tracing, stop_advanced_tracing
    
    # 开始高级跟踪
    tracer = start_advanced_tracing("example_advanced.log")
    
    def example_function(x, y):
        z = x * 2
        return z + y
    
    # 执行一些代码
    result = example_function(3, 4)
    print(f"结果: {result}")
    
    # 停止跟踪
    stop_advanced_tracing("example_advanced_summary.json")

# 示例3: 跟踪特定模块
def example_module_tracing():
    """跟踪特定模块的示例"""
    from code_execution_tracer import start_tracing, trace_class
    
    tracer = start_tracing("module_trace.log")
    
    @trace_class
    class MyClass:
        def method1(self):
            return "method1"
        
        def method2(self):
            return "method2"
    
    obj = MyClass()
    obj.method1()
    obj.method2()
    
    stop_tracing("module_summary.json")

if __name__ == "__main__":
    print("代码执行跟踪示例")
    print("=" * 50)
    
    print("\n1. 基础跟踪示例:")
    example_basic_tracing()
    
    print("\n2. 高级跟踪示例:")
    example_advanced_tracing()
    
    print("\n3. 模块跟踪示例:")
    example_module_tracing()
    
    print("\n跟踪完成！请查看生成的日志文件。")
