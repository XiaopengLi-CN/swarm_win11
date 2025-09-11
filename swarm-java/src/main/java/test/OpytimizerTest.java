package test;

import opytimizer.Opytimizer;
import opytimizer.core.Function;
import opytimizer.core.Space;
import opytimizer.spaces.SearchSpace;
import opytimizer.optimizers.swarm.CS;
import opfunu.name_based.Sphere;

/**
 * 完全匹配Python的测试示例
 * 
 * Python代码:
 * ```python
 * from opytimizer import Opytimizer
 * from opytimizer.core.function import Function
 * from opytimizer.spaces import SearchSpace
 * from opytimizer.optimizers.swarm import CS
 * from opfunu.name_based import Sphere
 * 
 * # 创建函数
 * f = Sphere(ndim=10)
 * 
 * # 创建搜索空间
 * space = SearchSpace(n_agents=30, n_variables=10, lower_bound=-5.12, upper_bound=5.12)
 * 
 * # 创建优化器
 * optimizer = CS()
 * 
 * # 创建Opytimizer
 * opt = Opytimizer(space, optimizer, f)
 * 
 * # 开始优化
 * result = opt.start(n_iterations=100)
 * 
 * # 获取结果
 * best_agent = opt.get_best_agent()
 * print(f"Best fitness: {best_agent.fit}")
 * ```
 */
public class OpytimizerTest {
    
    public static void main(String[] args) {
        System.out.println("=== 完全匹配Python的Opytimizer测试 ===");
        
        try {
            // 创建函数 - 完全匹配Python的调用方式
            Sphere f = new Sphere(10);
            System.out.println("Created function: " + f.get_name());
            
            // 创建搜索空间 - 完全匹配Python的参数
            SearchSpace space = new SearchSpace(30, 10, -5.12, 5.12);
            System.out.println("Created space: " + space);
            
            // 创建优化器 - 完全匹配Python的调用方式
            CS optimizer = new CS();
            System.out.println("Created optimizer: " + optimizer);
            
            // 创建Opytimizer - 完全匹配Python的调用方式
            Opytimizer opt = new Opytimizer(space, optimizer, new Function(x -> f.evaluate(x)));
            System.out.println("Created Opytimizer: " + opt);
            
            // 开始优化 - 完全匹配Python的方法调用
            Object result = opt.start(100);
            System.out.println("Optimization completed: " + result);
            
            // 获取最佳智能体 - 完全匹配Python的方法调用
            Object best_agent = opt.get_best_agent();
            System.out.println("Best agent: " + best_agent);
            
            // 获取历史记录 - 完全匹配Python的方法调用
            Object history = opt.get_history();
            System.out.println("History: " + history);
            
            System.out.println("=== 测试完成 ===");
            
        } catch (Exception e) {
            System.err.println("测试失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
