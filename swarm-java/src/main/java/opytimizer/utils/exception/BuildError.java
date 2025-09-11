package opytimizer.utils.exception;

/**
 * 构建错误类 - 匹配Python的BuildError
 */
public class BuildError extends Error {
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param error Error message to be logged
     */
    public BuildError(String error) {
        super("BuildError", error);
    }
}
