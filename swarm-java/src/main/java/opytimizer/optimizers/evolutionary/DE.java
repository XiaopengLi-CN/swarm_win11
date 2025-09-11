package opytimizer.optimizers.evolutionary;

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
 * Java版本的DE类 - 完全复现Python的de.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/optimizers/evolutionary/de.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class DE extends Optimizer {
    
    private static final Logger logger = Logger.get_logger(DE.class.getName());
    
    // 完全匹配Python的属性名 - 使用私有属性+getter/setter
    private double _CR;
    private double _F;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param params Contains key-value parameters to the meta-heuristics
     */
    public DE(Map<String, Object> params) throws Exception {
        super(params);
        
        logger.info("Overriding class: Optimizer -> DE.");
        
        // 完全匹配Python的属性赋值
        this.set_CR(0.9);
        this.set_F(0.7);
        
        // 构建类
        this.build(params);
        
        logger.info("Class overrided.");
    }
    
    /**
     * 构造函数重载 - 无参数
     */
    public DE() throws Exception {
        this(null);
    }
    
    /**
     * 获取CR - 完全匹配Python的@property CR
     */
    public double get_CR() {
        return this._CR;
    }
    
    /**
     * 设置CR - 完全匹配Python的@CR.setter
     */
    public void set_CR(double CR) throws TypeError, ValueError {
        if (CR < 0 || CR > 1) {
            throw new ValueError("`CR` should be between 0 and 1");
        }
        this._CR = CR;
    }
    
    /**
     * 获取F - 完全匹配Python的@property F
     */
    public double get_F() {
        return this._F;
    }
    
    /**
     * 设置F - 完全匹配Python的@F.setter
     */
    public void set_F(double F) throws TypeError, ValueError {
        if (F < 0 || F > 2) {
            throw new ValueError("`F` should be between 0 and 2");
        }
        this._F = F;
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
     * 变异智能体 - 完全匹配Python的_mutate_agent方法
     * 
     * @param agent Current agent
     * @param alpha 1st picked agent
     * @param beta 2nd picked agent
     * @param gamma 3rd picked agent
     * @return A mutated agent
     */
    private Agent _mutate_agent(Agent agent, Agent alpha, Agent beta, Agent gamma) {
        // Makes a deep copy of agent - 完全匹配Python的copy.deepcopy
        Agent a = agent.copy();
        
        // Generates a random index for further comparison - 完全匹配Python的r.generate_integer_random_number
        int R = Random.generate_integer_random_number(0, agent.n_variables, null, 1)[0];
        
        // For every decision variable - 完全匹配Python的逻辑
        for (int j = 0; j < a.n_variables; j++) {
            // Generates a uniform random number - 完全匹配Python的r.generate_uniform_random_number
            double r1 = Random.generate_uniform_random_number(0.0, 1.0, 1)[0];
            
            // If random number is smaller than crossover or `j` equals to the sampled index - 完全匹配Python的逻辑
            if (r1 < this.get_CR() || j == R) {
                // Updates the mutated agent position - 完全匹配Python的逻辑
                for (int d = 0; d < a.n_dimensions; d++) {
                    a.position[j][d] = alpha.position[j][d] + this.get_F() * 
                        (beta.position[j][d] - gamma.position[j][d]);
                }
            }
        }
        
        return a;
    }
    
    /**
     * 更新优化器 - 完全匹配Python的update方法
     * 
     * @param space Space containing agents and update-related information
     * @param function A Function object that will be used as the objective function
     */
    @Override
    public void update(Space space, Function function) {
        List<Agent> agents = space.get_agents();
        
        // Iterates through all agents - 完全匹配Python的逻辑
        for (int i = 0; i < agents.size(); i++) {
            Agent agent = agents.get(i);
            
            // Randomly picks three distinct other agents, not including current one - 完全匹配Python的逻辑
            List<Integer> available_indices = new ArrayList<>();
            for (int j = 0; j < agents.size(); j++) {
                if (j != i) {
                    available_indices.add(j);
                }
            }
            
            // 选择三个不同的智能体
            int[] C = new int[3];
            for (int k = 0; k < 3; k++) {
                int randomIndex = Random.generate_integer_random_number(0, available_indices.size(), null, 1)[0];
                C[k] = available_indices.get(randomIndex);
                available_indices.remove(randomIndex);
            }
            
            // Mutates the current agent - 完全匹配Python的逻辑
            Agent a = this._mutate_agent(agent, agents.get(C[0]), agents.get(C[1]), agents.get(C[2]));
            
            // Checks agent's limits - 完全匹配Python的a.clip_by_bound()
            a.clip_by_bound();
            
            // Calculates the fitness for the temporary position - 完全匹配Python的function(a.position)
            double[] position = new double[a.n_variables];
            for (int j = 0; j < a.n_variables; j++) {
                position[j] = a.position[j][0];
            }
            a.fit = function.call(position);
            
            // If new fitness is better than agent's fitness - 完全匹配Python的逻辑
            if (a.fit < agent.fit) {
                // Copies its position and fitness to the agent - 完全匹配Python的copy.deepcopy
                agent.position = a.position.clone();
                agent.fit = a.fit;
            }
        }
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("DE{CR=%.3f, F=%.3f, built=%s}", 
                           get_CR(), get_F(), built);
    }
}
