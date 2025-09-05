package com.swarm.benchmark;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Main class for running benchmark experiments.
 * This corresponds to the main part of benchmark_baselines.py.
 */
public class BenchmarkBaselines {
    private static final Logger logger = LogManager.getLogger(BenchmarkBaselines.class);
    
    private static final String DATA_FOLDER = "Data";
    private static final int MAX_THREADS = 32;
    
    public static void main(String[] args) {
        logger.info("Starting BIPOP-CMA-ES benchmark...");
        
        // Define experiment parameters (same as Python version)
        List<Integer> fids = List.of(1); // Only F1 (Sphere)
        List<String> algnames = List.of("modcma_bipop");
        List<Integer> iids = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10); // I1-I10
        List<Integer> dims = List.of(10); // Only 10D
        
        // Create all combinations
        List<ExperimentConfig> experiments = new ArrayList<>();
        for (String algname : algnames) {
            for (int fid : fids) {
                for (int iid : iids) {
                    for (int dim : dims) {
                        experiments.add(new ExperimentConfig(algname, fid, iid, dim));
                    }
                }
            }
        }
        
        logger.info("Created " + experiments.size() + " experiments to run");
        
        // Run experiments in parallel
        runParallelExperiments(experiments);
        
        logger.info("All experiments completed!");
    }
    
    /**
     * Runs experiments in parallel using a thread pool.
     */
    private static void runParallelExperiments(List<ExperimentConfig> experiments) {
        int numThreads = Math.min(MAX_THREADS, experiments.size());
        logger.info("Using " + numThreads + " threads for parallel execution");
        
        try (ExecutorService executor = Executors.newFixedThreadPool(numThreads)) {
            List<Future<Void>> futures = new ArrayList<>();
            
            for (ExperimentConfig config : experiments) {
                Future<Void> future = executor.submit(() -> {
                    runOptimizer(config);
                    return null;
                });
                futures.add(future);
            }
            
            // Wait for all experiments to complete
            for (Future<Void> future : futures) {
                future.get();
            }
        } catch (Exception e) {
            logger.error("Error during parallel execution", e);
        }
    }
    
    /**
     * Runs a single optimization experiment.
     */
    private static void runOptimizer(ExperimentConfig config) {
        String algname = config.algorithmName;
        int fid = config.functionId;
        int iid = config.instanceId;
        int dim = config.dimension;
        
        logger.info("Running: " + algname + " F" + fid + " I" + iid + " " + dim + "D");
        
        try {
            // Create algorithm evaluator
            AlgorithmEvaluator algorithm = new AlgorithmEvaluator(algname);
            
            // Create logger
            String folderName = algname + "_F" + fid + "_I" + iid + "_" + dim + "D";
            IOHLogger logger = new IOHLogger(DATA_FOLDER + "/Baselines/", folderName, algname);
            
            // Create objective function
            ObjectiveFunction func = new SphereFunction(dim, fid, iid);
            
            // Run algorithm
            algorithm.run(func, 5, logger); // 5 repetitions
            
            // Close logger
            logger.close();
            
            BenchmarkBaselines.logger.info("Completed: " + algname + " F" + fid + " I" + iid + " " + dim + "D");
            
        } catch (Exception e) {
            logger.error("Error running experiment: " + config, e);
        }
    }
    
    /**
     * Configuration for a single experiment.
     */
    private static class ExperimentConfig {
        final String algorithmName;
        final int functionId;
        final int instanceId;
        final int dimension;
        
        ExperimentConfig(String algorithmName, int functionId, int instanceId, int dimension) {
            this.algorithmName = algorithmName;
            this.functionId = functionId;
            this.instanceId = instanceId;
            this.dimension = dimension;
        }
        
        @Override
        public String toString() {
            return String.format("ExperimentConfig{algorithm=%s, fid=%d, iid=%d, dim=%d}",
                    algorithmName, functionId, instanceId, dimension);
        }
    }
}
