package com.swarm.algorithms;

/**
 * Result of an optimization run.
 */
public class OptimizationResult {
    private final double[] bestSolution;
    private final double bestFitness;
    private final int evaluationsUsed;
    private final long computationTime;
    private final String algorithmName;
    
    public OptimizationResult(double[] bestSolution, double bestFitness, 
                            int evaluationsUsed, long computationTime, String algorithmName) {
        this.bestSolution = bestSolution.clone();
        this.bestFitness = bestFitness;
        this.evaluationsUsed = evaluationsUsed;
        this.computationTime = computationTime;
        this.algorithmName = algorithmName;
    }
    
    public double[] getBestSolution() {
        return bestSolution.clone();
    }
    
    public double getBestFitness() {
        return bestFitness;
    }
    
    public int getEvaluationsUsed() {
        return evaluationsUsed;
    }
    
    public long getComputationTime() {
        return computationTime;
    }
    
    public String getAlgorithmName() {
        return algorithmName;
    }
    
    @Override
    public String toString() {
        return String.format("OptimizationResult{algorithm=%s, fitness=%.6f, evaluations=%d, time=%dms}",
                algorithmName, bestFitness, evaluationsUsed, computationTime);
    }
}
