package com.hse.li.swarm.modcma;

/**
 * 目标函数接口 - 对应Python中的IOH函数
 * 定义优化问题的目标函数
 */
public interface ObjectiveFunction {
    
    /**
     * 评估目标函数
     * @param x 输入向量
     * @return 函数值
     */
    double evaluate(double[] x);
    
    /**
     * 获取函数ID
     * @return 函数ID
     */
    int getFunctionId();
    
    /**
     * 获取实例ID
     * @return 实例ID
     */
    int getInstanceId();
    
    /**
     * 获取维度
     * @return 维度
     */
    int getDimension();
    
    /**
     * 重置函数状态
     */
    void reset();
    
    /**
     * 获取最优值
     * @return 最优值
     */
    double getOptimalValue();
}


