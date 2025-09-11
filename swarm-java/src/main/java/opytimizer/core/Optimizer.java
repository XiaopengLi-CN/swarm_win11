package opytimizer.core;

import opytimizer.utils.logging.Logger;
import opytimizer.utils.exception.TypeError;
import opytimizer.utils.exception.ValueError;
import opytimizer.utils.exception.BuildError;
import java.util.Map;
import java.util.HashMap;

/**
 * Java版本的Optimizer类 - 完全复现Python的optimizer.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/core/optimizer.py
 * 
 * 类名、方法名、参数名完全一致
 */
public abstract class Optimizer {
    
    private static final Logger logger = Logger.get_logger(Optimizer.class.getName());
    
    // 完全匹配Python的属性名
    public Map<String, Object> params;
    public boolean built;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param params Contains key-value parameters to the meta-heuristics
     */
    public Optimizer(Map<String, Object> params) {
        logger.info("Overriding class: Optimizer -> %s.", this.getClass().getSimpleName());
        
        // 完全匹配Python的属性赋值
        this.params = params != null ? new HashMap<>(params) : new HashMap<>();
        this.built = false;
        
        logger.info("Class overrided.");
    }
    
    /**
     * 构造函数重载 - 无参数
     */
    public Optimizer() {
        this(null);
    }
    
    /**
     * 构建优化器 - 完全匹配Python的build方法
     * 
     * @param params Contains key-value parameters to the meta-heuristics
     */
    public void build(Map<String, Object> params) throws Exception {
        logger.info("Building optimizer: %s.", this.getClass().getSimpleName());
        
        if (params != null) {
            this.params.putAll(params);
        }
        
        this._build();
        this.built = true;
        
        logger.info("Optimizer built successfully.");
    }
    
    /**
     * 内部构建方法 - 匹配Python的_build方法
     */
    protected abstract void _build() throws Exception;
    
    /**
     * 更新优化器 - 完全匹配Python的update方法
     * 
     * @param space Space containing agents and update-related information
     * @param function A Function object that will be used as the objective function
     */
    public abstract void update(Space space, Function function);
    
    /**
     * 编译优化器 - 完全匹配Python的compile方法
     * 
     * @param space Space containing agents and update-related information
     */
    public void compile(Space space) {
        logger.info("Compiling optimizer: %s.", this.getClass().getSimpleName());
        
        if (!space.get_built()) {
            throw new BuildError("Space should be built before compiling optimizer");
        }
        
        this._compile(space);
        this.built = true;
        
        logger.info("Optimizer compiled successfully.");
    }
    
    /**
     * 内部编译方法 - 匹配Python的_compile方法
     */
    protected abstract void _compile(Space space);
    
    /**
     * 获取参数 - 匹配Python的params属性
     */
    public Map<String, Object> get_params() {
        return this.params;
    }
    
    /**
     * 设置参数 - 匹配Python的params属性
     */
    public void set_params(Map<String, Object> params) {
        this.params = params != null ? new HashMap<>(params) : new HashMap<>();
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
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("%s{built=%s}", this.getClass().getSimpleName(), built);
    }
}
