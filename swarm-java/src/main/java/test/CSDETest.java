package test;

import opytimizer.Opytimizer;
import opytimizer.core.Function;
import opytimizer.core.Space;
import opytimizer.spaces.SearchSpace;
import opytimizer.optimizers.swarm.CS;
import opytimizer.optimizers.evolutionary.DE;
import opfunu.name_based.Sphere;

/**
 * 完全匹配Python的CS和DE算法测试
 * 
 * Python代码:
 * ```python
 * from opytimizer import Opytimizer
 * from opytimizer.core.function import Function
 * from opytimizer.spaces import SearchSpace
 * from opytimizer.optimizers.swarm import CS
 * from opytimizer.optimizers.evolutionary import DE
 * from opfunu.name_based import Sphere
 * 
 * # 测试CS算法
 * f = Sphere(ndim=10)
 * space = SearchSpace(n_agents=30, n_variables=10, lower_bound=-5.12, upper_bound=5.12)
 * optimizer = CS()
 * opt = Opytimizer(space, optimizer, f)
 * result = opt.start(n_iterations=100)
 * 
 * # 测试DE算法
 * optimizer2 = DE()
 * opt2 = Opytimizer(space, optimizer2, f)
 * result2 = opt2.start(n_iterations=100)
 * ```
 */
public class CSDETest {
    
    public static void main(String[] args) {
        System.out.println("=== 完全匹配Python的CS和DE算法测试 ===");
        
        try {
            // 创建函数 - 完全匹配Python的调用方式
            Sphere f = new Sphere(10);
            System.out.println("Created function: " + f.get_name());
            
            // 创建搜索空间 - 完全匹配Python的参数
            SearchSpace space = new SearchSpace(30, 10, -5.12, 5.12);
            System.out.println("Created space: " + space);
            
            // 测试CS算法 - 完全匹配Python的调用方式
            System.out.println("\n--- 测试CS算法 ---");
            CS cs_optimizer = new CS();
            System.out.println("Created CS optimizer: " + cs_optimizer);
            
            Opytimizer cs_opt = new Opytimizer(space, cs_optimizer, new Function(x -> f.evaluate(x)));
            System.out.println("Created CS Opytimizer: " + cs_opt);
            
            Object cs_result = cs_opt.start(100);
            System.out.println("CS Optimization completed: " + cs_result);
            
            Object cs_best_agent = cs_opt.get_best_agent();
            System.out.println("CS Best agent: " + cs_best_agent);
            
            // 测试DE算法 - 完全匹配Python的调用方式
            System.out.println("\n--- 测试DE算法 ---");
            DE de_optimizer = new DE();
            System.out.println("Created DE optimizer: " + de_optimizer);
            
            Opytimizer de_opt = new Opytimizer(space, de_optimizer, new Function(x -> f.evaluate(x)));
            System.out.println("Created DE Opytimizer: " + de_opt);
            
            Object de_result = de_opt.start(100);
            System.out.println("DE Optimization completed: " + de_result);
            
            Object de_best_agent = de_opt.get_best_agent();
            System.out.println("DE Best agent: " + de_best_agent);
            
            System.out.println("\n=== 测试完成 ===");
            
        } catch (Exception e) {
            System.err.println("测试失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
