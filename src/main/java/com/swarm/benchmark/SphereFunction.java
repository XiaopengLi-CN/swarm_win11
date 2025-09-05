package com.swarm.benchmark;

import java.util.Arrays;

/**
 * Implementation of the Sphere function (F1).
 * This is the simplest benchmark function: f(x) = sum(x_i^2)
 */
public class SphereFunction implements ObjectiveFunction {
    private final int dimension;
    private final int functionId;
    private final int instanceId;
    private final FunctionMetadata metadata;
    private final double[] lowerBounds;
    private final double[] upperBounds;
    
    public SphereFunction(int dimension, int functionId, int instanceId) {
        this.dimension = dimension;
        this.functionId = functionId;
        this.instanceId = instanceId;
        this.metadata = new FunctionMetadata(dimension, functionId, instanceId, "Sphere");
        
        // Sphere function typically has bounds [-5, 5] for each dimension
        this.lowerBounds = new double[dimension];
        this.upperBounds = new double[dimension];
        Arrays.fill(lowerBounds, -5.0);
        Arrays.fill(upperBounds, 5.0);
    }
    
    @Override
    public double evaluate(double[] solution) {
        if (solution.length != dimension) {
            throw new IllegalArgumentException("Solution dimension must be " + dimension);
        }
        
        // Sphere function: f(x) = sum(x_i^2)
        double sum = 0.0;
        for (double x : solution) {
            sum += x * x;
        }
        return sum;
    }
    
    @Override
    public int getDimension() {
        return dimension;
    }
    
    @Override
    public double[] getLowerBounds() {
        return lowerBounds.clone();
    }
    
    @Override
    public double[] getUpperBounds() {
        return upperBounds.clone();
    }
    
    @Override
    public int getFunctionId() {
        return functionId;
    }
    
    @Override
    public int getInstanceId() {
        return instanceId;
    }
    
    @Override
    public void reset() {
        // Sphere function is stateless, so no reset needed
    }
    
    @Override
    public FunctionMetadata getMetadata() {
        return metadata;
    }
}
