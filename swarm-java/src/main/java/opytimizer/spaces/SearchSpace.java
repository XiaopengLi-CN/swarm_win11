package opytimizer.spaces;

import opytimizer.core.Space;
import opytimizer.utils.logging.Logger;

/**
 * Java版本的SearchSpace类 - 完全复现Python的search.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/spaces/search.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class SearchSpace extends Space {
    
    private static final Logger logger = Logger.get_logger(SearchSpace.class.getName());
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param n_agents Number of agents
     * @param n_variables Number of decision variables
     * @param lower_bound Minimum possible values
     * @param upper_bound Maximum possible values
     */
    public SearchSpace(int n_agents, int n_variables, double[] lower_bound, double[] upper_bound) {
        super(n_agents, n_variables, 1, lower_bound, upper_bound, null);
        
        logger.info("Overriding class: Space -> SearchSpace.");
        logger.info("Class overrided.");
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public SearchSpace(int n_agents, int n_variables, double lower_bound, double upper_bound) {
        this(n_agents, n_variables, new double[]{lower_bound}, new double[]{upper_bound});
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public SearchSpace(int n_agents, int n_variables) {
        this(n_agents, n_variables, 0.0, 1.0);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public SearchSpace(int n_agents) {
        this(n_agents, 1, 0.0, 1.0);
    }
    
    /**
     * 构造函数重载 - 匹配Python的默认参数
     */
    public SearchSpace() {
        this(1, 1, 0.0, 1.0);
    }
    
    /**
     * 构建搜索空间 - 完全匹配Python的build方法
     */
    @Override
    public void build() {
        logger.info("Building space: %d agents, %d variables, %d dimensions", 
                   n_agents, n_variables, n_dimensions);
        
        // 调用父类的构建方法
        super.build();
        
        logger.info("Space built successfully.");
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("SearchSpace{n_agents=%d, n_variables=%d, built=%s}", 
                           n_agents, n_variables, built);
    }
}
