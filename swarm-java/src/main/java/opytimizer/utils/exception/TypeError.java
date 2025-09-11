package opytimizer.utils.exception;

/**
 * 类型错误类 - 匹配Python的TypeError
 */
public class TypeError extends Error {
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param error Error message to be logged
     */
    public TypeError(String error) {
        super("TypeError", error);
    }
}
