package opytimizer.core;

import opytimizer.utils.logging.Logger;
import opytimizer.utils.exception.TypeError;
import opytimizer.utils.exception.ArgumentError;

/**
 * Java版本的Function类 - 完全复现Python的function.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/core/function.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Function {
    
    private static final Logger logger = Logger.get_logger(Function.class.getName());
    
    // 完全匹配Python的属性名
    private java.util.function.Function<double[], Double> _pointer;
    private String _name;
    private boolean _built;
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param pointer Pointer to a function that will return the fitness value
     */
    public Function(java.util.function.Function<double[], Double> pointer) {
        logger.info("Creating class: Function.");
        
        // 完全匹配Python的属性赋值
        this._pointer = pointer;
        
        // 获取函数名称 - 匹配Python的逻辑
        if (pointer != null) {
            this._name = pointer.getClass().getSimpleName();
        } else {
            this._name = "Unknown";
        }
        
        // 如果无误，声明函数为built
        this._built = true;
        
        logger.debug("Function: %s | Built: %s.", this._name, this._built);
        logger.info("Class created.");
    }
    
    /**
     * 构造函数重载 - 带名称
     */
    public Function(java.util.function.Function<double[], Double> pointer, String name) {
        logger.info("Creating class: Function.");
        
        this._pointer = pointer;
        this._name = name;
        this._built = true;
        
        logger.debug("Function: %s | Built: %s.", this._name, this._built);
        logger.info("Class created.");
    }
    
    /**
     * 调用函数 - 匹配Python的__call__方法
     * 
     * @param x Array of positions
     * @return Single-objective function fitness
     */
    public double call(double[] x) {
        return this._pointer.apply(x);
    }
    
    /**
     * 获取指针 - 匹配Python的pointer属性
     */
    public java.util.function.Function<double[], Double> get_pointer() {
        return this._pointer;
    }
    
    /**
     * 设置指针 - 匹配Python的pointer属性
     */
    public void set_pointer(java.util.function.Function<double[], Double> pointer) {
        if (pointer == null) {
            throw new TypeError("`pointer` should be a callable");
        }
        
        this._pointer = pointer;
    }
    
    /**
     * 获取名称 - 匹配Python的name属性
     */
    public String get_name() {
        return this._name;
    }
    
    /**
     * 设置名称 - 匹配Python的name属性
     */
    public void set_name(String name) {
        if (name == null) {
            throw new TypeError("`name` should be a string");
        }
        
        this._name = name;
    }
    
    /**
     * 获取构建状态 - 匹配Python的built属性
     */
    public boolean get_built() {
        return this._built;
    }
    
    /**
     * 设置构建状态 - 匹配Python的built属性
     */
    public void set_built(boolean built) {
        this._built = built;
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Function{name='%s', built=%s}", _name, _built);
    }
}
