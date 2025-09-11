package opytimizer.optimizers.swarm;

import opytimizer.core.Optimizer;
import opytimizer.core.Space;
import opytimizer.core.Function;
import opytimizer.core.Agent;
import opytimizer.utils.logging.Logger;
import opytimizer.utils.exception.TypeError;
import opytimizer.utils.exception.ValueError;
import opytimizer.math.distribution.Distribution;
import opytimizer.math.random.Random;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

/**
 * Java版本的CS类 - 完全复现Python的cs.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/optimizers/swarm/cs.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class CS extends Optimizer {
    
    private static final Logger logger = Logger.get_logger(CS.class.getName());
    
    // 完全匹配Python的属性名 - 使用私有属性+getter/setter
    private double _alpha;
    private double _beta;
    private double _p;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param params Contains key-value parameters to the meta-heuristics
     */
    public CS(Map<String, Object> params) throws Exception {
        super(params);
        
        logger.info("Overriding class: Optimizer -> CS.");
        
        // 完全匹配Python的属性赋值
        this.set_alpha(1.0);
        this.set_beta(1.5);
        this.set_p(0.2);
        
        // 构建类
        this.build(params);
        
        logger.info("Class overrided.");
    }
    
    /**
     * 构造函数重载 - 无参数
     */
    public CS() throws Exception {
        this(null);
    }
    
    /**
     * 获取alpha - 完全匹配Python的@property alpha
     */
    public double get_alpha() {
        return this._alpha;
    }
    
    /**
     * 设置alpha - 完全匹配Python的@alpha.setter
     */
    public void set_alpha(double alpha) throws TypeError, ValueError {
        if (alpha < 0) {
            throw new ValueError("`alpha` should be >= 0");
        }
        this._alpha = alpha;
    }
    
    /**
     * 获取beta - 完全匹配Python的@property beta
     */
    public double get_beta() {
        return this._beta;
    }
    
    /**
     * 设置beta - 完全匹配Python的@beta.setter
     */
    public void set_beta(double beta) throws TypeError, ValueError {
        if (beta <= 0 || beta > 2) {
            throw new ValueError("`beta` should be between 0 and 2");
        }
        this._beta = beta;
    }
    
    /**
     * 获取p - 完全匹配Python的@property p
     */
    public double get_p() {
        return this._p;
    }
    
    /**
     * 设置p - 完全匹配Python的@p.setter
     */
    public void set_p(double p) throws TypeError, ValueError {
        if (p < 0 || p > 1) {
            throw new ValueError("`p` should be between 0 and 1");
        }
        this._p = p;
    }
    
    /**
     * 内部构建方法 - 匹配Python的_build方法
     */
    @Override
    protected void _build() throws Exception {
        // Python版本没有额外的构建逻辑
    }
    
    /**
     * 内部编译方法 - 匹配Python的_compile方法
     */
    @Override
    protected void _compile(Space space) {
        // Python版本没有编译逻辑
    }
    
    /**
     * 生成新巢穴 - 完全匹配Python的_generate_new_nests方法
     * 
     * @param agents List of agents
     * @param best_agent Global best agent
     * @return A new list of agents which can be seen as new nests
     */
    private List<Agent> _generate_new_nests(List<Agent> agents, Agent best_agent) {
        // Makes a temporary copy of current agents - 完全匹配Python的copy.deepcopy
        List<Agent> new_agents = new ArrayList<>();
        for (Agent agent : agents) {
            new_agents.add(agent.copy());
        }
        
        // Then, we iterate for every agent - 完全匹配Python的逻辑
        for (Agent new_agent : new_agents) {
            // Calculates the Lévy distribution - 完全匹配Python的d.generate_levy_distribution
            double[] step = Distribution.generate_levy_distribution(this.get_beta(), new_agent.n_variables);
            
            // Expanding its dimension to perform entrywise multiplication - 匹配Python的np.expand_dims
            // 在Java中，我们直接使用一维数组进行计算
            
            // Calculates the difference vector between local and best positions
            // Alpha controls the intensity of the step size - 完全匹配Python的逻辑
            double[] step_size = new double[new_agent.n_variables];
            for (int i = 0; i < new_agent.n_variables; i++) {
                step_size[i] = this.get_alpha() * step[i] * 
                    (new_agent.position[i][0] - best_agent.position[i][0]);
            }
            
            // Generates a random normal distribution - 完全匹配Python的r.generate_gaussian_random_number
            double[] g = Random.generate_gaussian_random_number(0.0, 1.0, new_agent.n_variables);
            
            // Actually performs the random walk / flight - 完全匹配Python的逻辑
            for (int i = 0; i < new_agent.n_variables; i++) {
                new_agent.position[i][0] += step_size[i] * g[i];
            }
        }
        
        return new_agents;
    }
    
    /**
     * 生成废弃的巢穴 - 完全匹配Python的_generate_abandoned_nests方法
     * 
     * @param agents List of agents
     * @param prob Probability of replacing worst nests
     * @return A new list of agents which can be seen as the new nests to be replaced
     */
    private List<Agent> _generate_abandoned_nests(List<Agent> agents, double prob) {
        // Makes a temporary copy of current agents - 完全匹配Python的copy.deepcopy
        List<Agent> new_agents = new ArrayList<>();
        for (Agent agent : agents) {
            new_agents.add(agent.copy());
        }
        
        // Generates a bernoulli distribution array - 完全匹配Python的d.generate_bernoulli_distribution
        double[] b = Distribution.generate_bernoulli_distribution(1 - prob, agents.size());
        
        // Iterates through every new agent - 完全匹配Python的逻辑
        for (int j = 0; j < new_agents.size(); j++) {
            Agent new_agent = new_agents.get(j);
            
            // Generates a uniform random number - 完全匹配Python的r.generate_uniform_random_number
            double r1 = Random.generate_uniform_random_number(0.0, 1.0, 1)[0];
            
            // Then, we select two random nests - 完全匹配Python的r.generate_integer_random_number
            int k = Random.generate_integer_random_number(0, agents.size() - 1, null, 1)[0];
            int l = Random.generate_integer_random_number(0, agents.size() - 1, k, 1)[0];
            
            // Calculates the random walk between these two nests - 完全匹配Python的逻辑
            for (int i = 0; i < new_agent.n_variables; i++) {
                double step_size = r1 * (agents.get(k).position[i][0] - agents.get(l).position[i][0]);
                // Finally, we replace the old nest - 完全匹配Python的逻辑
                // Note it will only be replaced if 'b' is 1
                new_agent.position[i][0] += step_size * b[j];
            }
        }
        
        return new_agents;
    }
    
    /**
     * 评估巢穴 - 完全匹配Python的_evaluate_nests方法
     * 
     * @param agents List of current agents
     * @param new_agents List of new agents to be evaluated
     * @param function Fitness function used to evaluate
     */
    private void _evaluate_nests(List<Agent> agents, List<Agent> new_agents, Function function) {
        // Iterates through each agent and new agent - 完全匹配Python的zip逻辑
        for (int i = 0; i < agents.size(); i++) {
            Agent agent = agents.get(i);
            Agent new_agent = new_agents.get(i);
            
            // Checks agent's limits - 完全匹配Python的new_agent.clip_by_bound()
            new_agent.clip_by_bound();
            
            // Calculates the new agent fitness - 完全匹配Python的function(new_agent.position)
            double[] position = new double[new_agent.n_variables];
            for (int j = 0; j < new_agent.n_variables; j++) {
                position[j] = new_agent.position[j][0];
            }
            new_agent.fit = function.call(position);
            
            // If new agent's fitness is better than agent's - 完全匹配Python的逻辑
            if (new_agent.fit < agent.fit) {
                // Replace its position and fitness - 完全匹配Python的copy.deepcopy
                agent.position = new_agent.position.clone();
                agent.fit = new_agent.fit;
            }
        }
    }
    
    /**
     * 更新优化器 - 完全匹配Python的update方法
     * 
     * @param space Space containing agents and update-related information
     * @param function A Function object that will be used as the objective function
     */
    @Override
    public void update(Space space, Function function) {
        // Generate new nests - 完全匹配Python的逻辑
        List<Agent> new_agents = this._generate_new_nests(space.get_agents(), space.get_best_agent());
        
        // Evaluate new generated nests - 完全匹配Python的逻辑
        this._evaluate_nests(space.get_agents(), new_agents, function);
        
        // Generate new nests to be replaced - 完全匹配Python的逻辑
        new_agents = this._generate_abandoned_nests(space.get_agents(), this.get_p());
        
        // Evaluate new generated nests for further replacement - 完全匹配Python的逻辑
        this._evaluate_nests(space.get_agents(), new_agents, function);
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("CS{alpha=%.3f, beta=%.3f, p=%.3f, built=%s}", 
                           get_alpha(), get_beta(), get_p(), built);
    }
}