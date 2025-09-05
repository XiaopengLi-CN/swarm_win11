"""
简单测试脚本 - 验证代码执行跟踪功能
"""

def test_basic_tracing():
    """测试基础跟踪功能"""
    try:
        from code_execution_tracer import start_tracing, stop_tracing, trace_function
        
        print("开始测试基础跟踪功能...")
        
        # 开始跟踪
        tracer = start_tracing("test_basic.log")
        
        @trace_function
        def test_function(x, y):
            return x + y
        
        # 执行测试
        result = test_function(1, 2)
        print(f"测试函数结果: {result}")
        
        # 停止跟踪
        stop_tracing("test_basic_summary.json")
        
        print("基础跟踪测试完成！")
        return True
        
    except Exception as e:
        print(f"基础跟踪测试失败: {e}")
        return False

def test_advanced_tracing():
    """测试高级跟踪功能"""
    try:
        from advanced_code_tracer import start_advanced_tracing, stop_advanced_tracing
        
        print("开始测试高级跟踪功能...")
        
        # 开始高级跟踪
        tracer = start_advanced_tracing("test_advanced.log")
        
        def test_function(x, y):
            z = x * 2
            return z + y
        
        # 执行测试
        result = test_function(3, 4)
        print(f"测试函数结果: {result}")
        
        # 停止跟踪
        stop_advanced_tracing("test_advanced_summary.json")
        
        print("高级跟踪测试完成！")
        return True
        
    except Exception as e:
        print(f"高级跟踪测试失败: {e}")
        return False

if __name__ == "__main__":
    print("代码执行跟踪功能测试")
    print("=" * 50)
    
    # 测试基础跟踪
    basic_success = test_basic_tracing()
    
    print("\n" + "-" * 50 + "\n")
    
    # 测试高级跟踪
    advanced_success = test_advanced_tracing()
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"基础跟踪: {'成功' if basic_success else '失败'}")
    print(f"高级跟踪: {'成功' if advanced_success else '失败'}")
    
    if basic_success and advanced_success:
        print("\n所有测试通过！跟踪功能正常工作。")
        print("您现在可以使用以下命令运行带跟踪的benchmark:")
        print("python benchmark_baselines_traced.py")
        print("python benchmark_baselines_advanced_traced.py")
    else:
        print("\n部分测试失败，请检查错误信息。")
