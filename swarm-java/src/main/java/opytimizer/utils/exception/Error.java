package opytimizer.utils.exception;

import opytimizer.utils.logging.Logger;

/**
 * Java版本的异常基类 - 完全复现Python的exception.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/utils/exception.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Error extends Exception {
    
    private static final Logger logger = Logger.get_logger(Error.class.getName());
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param cls Class identifier
     * @param msg Message to be logged
     */
    public Error(String cls, String msg) {
        super();
        
        // 记录错误日志 - 匹配Python的逻辑
        logger.error("%s: %s.", cls, msg);
    }
}