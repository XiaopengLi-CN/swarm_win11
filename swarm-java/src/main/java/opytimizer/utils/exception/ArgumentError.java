package opytimizer.utils.exception;

/**
 * 参数错误类 - 匹配Python的ArgumentError
 */
public class ArgumentError extends Error {
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param error Error message to be logged
     */
    public ArgumentError(String error) {
        super("ArgumentError", error);
    }
}
