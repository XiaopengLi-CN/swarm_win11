package opytimizer;

import opytimizer.core.Function;
import opytimizer.core.Optimizer;
import opytimizer.core.Space;
import opytimizer.utils.history.History;
import opytimizer.utils.logging.Logger;

/**
 * Java版本的Opytimizer类 - 完全复现Python的opytimizer.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/opytimizer.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Opytimizer {
    
    private static final Logger logger = Logger.get_logger(Opytimizer.class.getName());
    
    // 完全匹配Python的属性名
    public Space space;
    public Optimizer optimizer;
    public Function function;
    public boolean save_agents;
    public History history;
    public int iteration;
    public int total_iterations;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param space Space-child instance
     * @param optimizer Optimizer-child instance  
     * @param function Function or Function-child instance
     * @param save_agents Saves all agents in the search space
     */
    public Opytimizer(Space space, Optimizer optimizer, Function function, Boolean save_agents) {
        logger.info("Creating class: Opytimizer.");
        
        // 完全匹配Python的属性赋值
        this.space = space;
        this.optimizer = optimizer;
        this.function = function;
        this.save_agents = save_agents != null ? save_agents : false;
        
        // 初始化历史记录
        this.history = new History(this.save_agents);
        
        // 初始化迭代计数
        this.iteration = 0;
        this.total_iterations = 0;
        
        logger.info("Class created.");
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Opytimizer(Space space, Optimizer optimizer, Function function) {
        this(space, optimizer, function, false);
    }
    
    /**
     * 开始优化 - 完全匹配Python的start方法
     * 
     * @param n_iterations Number of iterations
     * @return Optimization result
     */
    public Object start(int n_iterations) {
        logger.info("Starting optimization with {} iterations", n_iterations);
        
        this.total_iterations = n_iterations;
        this.iteration = 0;
        
        long start_time = System.currentTimeMillis();
        
        try {
            // 优化循环 - 完全匹配Python的逻辑
            for (int i = 0; i < n_iterations; i++) {
                this.iteration = i;
                
                // 执行优化步骤
                this.optimizer.update(this.space, this.function);
                
                // 记录历史
                this.history.record(this.space, this.optimizer, this.function, i);
            }
            
            long end_time = System.currentTimeMillis();
            long duration = end_time - start_time;
            
            logger.info("Optimization completed in {} ms", duration);
            
            // 返回结果 - 匹配Python的返回值结构
            return new OptimizationResult(
                this.space.get_best_agent(),
                this.history,
                duration,
                n_iterations
            );
            
        } catch (Exception e) {
            logger.error("Optimization failed", e);
            throw new RuntimeException("Optimization failed", e);
        }
    }
    
    /**
     * 获取最佳智能体 - 匹配Python的get_best_agent方法
     */
    public Object get_best_agent() {
        return this.space.get_best_agent();
    }
    
    /**
     * 获取历史记录 - 匹配Python的get_history方法
     */
    public History get_history() {
        return this.history;
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Opytimizer{space=%s, optimizer=%s, function=%s, iteration=%d/%d}", 
                           space, optimizer, function, iteration, total_iterations);
    }
}

/**
 * 优化结果类 - 匹配Python的返回值结构
 */
class OptimizationResult {
    public Object best_agent;
    public History history;
    public long duration;
    public int iterations;
    
    public OptimizationResult(Object best_agent, History history, long duration, int iterations) {
        this.best_agent = best_agent;
        this.history = history;
        this.duration = duration;
        this.iterations = iterations;
    }
}
