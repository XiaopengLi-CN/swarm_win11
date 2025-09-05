package com.swarm.algorithms;

import com.swarm.benchmark.ObjectiveFunction;

/**
 * Interface for optimization algorithms.
 * All algorithms must implement this interface.
 */
public interface OptimizationAlgorithm {
    
    /**
     * Optimizes the given objective function.
     * 
     * @param function the objective function to optimize
     * @param maxEvaluations maximum number of function evaluations
     * @param logger the IOH logger to record evaluations
     * @return the best solution found
     */
    OptimizationResult optimize(ObjectiveFunction function, int maxEvaluations, com.swarm.benchmark.IOHLogger logger);
    
    /**
     * Gets the name of the algorithm.
     * 
     * @return algorithm name
     */
    String getName();
    
    /**
     * Gets the algorithm parameters.
     * 
     * @return map of parameter names to values
     */
    java.util.Map<String, Object> getParameters();
}
