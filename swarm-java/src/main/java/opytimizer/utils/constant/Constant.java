package opytimizer.utils.constant;

import java.util.Map;
import java.util.HashMap;

/**
 * Java版本的常量类 - 完全复现Python的constant.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/utils/constant.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Constant {
    
    // 完全匹配Python的常量定义
    public static final double EPSILON = 1e-32;
    public static final double FLOAT_MAX = Double.MAX_VALUE;
    public static final double LIGHT_SPEED = 3e5;
    public static final double TEST_EPSILON = 100;
    
    // 完全匹配Python的FUNCTION_N_ARGS字典
    public static final Map<String, Integer> FUNCTION_N_ARGS = Map.of(
        "SUM", 2,
        "SUB", 2,
        "MUL", 2,
        "DIV", 2,
        "EXP", 1,
        "SQRT", 1,
        "LOG", 1,
        "ABS", 1,
        "SIN", 1,
        "COS", 1
    );
}
