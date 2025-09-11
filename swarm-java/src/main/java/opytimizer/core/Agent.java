package opytimizer.core;

import opytimizer.utils.logging.Logger;
import opytimizer.utils.constant.Constant;

/**
 * Java版本的Agent类 - 完全复现Python的agent.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/core/agent.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Agent {
    
    private static final Logger logger = Logger.get_logger(Agent.class.getName());
    
    // 完全匹配Python的属性名
    public int n_variables;
    public int n_dimensions;
    public double[][] position;
    public double fit;
    public double[] lb;
    public double[] ub;
    public String[] mapping;
    public long ts;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param n_variables Number of decision variables
     * @param n_dimensions Number of dimensions
     * @param lower_bound Minimum possible values
     * @param upper_bound Maximum possible values
     * @param mapping String-based identifiers for mapping variables' names
     */
    public Agent(int n_variables, int n_dimensions, double[] lower_bound, double[] upper_bound, String[] mapping) {
        logger.info("Creating class: Agent.");
        
        // 完全匹配Python的属性赋值
        this.n_variables = n_variables;
        this.n_dimensions = n_dimensions;
        this.position = new double[n_variables][n_dimensions];
        this.fit = Constant.FLOAT_MAX;
        this.lb = lower_bound.clone();
        this.ub = upper_bound.clone();
        this.mapping = mapping != null ? mapping.clone() : null;
        this.ts = System.currentTimeMillis() / 1000;
        
        logger.debug("Agent: %s | Variables: %d | Dimensions: %d | Built: %s.", 
                    this, n_variables, n_dimensions, true);
        logger.info("Class created.");
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Agent(int n_variables, int n_dimensions, double[] lower_bound, double[] upper_bound) {
        this(n_variables, n_dimensions, lower_bound, upper_bound, null);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public Agent(int n_variables, int n_dimensions, double lower_bound, double upper_bound) {
        this(n_variables, n_dimensions, 
             new double[]{lower_bound}, new double[]{upper_bound}, null);
    }
    
    /**
     * 获取位置 - 匹配Python的position属性
     */
    public double[][] get_position() {
        return this.position;
    }
    
    /**
     * 设置位置 - 匹配Python的position属性
     */
    public void set_position(double[][] position) {
        this.position = position;
    }
    
    /**
     * 获取适应度 - 匹配Python的fit属性
     */
    public double get_fit() {
        return this.fit;
    }
    
    /**
     * 设置适应度 - 匹配Python的fit属性
     */
    public void set_fit(double fit) {
        this.fit = fit;
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
     * 获取映射 - 匹配Python的mapping属性
     */
    public String[] get_mapping() {
        return this.mapping;
    }
    
    /**
     * 获取时间戳 - 匹配Python的ts属性
     */
    public long get_ts() {
        return this.ts;
    }
    
    /**
     * 复制智能体 - 匹配Python的copy方法
     */
    public Agent copy() {
        Agent new_agent = new Agent(this.n_variables, this.n_dimensions, this.lb, this.ub, this.mapping);
        new_agent.position = this.position.clone();
        new_agent.fit = this.fit;
        new_agent.ts = this.ts;
        return new_agent;
    }
    
    /**
     * 边界裁剪 - 完全匹配Python的clip_by_bound方法
     */
    public void clip_by_bound() {
        // Iterates through all the decision variables - 完全匹配Python的逻辑
        for (int j = 0; j < n_variables; j++) {
            // Clips the array based on variable's lower and upper bounds - 完全匹配Python的np.clip
            for (int d = 0; d < n_dimensions; d++) {
                position[j][d] = Math.max(lb[j], Math.min(ub[j], position[j][d]));
            }
        }
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Agent{variables=%d, dimensions=%d, fit=%.6f, ts=%d}", 
                           n_variables, n_dimensions, fit, ts);
    }
}
