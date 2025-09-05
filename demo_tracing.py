"""
代码执行跟踪演示脚本
这个脚本展示了如何使用跟踪功能来记录benchmark_baselines.py的执行过程
"""

# 方法1: 使用基础跟踪器
def demo_basic_tracing():
    """演示基础跟踪功能"""
    print("=== 基础跟踪器演示 ===")
    
    # 导入跟踪器
    from code_execution_tracer import start_tracing, stop_tracing, trace_function
    
    # 开始跟踪
    tracer = start_tracing("demo_basic.log")
    
    # 定义要跟踪的函数
    @trace_function
    def calculate_sum(numbers):
        """计算数字列表的和"""
        total = 0
        for num in numbers:
            total += num
        return total
    
    @trace_function
    def process_data(data):
        """处理数据"""
        result = []
        for item in data:
            if item > 0:
                result.append(item * 2)
        return result
    
    # 执行一些操作
    numbers = [1, 2, 3, 4, 5]
    sum_result = calculate_sum(numbers)
    print(f"数字和: {sum_result}")
    
    processed = process_data(numbers)
    print(f"处理后的数据: {processed}")
    
    # 停止跟踪
    stop_tracing("demo_basic_summary.json")
    print("基础跟踪完成！查看 demo_basic.log 和 demo_basic_summary.json")

# 方法2: 使用高级跟踪器
def demo_advanced_tracing():
    """演示高级跟踪功能"""
    print("\n=== 高级跟踪器演示 ===")
    
    # 导入高级跟踪器
    from advanced_code_tracer import start_advanced_tracing, stop_advanced_tracing
    
    # 开始高级跟踪
    tracer = start_advanced_tracing("demo_advanced.log")
    
    def complex_calculation(x, y):
        """复杂计算函数"""
        # 第一步：计算平方
        x_squared = x * x
        y_squared = y * y
        
        # 第二步：计算和
        sum_squares = x_squared + y_squared
        
        # 第三步：计算平方根
        import math
        result = math.sqrt(sum_squares)
        
        return result
    
    # 执行计算
    result = complex_calculation(3, 4)
    print(f"复杂计算结果: {result}")
    
    # 停止跟踪
    stop_advanced_tracing("demo_advanced_summary.json")
    print("高级跟踪完成！查看 demo_advanced.log 和 demo_advanced_summary.json")

# 方法3: 模拟benchmark_baselines.py的执行跟踪
def demo_benchmark_tracing():
    """演示如何跟踪benchmark_baselines.py的执行"""
    print("\n=== Benchmark跟踪演示 ===")
    
    from code_execution_tracer import start_tracing, stop_tracing, trace_function
    
    # 开始跟踪
    tracer = start_tracing("benchmark_demo.log")
    
    @trace_function
    def simulate_optimizer_run(problem_id, instance_id, dimension):
        """模拟优化器运行"""
        print(f"运行优化器: F{problem_id}, I{instance_id}, {dimension}D")
        
        # 模拟一些计算
        import time
        time.sleep(0.1)  # 模拟计算时间
        
        return f"F{problem_id}_I{instance_id}_{dimension}D 完成"
    
    @trace_function
    def run_parallel_tasks():
        """运行并行任务"""
        tasks = [
            (20, 1, 10),  # F20, I1, 10D
            (21, 1, 10),  # F21, I1, 10D
            (22, 1, 10),  # F22, I1, 10D
        ]
        
        results = []
        for task in tasks:
            result = simulate_optimizer_run(*task)
            results.append(result)
        
        return results
    
    # 执行模拟的benchmark
    results = run_parallel_tasks()
    print(f"所有任务完成: {len(results)} 个结果")
    
    # 停止跟踪
    stop_tracing("benchmark_demo_summary.json")
    print("Benchmark跟踪演示完成！")

if __name__ == "__main__":
    print("代码执行跟踪功能演示")
    print("=" * 60)
    
    try:
        # 演示基础跟踪
        demo_basic_tracing()
        
        # 演示高级跟踪
        demo_advanced_tracing()
        
        # 演示benchmark跟踪
        demo_benchmark_tracing()
        
        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("\n现在您可以使用以下方法跟踪您的benchmark_baselines.py:")
        print("1. 运行: python benchmark_baselines_traced.py")
        print("2. 运行: python benchmark_baselines_advanced_traced.py")
        print("3. 查看生成的日志文件了解详细执行过程")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        print("请检查跟踪器文件是否正确创建")
