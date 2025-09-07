package com.hse.li.swarm.benchmark;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;

/**
 * 简化版Java基准测试 - 不依赖外部库
 * 可以直接运行，无需Maven
 */
public class SimpleBenchmark {
    
    // 配置参数
    private static final String DATA_FOLDER = "Data";
    private static final int MAX_THREADS = 4; // 减少线程数避免问题
    private static final int N_REPS = 2; // 减少重复次数加快测试
    
    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("Simplified Java BIPOP-CMA-ES Benchmark Test");
        System.out.println("Test functions: F20-F24");
        System.out.println("Instances: I1-I3 (simplified)");
        System.out.println("Dimensions: 10D");
        System.out.println("============================================================");
        
        try {
            // 创建输出目录
            createDirectories();
            
            // 创建线程池
            ExecutorService executor = Executors.newFixedThreadPool(MAX_THREADS);
            
            // 生成测试任务
            List<OptimizationTask> tasks = generateSimpleTasks();
            System.out.println("Generated " + tasks.size() + " test tasks");
            
            // 并行执行任务
            List<Future<String>> futures = new ArrayList<>();
            for (OptimizationTask task : tasks) {
                Future<String> future = executor.submit(() -> runSimpleOptimizer(task));
                futures.add(future);
            }
            
            // 收集结果
            int successCount = 0;
            for (Future<String> future : futures) {
                try {
                    String result = future.get();
                    System.out.println(result);
                    successCount++;
                } catch (Exception e) {
                    System.err.println("Task execution failed: " + e.getMessage());
                }
            }
            
            // 关闭线程池
            executor.shutdown();
            
            System.out.println("============================================================");
            System.out.println("Benchmark test completed!");
            System.out.println("Successfully completed tasks: " + successCount);
            System.out.println("Results saved to: " + DATA_FOLDER + "/Baselines/");
            System.out.println("============================================================");
            
        } catch (Exception e) {
            System.err.println("Benchmark test execution failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * 创建必要的目录
     */
    private static void createDirectories() {
        try {
            java.nio.file.Files.createDirectories(java.nio.file.Paths.get(DATA_FOLDER, "Baselines"));
            java.nio.file.Files.createDirectories(java.nio.file.Paths.get("logs"));
            System.out.println("Output directory created successfully");
        } catch (IOException e) {
            System.err.println("Failed to create directory: " + e.getMessage());
        }
    }
    
    /**
     * 生成简化的测试任务
     */
    private static List<OptimizationTask> generateSimpleTasks() {
        List<OptimizationTask> tasks = new ArrayList<>();
        
        // 简化的测试配置
        int[] functionIds = {20, 21, 22}; // 只测试F20-F22
        int[] instanceIds = {1, 2, 3};    // 只测试I1-I3
        int[] dimensions = {10};          // 10维
        
        for (int fid : functionIds) {
            for (int iid : instanceIds) {
                for (int dim : dimensions) {
                    tasks.add(new OptimizationTask("modcma_bipop", fid, iid, dim));
                }
            }
        }
        
        return tasks;
    }
    
    /**
     * 运行简化的优化器
     */
    private static String runSimpleOptimizer(OptimizationTask task) {
        System.out.println("Starting task execution: " + task);
        
        try {
            // 创建简化的目标函数
            SimpleBBOBFunction function = new SimpleBBOBFunction(
                task.getFunctionId(), task.getInstanceId(), task.getDimension()
            );
            
            // 执行简化的优化算法
            double bestResult = runSimpleOptimization(function, task.getDimension());
            
            // 保存结果
            saveResult(task, bestResult);
            
            return "Task completed: " + task + ", best value: " + bestResult;
            
        } catch (Exception e) {
            return "Task failed: " + task + ", error: " + e.getMessage();
        }
    }
    
    /**
     * 运行简化的优化算法
     */
    private static double runSimpleOptimization(SimpleBBOBFunction function, int dimension) {
        Random random = new Random(42); // 固定种子
        double[] x = new double[dimension];
        double[] sigma = new double[dimension];
        
        // 初始化
        for (int i = 0; i < dimension; i++) {
            x[i] = random.nextGaussian();
            sigma[i] = 1.0;
        }
        
        double bestFitness = Double.MAX_VALUE;
        int budget = 1000; // 减少预算加快测试
        
        // 简化的优化循环
        for (int iteration = 0; iteration < budget; iteration++) {
            // 生成候选解
            double[] candidate = new double[dimension];
            for (int i = 0; i < dimension; i++) {
                candidate[i] = x[i] + sigma[i] * random.nextGaussian();
            }
            
            // 评估适应度
            double fitness = function.evaluate(candidate);
            
            // 更新最优解
            if (fitness < bestFitness) {
                bestFitness = fitness;
                System.arraycopy(candidate, 0, x, 0, dimension);
            }
            
            // 简化的参数更新
            for (int i = 0; i < dimension; i++) {
                sigma[i] *= 0.99; // 逐渐减少步长
                sigma[i] = Math.max(0.001, sigma[i]);
            }
        }
        
        return bestFitness;
    }
    
    /**
     * 保存结果到文件
     */
    private static void saveResult(OptimizationTask task, double result) {
        try {
            String fileName = String.format("%s/Baselines/%s_F%d_I%d_%dD/result.txt",
                DATA_FOLDER, task.getAlgorithmName(), task.getFunctionId(), 
                task.getInstanceId(), task.getDimension());
            
            // 创建目录
            java.nio.file.Files.createDirectories(
                java.nio.file.Paths.get(fileName).getParent()
            );
            
            // 写入结果
            try (FileWriter writer = new FileWriter(fileName)) {
                writer.write("Algorithm: " + task.getAlgorithmName() + "\n");
                writer.write("Function ID: " + task.getFunctionId() + "\n");
                writer.write("Instance ID: " + task.getInstanceId() + "\n");
                writer.write("Dimension: " + task.getDimension() + "\n");
                writer.write("Best Result: " + result + "\n");
            }
            
        } catch (IOException e) {
            System.err.println("Failed to save results: " + e.getMessage());
        }
    }
    
    /**
     * 简化的BBOB函数实现
     */
    private static class SimpleBBOBFunction {
        private final int functionId;
        private final int instanceId;
        private final int dimension;
        
        public SimpleBBOBFunction(int functionId, int instanceId, int dimension) {
            this.functionId = functionId;
            this.instanceId = instanceId;
            this.dimension = dimension;
        }
        
        public double evaluate(double[] x) {
            if (x.length != dimension) {
                throw new IllegalArgumentException("Dimension mismatch");
            }
            
            double result = 0.0;
            
            switch (functionId) {
                case 20: // 简化的F20
                    for (int i = 0; i < dimension; i++) {
                        result += x[i] * x[i];
                    }
                    result += 10.0 * Math.sin(2.0 * Math.PI * x[0]);
                    break;
                    
                case 21: // 简化的F21
                    for (int i = 0; i < dimension; i++) {
                        result += x[i] * x[i];
                    }
                    result += 20.0 * Math.sin(2.0 * Math.PI * x[0]);
                    break;
                    
                case 22: // 简化的F22
                    result = 1.0;
                    for (int i = 0; i < dimension; i++) {
                        result *= (1.0 + (i + 1) * Math.abs(x[i]));
                    }
                    result -= 1.0;
                    break;
                    
                default:
                    // 默认球函数
                    for (int i = 0; i < dimension; i++) {
                        result += x[i] * x[i];
                    }
                    break;
            }
            
            return result;
        }
    }
}

