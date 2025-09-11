package opytimizer.core;

import opytimizer.utils.logging.Logger;
import opytimizer.utils.exception.TypeError;
import opytimizer.utils.exception.ValueError;
import opytimizer.utils.exception.BuildError;
import java.util.List;
import java.util.ArrayList;

/**
 * Java版本的Space类 - 完全复现Python的space.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/core/space.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Space {
    
    private static final Logger logger = Logger.get_logger(Space.class.getName());
    
    // 完全匹配Python的属性名
    public int n_agents;
    public int n_variables;
    public int n_dimensions;
    public double[] lb;
    public double[] ub;
    public String[] mapping;
    public List<Agent> agents;
    public Agent best_agent;
    public boolean built;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param n_agents Number of agents
     * @param n_variables Number of decision variables
     * @param n_dimensions Dimension of search space
     * @param lower_bound Minimum possible values
     * @param upper_bound Maximum possible values
     * @param mapping String-based identifiers for mapping variables' names
     */
    public Space(int n_agents, int n_variables, int n_dimensions, 
                double[] lower_bound, double[] upper_bound, String[] mapping) {
        logger.info("Creating class: Space.");
        
        // 完全匹配Python的属性赋值
        this.n_agents = n_agents;
        this.n_variables = n_variables;
        this.n_dimensions = n_dimensions;
        this.lb = lower_bound.clone();
        this.ub = upper_bound.clone();
        this.mapping = mapping != null ? mapping.clone() : null;
        
        // 初始化智能体列表
        this.agents = new ArrayList<>();
        
        // 创建最佳智能体
        this.best_agent = new Agent(n_variables, n_dimensions, lower_bound, upper_bound, mapping);
        
        // 表示空间是否已构建
        this.built = false;
        
        logger.debug("Space: %s | Agents: %d | Variables: %d | Dimensions: %d | Built: %s.", 
                    this, n_agents, n_variables, n_dimensions, built);
        logger.info("Class created.");
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Space(int n_agents, int n_variables, int n_dimensions, 
                double lower_bound, double upper_bound) {
        this(n_agents, n_variables, n_dimensions, 
             new double[]{lower_bound}, new double[]{upper_bound}, null);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Space(int n_agents, int n_variables, double lower_bound, double upper_bound) {
        this(n_agents, n_variables, 1, lower_bound, upper_bound);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Space(int n_agents, int n_variables) {
        this(n_agents, n_variables, 1, 0.0, 1.0);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Space(int n_agents) {
        this(n_agents, 1, 1, 0.0, 1.0);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Space() {
        this(1, 1, 1, 0.0, 1.0);
    }
    
    /**
     * 构建空间 - 完全匹配Python的build方法
     */
    public void build() {
        logger.info("Building space: %d agents, %d variables, %d dimensions", 
                   n_agents, n_variables, n_dimensions);
        
        // 创建智能体
        this.agents.clear();
        for (int i = 0; i < n_agents; i++) {
            Agent agent = new Agent(n_variables, n_dimensions, lb, ub, mapping);
            this.agents.add(agent);
        }
        
        this.built = true;
        logger.info("Space built successfully.");
    }
    
    /**
     * 获取最佳智能体 - 匹配Python的get_best_agent方法
     */
    public Agent get_best_agent() {
        return this.best_agent;
    }
    
    /**
     * 设置最佳智能体 - 匹配Python的set_best_agent方法
     */
    public void set_best_agent(Agent agent) {
        this.best_agent = agent;
    }
    
    /**
     * 获取智能体 - 匹配Python的get_agent方法
     */
    public Agent get_agent(int index) throws ValueError {
        if (index < 0 || index >= agents.size()) {
            throw new ValueError("Agent index out of bounds");
        }
        return this.agents.get(index);
    }
    
    /**
     * 设置智能体 - 匹配Python的set_agent方法
     */
    public void set_agent(int index, Agent agent) throws ValueError {
        if (index < 0 || index >= agents.size()) {
            throw new ValueError("Agent index out of bounds");
        }
        this.agents.set(index, agent);
    }
    
    /**
     * 获取所有智能体 - 匹配Python的agents属性
     */
    public List<Agent> get_agents() {
        return this.agents;
    }
    
    /**
     * 获取构建状态 - 匹配Python的built属性
     */
    public boolean get_built() {
        return this.built;
    }
    
    /**
     * 设置构建状态 - 匹配Python的built属性
     */
    public void set_built(boolean built) {
        this.built = built;
    }
    
    /**
     * 获取下界 - 匹配Python的lb属性
     */
    public double[] get_lb() {
        return this.lb;
    }
    
    /**
     * 获取上界 - 匹配Python的ub属性
     */
    public double[] get_ub() {
        return this.ub;
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Space{n_agents=%d, n_variables=%d, n_dimensions=%d, built=%s}", 
                           n_agents, n_variables, n_dimensions, built);
    }
}
