package com.hse.li.swarm.modcma;

import java.util.HashMap;
import java.util.Map;

/**
 * modcma参数配置系统 - 对应Python中的modcma_params
 * 严格按照Python实现：
 * modcma_params = { 'base' : {},
 *                   'bipop' : {
 *                   'local_restart' : 'BIPOP'
 *                   }}
 */
public class ModCMAConfig {
    
    private static final Map<String, Map<String, Object>> MODCMA_PARAMS = new HashMap<>();
    
    // 私有构造函数防止实例化
    private ModCMAConfig() {
        throw new UnsupportedOperationException("Utility class");
    }
    
    static {
        // 初始化base参数（空配置）
        Map<String, Object> baseParams = new HashMap<>();
        MODCMA_PARAMS.put("base", baseParams);
        
        // 初始化bipop参数
        Map<String, Object> bipopParams = new HashMap<>();
        bipopParams.put("local_restart", "BIPOP");
        // 添加BIPOP特定参数
        bipopParams.put("lambda_init", 4);
        bipopParams.put("mu_factor", 0.5);
        MODCMA_PARAMS.put("bipop", bipopParams);
    }
    
    /**
     * 获取算法参数 - 对应Python中的modcma_params[self.alg[7:]]
     * @param algorithmName 完整算法名称，如"modcma_bipop"
     * @return 对应的参数配置
     */
    public static Map<String, Object> getAlgorithmParams(String algorithmName) {
        // 提取算法类型 - 对应Python中的self.alg[7:]
        // 从"modcma_bipop"提取"bipop"
        String algorithmType = algorithmName.substring(7); // 跳过"modcma_"
        
        Map<String, Object> params = MODCMA_PARAMS.get(algorithmType);
        if (params == null) {
            // 如果找不到对应参数，返回base参数
            params = MODCMA_PARAMS.get("base");
        }
        
        return new HashMap<>(params); // 返回副本避免修改原始配置
    }
    
    /**
     * 获取所有可用的算法类型
     * @return 算法类型集合
     */
    public static String[] getAvailableAlgorithmTypes() {
        return MODCMA_PARAMS.keySet().toArray(new String[0]);
    }
    
    /**
     * 检查算法类型是否存在
     * @param algorithmType 算法类型
     * @return 是否存在
     */
    public static boolean hasAlgorithmType(String algorithmType) {
        return MODCMA_PARAMS.containsKey(algorithmType);
    }
    
    /**
     * 添加新的算法参数配置
     * @param algorithmType 算法类型
     * @param params 参数配置
     */
    public static void addAlgorithmParams(String algorithmType, Map<String, Object> params) {
        MODCMA_PARAMS.put(algorithmType, new HashMap<>(params));
    }
}


