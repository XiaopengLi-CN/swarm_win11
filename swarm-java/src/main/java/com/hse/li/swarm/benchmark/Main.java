package com.hse.li.swarm.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.hse.li.swarm.ioh.AnalyzerLogger;
import com.hse.li.swarm.ioh.BBOBProblem;
import com.hse.li.swarm.ioh.IOHProblemFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

/**
 * Main benchmark test class - corresponds to benchmark_baselines.py in Python
 * Strictly follows Python implementation with complete AnalyzerLogger functionality
 * 
 * Python implementation reference:
 * def main():
 *     fids = range(20,25)  # Test F20-F24
 *     algnames = ["modcma_bipop"]
 *     iids = range(1,11)  # Test I1-I10, total 10 instances
 *     dims = [10]  # Only test 10 dimensions
 *     args = product(algnames, fids, iids, dims)
 *     runParallelFunction(run_optimizer, args)
 * 
 * def run_optimizer(temp):
 *     algname, fid, iid, dim = temp
 *     print(algname, fid, iid, dim)
 *     algorithm = Algorithm_Evaluator(algname)
 *     logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/Baselines/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")
 *     func = ioh.get_problem(fid, dimension=dim, instance=iid)
 *     func.attach_logger(logger)
 *     algorithm(func, 5)
 *     logger.close()
 */
public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    
    // Data folder path - corresponds to DATA_FOLDER in Python
    private static final String DATA_FOLDER = "Data";
    
    // Maximum thread count - corresponds to MAX_THREADS in Python
    private static final int MAX_THREADS = 32;
    
    public static void main(String[] args) {
        logger.info("Starting Java version benchmark test...");
        
        try {
            // Setup environment variables - corresponds to environment setup in Python
            setupEnvironmentVariables();
            setupWarningFilters();
            
            // Run benchmark test
            runBenchmark();
            
            logger.info("Benchmark test completed!");
            
        } catch (Exception e) {
            logger.error("Benchmark test failed: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Setup environment variables - corresponds to environment setup in Python
     */
    private static void setupEnvironmentVariables() {
        System.setProperty("OMP_NUM_THREADS", "1");
        System.setProperty("OPENBLAS_NUM_THREADS", "1");
        logger.info("Environment variables setup completed");
    }
    
    /**
     * Setup warning filters - corresponds to warning setup in Python
     */
    private static void setupWarningFilters() {
        // In Java, warnings can be controlled through log levels
        logger.debug("Warning filters setup completed");
    }
    
    /**
     * Run benchmark test - corresponds to main() function in Python
     * Strictly follows Python implementation:
     * fids = range(20,25)  # Test F20-F24
     * algnames = ["modcma_bipop"]
     * iids = range(1,11)  # Test I1-I10, total 10 instances
     * dims = [10]  # Only test 10 dimensions
     * args = product(algnames, fids, iids, dims)
     * runParallelFunction(run_optimizer, args)
     */
    private static void runBenchmark() {
        logger.info("Starting benchmark test...");
        
        // Define test parameters - strictly follows Python implementation
        int[] fids = {20, 21, 22, 23, 24}; // range(20,25) - Test F20-F24
        String[] algnames = {"modcma_bipop"}; // ["modcma_bipop"]
        int[] iids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}; // range(1,11) - Test I1-I10, total 10 instances
        int[] dims = {10}; // [10] - Only test 10 dimensions
        
        // Create optimization task list - corresponds to product(algnames, fids, iids, dims) in Python
        List<OptimizationTask> tasks = new ArrayList<>();
        for (String algname : algnames) {
            for (int fid : fids) {
                for (int iid : iids) {
                    for (int dim : dims) {
                        tasks.add(new OptimizationTask(algname, fid, iid, dim));
                    }
                }
            }
        }
        
        logger.info("Created {} optimization tasks", tasks.size());
        
        // Use parallel executor to run tasks - corresponds to runParallelFunction(run_optimizer, args) in Python
        runParallelFunction(tasks);
    }
    
    /**
     * Parallel execution function - corresponds to runParallelFunction() in Python
     * @param tasks Task list
     */
    private static void runParallelFunction(List<OptimizationTask> tasks) {
        ExecutorService executor = Executors.newFixedThreadPool(MAX_THREADS);
        List<Future<String>> futures = new ArrayList<>();
        
        try {
            // Submit all tasks
            for (OptimizationTask task : tasks) {
                Future<String> future = executor.submit(() -> runOptimizer(task));
                futures.add(future);
            }
            
            // Wait for all tasks to complete and collect results
            for (Future<String> future : futures) {
                try {
                    String result = future.get(30, TimeUnit.MINUTES); // 30 minutes timeout
                    logger.info(result);
                } catch (Exception e) {
                    logger.error("Task execution failed: {}", e.getMessage(), e);
                }
            }
            
        } finally {
            executor.shutdown();
            try {
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }
    }
    
    /**
     * Run optimizer - corresponds to run_optimizer() function in Python
     * Strictly follows Python implementation:
     * def run_optimizer(temp):
     *     algname, fid, iid, dim = temp
     *     print(algname, fid, iid, dim)
     *     algorithm = Algorithm_Evaluator(algname)
     *     logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/Baselines/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")
     *     func = ioh.get_problem(fid, dimension=dim, instance=iid)
     *     func.attach_logger(logger)
     *     algorithm(func, 5)
     *     logger.close()
     */
    private static String runOptimizer(OptimizationTask task) {
        try {
            String algname = task.getAlgorithmName();
            int fid = task.getFunctionId();
            int iid = task.getInstanceId();
            int dim = task.getDimension();
            
            // Output task information - corresponds to print(algname, fid, iid, dim) in Python
            logger.info("Running task: {} {} {} {}", algname, fid, iid, dim);
            
            // Create algorithm evaluator - corresponds to algorithm = Algorithm_Evaluator(algname) in Python
            AlgorithmEvaluator algorithm = new AlgorithmEvaluator(algname);
            
            // Create AnalyzerLogger - corresponds to logger = ioh.logger.Analyzer(...) in Python
            String folderName = String.format("%s_F%d_I%d_%dD", algname, fid, iid, dim);
            AnalyzerLogger analyzerLogger = new AnalyzerLogger(
                DATA_FOLDER + "/Baselines/",  // root=f"{DATA_FOLDER}/Baselines/"
                folderName,                   // folder_name=f"{algname}_F{fid}_I{iid}_{dim}D"
                algname                       // algorithm_name=f"{algname}"
            );
            
            // Create BBOB problem - corresponds to func = ioh.get_problem(fid, dimension=dim, instance=iid) in Python
            BBOBProblem func = IOHProblemFactory.getProblem(fid, dim, iid);
            
            // Attach logger - corresponds to func.attach_logger(logger) in Python
            func.attachLogger(analyzerLogger);
            
            // Run algorithm evaluation - corresponds to algorithm(func, 5) in Python
            algorithm.evaluate(func, 5);
            
            // Close logger - corresponds to logger.close() in Python
            analyzerLogger.close();
            
            return String.format("Task completed: %s", task);
            
        } catch (Exception e) {
            logger.error("Task failed: {} - {}", task, e.getMessage(), e);
            return String.format("Task failed: %s - %s", task, e.getMessage());
        }
    }
}