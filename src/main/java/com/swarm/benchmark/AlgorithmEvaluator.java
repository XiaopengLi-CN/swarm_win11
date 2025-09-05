package com.swarm.benchmark;

import com.swarm.algorithms.BIPOPCMAES;
import com.swarm.algorithms.OptimizationAlgorithm;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.HashMap;
import java.util.Map;

/**
 * Evaluator for optimization algorithms.
 * This corresponds to the Algorithm_Evaluator class in the Python code.
 */
public class AlgorithmEvaluator {
    private static final Logger logger = LogManager.getLogger(AlgorithmEvaluator.class);
    
    private final String algorithmName;
    private final Map<String, Object> algorithmParams;
    
    public AlgorithmEvaluator(String algorithmName) {
        this.algorithmName = algorithmName;
        this.algorithmParams = new HashMap<>();
        
        // Set default parameters based on algorithm type
        if (algorithmName.startsWith("modcma_")) {
            String variant = algorithmName.substring(7); // Extract 'bipop' from 'modcma_bipop'
            if ("bipop".equals(variant)) {
                algorithmParams.put("localRestart", "BIPOP");
            }
        }
    }
    
    /**
     * Runs the algorithm on the given function for multiple repetitions.
     * 
     * @param function the objective function
     * @param nReps number of repetitions
     * @param logger the IOH logger to record evaluations
     */
    public void run(ObjectiveFunction function, int nReps, IOHLogger logger) {
        logger.info("Running algorithm: " + algorithmName);
        
        for (int seed = 0; seed < nReps; seed++) {
            logger.info("Starting run " + (seed + 1) + "/" + nReps + " with seed " + seed);
            
            // Create algorithm instance
            OptimizationAlgorithm algorithm = createAlgorithm(function, seed);
            
            // Calculate budget
            int budget = 10000 * function.getDimension();
            
            // Run optimization with logger
            var result = algorithm.optimize(function, budget, logger);
            
            logger.info("Run " + (seed + 1) + " completed: " + result);
            
            // Reset function for next run
            function.reset();
        }
    }
    
    /**
     * Creates an algorithm instance based on the algorithm name.
     */
    private OptimizationAlgorithm createAlgorithm(ObjectiveFunction function, int seed) {
        if (algorithmName.startsWith("modcma_")) {
            return new BIPOPCMAES(
                function.getDimension(),
                function.getLowerBounds(),
                function.getUpperBounds()
            );
        } else {
            throw new IllegalArgumentException("Unknown algorithm: " + algorithmName);
        }
    }
    
    /**
     * Gets the algorithm name.
     */
    public String getAlgorithmName() {
        return algorithmName;
    }
    
    /**
     * Gets the algorithm parameters.
     */
    public Map<String, Object> getAlgorithmParams() {
        return new HashMap<>(algorithmParams);
    }
}
