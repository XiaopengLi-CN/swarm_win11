package com.hse.li.swarm.ioh;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * IOH问题获取接口 - 对应Python中的ioh.get_problem()
 * 负责创建BBOB测试问题实例
 */
public class IOHProblemFactory {
    private static final Logger logger = LoggerFactory.getLogger(IOHProblemFactory.class);
    
    /**
     * 函数名称映射 - 对应Python中的函数名称
     */
    public static final java.util.Map<Integer, String> FUNCTION_NAMES = new java.util.HashMap<>();
    static {
        FUNCTION_NAMES.put(20, "Schwefel");
        FUNCTION_NAMES.put(21, "Gallagher101");
        FUNCTION_NAMES.put(22, "Gallagher21");
        FUNCTION_NAMES.put(23, "Katsuura");
        FUNCTION_NAMES.put(24, "Lunacek");
    }
    
    /**
     * 获取BBOB问题实例 - 对应Python中的ioh.get_problem(fid, dimension=dim, instance=iid)
     * 严格按照env_win11环境中的ioh.get_problem()实现
     * @param functionId 函数ID (F20-F24)
     * @param dimension 问题维度
     * @param instance 实例ID (I1-I10)
     * @return BBOB问题实例
     */
    public static BBOBProblem getProblem(int functionId, int dimension, int instance) {
        // 验证BBOB函数维度要求 - 对应env_win11中的验证逻辑
        if (functionId >= 1 && functionId <= 24) {
            if (dimension < 2) {
                throw new IllegalArgumentException("For BBOB functions the minimal dimension is 2");
            }
        }
        
        logger.debug("创建BBOB问题: F{}, {}D, I{}", functionId, dimension, instance);
        
        // 创建BBOB问题实例
        BBOBProblem problem = new BBOBProblem(functionId, dimension, instance);
        
        // 设置问题元数据
        problem.setMetaData(new ProblemMetaData(functionId, dimension, instance));
        
        return problem;
    }
    
    /**
     * 问题元数据类 - 对应Python中的func.meta_data
     */
    public static class ProblemMetaData {
        private final int functionId;
        private final int dimension;
        private final int instance;
        private final String functionName;
        
        public ProblemMetaData(int functionId, int dimension, int instance) {
            this.functionId = functionId;
            this.dimension = dimension;
            this.instance = instance;
            this.functionName = getFunctionName(functionId);
        }
        
        public ProblemMetaData(int functionId, String functionName, int dimension, int instance) {
            this.functionId = functionId;
            this.dimension = dimension;
            this.instance = instance;
            this.functionName = functionName;
        }
        
        public int getFunctionId() { return functionId; }
        public int getDimension() { return dimension; }
        public int getInstance() { return instance; }
        public String getFunctionName() { return functionName; }
        public int getNVariables() { return dimension; }
        
        private String getFunctionName(int fid) {
            switch (fid) {
                case 20: return "Schwefel";
                case 21: return "Gallagher101";
                case 22: return "Gallagher21";
                case 23: return "Katsuura";
                case 24: return "LunacekBiRastrigin";
                default: return "Unknown";
            }
        }
    }
}


