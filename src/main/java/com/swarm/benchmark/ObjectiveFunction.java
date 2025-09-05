package com.swarm.benchmark;

/**
 * Interface for objective functions to be optimized.
 * This corresponds to the IOH problem interface.
 */
public interface ObjectiveFunction {
    
    /**
     * Evaluates the objective function at the given point.
     * 
     * @param solution the solution vector to evaluate
     * @return the fitness value
     */
    double evaluate(double[] solution);
    
    /**
     * Gets the dimension of the problem.
     * 
     * @return the number of variables
     */
    int getDimension();
    
    /**
     * Gets the lower bounds of the search space.
     * 
     * @return array of lower bounds
     */
    double[] getLowerBounds();
    
    /**
     * Gets the upper bounds of the search space.
     * 
     * @return array of upper bounds
     */
    double[] getUpperBounds();
    
    /**
     * Gets the function ID.
     * 
     * @return the function ID
     */
    int getFunctionId();
    
    /**
     * Gets the instance ID.
     * 
     * @return the instance ID
     */
    int getInstanceId();
    
    /**
     * Resets the function state.
     */
    void reset();
    
    /**
     * Gets metadata about the function.
     * 
     * @return function metadata
     */
    FunctionMetadata getMetadata();
}
