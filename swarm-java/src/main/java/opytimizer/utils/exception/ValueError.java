package opytimizer.utils.exception;

/**
 * 值错误类 - 匹配Python的ValueError
 */
public class ValueError extends Error {
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param error Error message to be logged
     */
    public ValueError(String error) {
        super("ValueError", error);
    }
}
