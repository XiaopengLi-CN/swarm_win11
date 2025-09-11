package opytimizer.utils.history;

import opytimizer.core.Space;
import opytimizer.core.Optimizer;
import opytimizer.core.Function;
import opytimizer.core.Agent;
import opytimizer.utils.logging.Logger;
import java.util.List;
import java.util.ArrayList;

/**
 * Java版本的History类 - 完全复现Python的history.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/utils/history.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class History {
    
    private static final Logger logger = Logger.get_logger(History.class.getName());
    
    // 完全匹配Python的属性名
    public boolean save_agents;
    public List<Double> best_fitness;
    public List<Double> mean_fitness;
    public List<Double> worst_fitness;
    public List<List<Agent>> agents;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param save_agents Saves all agents in the search space
     */
    public History(boolean save_agents) {
        logger.info("Creating class: History.");
        
        // 完全匹配Python的属性赋值
        this.save_agents = save_agents;
        this.best_fitness = new ArrayList<>();
        this.mean_fitness = new ArrayList<>();
        this.worst_fitness = new ArrayList<>();
        this.agents = new ArrayList<>();
        
        logger.info("Class created.");
    }
    
    /**
     * 构造函数重载 - 默认不保存智能体
     */
    public History() {
        this(false);
    }
    
    /**
     * 记录历史 - 完全匹配Python的record方法
     * 
     * @param space Space containing agents and update-related information
     * @param optimizer Optimizer containing update-related information
     * @param function Function containing evaluation-related information
     * @param iteration Current iteration number
     */
    public void record(Space space, Optimizer optimizer, Function function, int iteration) {
        // 计算适应度统计 - 匹配Python的逻辑
        double best = Double.POSITIVE_INFINITY;
        double worst = Double.NEGATIVE_INFINITY;
        double sum = 0.0;
        
        for (Agent agent : space.get_agents()) {
            double fitness = agent.get_fit();
            best = Math.min(best, fitness);
            worst = Math.max(worst, fitness);
            sum += fitness;
        }
        
        double mean = sum / space.get_agents().size();
        
        // 记录统计信息
        this.best_fitness.add(best);
        this.mean_fitness.add(mean);
        this.worst_fitness.add(worst);
        
        // 如果启用，保存智能体
        if (this.save_agents) {
            List<Agent> iteration_agents = new ArrayList<>();
            for (Agent agent : space.get_agents()) {
                iteration_agents.add(agent.copy());
            }
            this.agents.add(iteration_agents);
        }
    }
    
    /**
     * 获取最佳适应度历史 - 匹配Python的get_best_fitness方法
     */
    public List<Double> get_best_fitness() {
        return this.best_fitness;
    }
    
    /**
     * 获取平均适应度历史 - 匹配Python的get_mean_fitness方法
     */
    public List<Double> get_mean_fitness() {
        return this.mean_fitness;
    }
    
    /**
     * 获取最差适应度历史 - 匹配Python的get_worst_fitness方法
     */
    public List<Double> get_worst_fitness() {
        return this.worst_fitness;
    }
    
    /**
     * 获取智能体历史 - 匹配Python的get_agents方法
     */
    public List<List<Agent>> get_agents() {
        return this.agents;
    }
    
    /**
     * 获取历史长度 - 匹配Python的get_length方法
     */
    public int get_length() {
        return this.best_fitness.size();
    }
    
    /**
     * 清空历史 - 匹配Python的clear方法
     */
    public void clear() {
        this.best_fitness.clear();
        this.mean_fitness.clear();
        this.worst_fitness.clear();
        this.agents.clear();
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("History{length=%d, save_agents=%s}", 
                           get_length(), save_agents);
    }
}
