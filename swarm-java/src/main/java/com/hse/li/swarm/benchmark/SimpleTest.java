package com.hse.li.swarm.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 简单的测试类
 */
public class SimpleTest {
    private static final Logger logger = LoggerFactory.getLogger(SimpleTest.class);
    
    public static void main(String[] args) {
        logger.info("Java 项目测试开始...");
        
        try {
            // 测试基本功能
            logger.info("测试 1: 创建优化任务");
            OptimizationTask task = new OptimizationTask("modcma_bipop", 20, 1, 10);
            logger.info("任务创建成功: {}", task);
            
            logger.info("测试 2: 创建算法评估器");
            AlgorithmEvaluator evaluator = new AlgorithmEvaluator("modcma_bipop");
            logger.info("算法评估器创建成功: {}", evaluator.getAlgorithmName());
            
            logger.info("测试 3: 创建BBOB问题");
            com.hse.li.swarm.ioh.BBOBProblem problem = com.hse.li.swarm.ioh.IOHProblemFactory.getProblem(20, 10, 1);
            logger.info("BBOB问题创建成功: F{}, {}D, I{}", problem.getFunctionId(), problem.getDimension(), problem.getInstanceId());
            
            logger.info("测试 4: 评估函数");
            double[] testSolution = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0};
            double fitness = problem.evaluate(testSolution);
            logger.info("函数评估成功: 适应度 = {}", fitness);
            
            logger.info("所有测试通过！Java 项目工作正常。");
            
        } catch (Exception e) {
            logger.error("测试失败: {}", e.getMessage(), e);
        }
    }
}
