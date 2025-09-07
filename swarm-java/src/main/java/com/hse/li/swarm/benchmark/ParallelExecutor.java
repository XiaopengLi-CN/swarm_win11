package com.hse.li.swarm.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.function.Function;

/**
 * 并行执行管理器 - 对应Python中的runParallelFunction
 * 负责管理多线程并行执行优化任务
 */
public class ParallelExecutor {
    private static final Logger logger = LoggerFactory.getLogger(ParallelExecutor.class);
    
    private final int maxThreads;
    private final ExecutorService executorService;
    
    public ParallelExecutor(int maxThreads) {
        this.maxThreads = maxThreads;
        this.executorService = Executors.newFixedThreadPool(maxThreads);
        logger.info("Initializing parallel executor, max threads: {}", maxThreads);
    }
    
    /**
     * 并行执行函数 - 对应Python中的runParallelFunction
     * @param function 要执行的函数
     * @param arguments 参数列表
     * @param <T> 参数类型
     * @param <R> 返回类型
     * @return 结果列表
     */
    public <T, R> List<R> runParallelFunction(Function<T, R> function, List<T> arguments) {
        logger.info("Starting parallel execution, task count: {}, thread count: {}", arguments.size(), maxThreads);
        
        List<Future<R>> futures = new ArrayList<>();
        
        // 提交所有任务
        for (T argument : arguments) {
            Future<R> future = executorService.submit(() -> {
                try {
                    return function.apply(argument);
                } catch (Exception e) {
                    logger.error("Task execution failed: {}", e.getMessage());
                    throw new RuntimeException(e);
                }
            });
            futures.add(future);
        }
        
        // 收集结果
        List<R> results = new ArrayList<>();
        for (Future<R> future : futures) {
            try {
                R result = future.get(); // 等待任务完成
                results.add(result);
            } catch (InterruptedException | ExecutionException e) {
                logger.error("Failed to get task result: {}", e.getMessage());
                throw new RuntimeException(e);
            }
        }
        
        logger.info("Parallel execution completed, successful tasks: {}", results.size());
        return results;
    }
    
    /**
     * 关闭执行器
     */
    public void shutdown() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(60, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
                logger.warn("Force shutdown executor");
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
        logger.info("Parallel executor closed");
    }
    
    /**
     * 获取当前活跃线程数
     */
    public int getActiveThreadCount() {
        return ((ThreadPoolExecutor) executorService).getActiveCount();
    }
    
    /**
     * 获取已完成任务数
     */
    public long getCompletedTaskCount() {
        return ((ThreadPoolExecutor) executorService).getCompletedTaskCount();
    }
}

