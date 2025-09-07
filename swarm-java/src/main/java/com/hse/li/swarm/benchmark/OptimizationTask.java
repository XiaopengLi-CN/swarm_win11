package com.hse.li.swarm.benchmark;

/**
 * 优化任务参数 - 对应Python中的temp参数
 * 包含算法名称、函数ID、实例ID和维度
 */
public class OptimizationTask {
    private final String algorithmName;
    private final int functionId;
    private final int instanceId;
    private final int dimension;
    
    public OptimizationTask(String algorithmName, int functionId, int instanceId, int dimension) {
        this.algorithmName = algorithmName;
        this.functionId = functionId;
        this.instanceId = instanceId;
        this.dimension = dimension;
    }
    
    public String getAlgorithmName() {
        return algorithmName;
    }
    
    public int getFunctionId() {
        return functionId;
    }
    
    public int getInstanceId() {
        return instanceId;
    }
    
    public int getDimension() {
        return dimension;
    }
    
    @Override
    public String toString() {
        return String.format("OptimizationTask{algorithm='%s', fid=%d, iid=%d, dim=%d}", 
            algorithmName, functionId, instanceId, dimension);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        OptimizationTask that = (OptimizationTask) obj;
        return functionId == that.functionId &&
               instanceId == that.instanceId &&
               dimension == that.dimension &&
               algorithmName.equals(that.algorithmName);
    }
    
    @Override
    public int hashCode() {
        int result = algorithmName.hashCode();
        result = 31 * result + functionId;
        result = 31 * result + instanceId;
        result = 31 * result + dimension;
        return result;
    }
}

