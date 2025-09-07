package com.hse.li.swarm.ioh;

import org.apache.commons.math3.util.FastMath;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.hse.li.swarm.ioh.IOHLogger;
import com.hse.li.swarm.modcma.ObjectiveFunction;

import java.util.Random;

/**
 * BBOB problem class - corresponds to problem object returned by ioh.get_problem() in Python
 * Implements F20-F24 functions with logging and reset functionality
 */
public class BBOBProblem implements ObjectiveFunction {
    private static final Logger logger = LoggerFactory.getLogger(BBOBProblem.class);
    
    private final int functionId;
    private final int instanceId;
    private final int dimension;
    private IOHProblemFactory.ProblemMetaData metaData;
    private IOHLogger attachedLogger;
    private Random random;
    private int evaluationCount;
    
    public BBOBProblem(int functionId, int instanceId, int dimension) {
        this.functionId = functionId;
        this.instanceId = instanceId;
        this.dimension = dimension;
        this.random = new Random();
        this.evaluationCount = 0;
        this.metaData = new IOHProblemFactory.ProblemMetaData(functionId, getFunctionName(functionId), dimension, instanceId);
        logger.info("Created BBOB problem: F{}, I{}, {}D", functionId, instanceId, dimension);
    }
    
    @Override
    public double evaluate(double[] x) {
        if (x.length != dimension) {
            throw new IllegalArgumentException("Input dimension mismatch: expected " + dimension + ", actual " + x.length);
        }
        
        evaluationCount++;
        double fitness = evaluateFunction(x);
        
        // Log to logger
        if (attachedLogger != null) {
            attachedLogger.logEvaluation(evaluationCount, fitness, x);
        }
        
        return fitness;
    }
    
    /**
     * Evaluate function - select corresponding BBOB function based on function ID
     */
    private double evaluateFunction(double[] x) {
        switch (functionId) {
            case 20: return schwefelFunction(x);
            case 21: return gallagher101Function(x);
            case 22: return gallagher21Function(x);
            case 23: return katsuuraFunction(x);
            case 24: return lunacekFunction(x);
            default: return simpleSphereFunction(x);
        }
    }
    
    /**
     * F20: Schwefel function
     */
    private double schwefelFunction(double[] x) {
        double sum = 0.0;
        for (double xi : x) {
            sum += xi * FastMath.sin(FastMath.sqrt(FastMath.abs(xi)));
        }
        return 418.9829 * x.length - sum;
    }
    
    /**
     * F21: Gallagher 101 function (simplified implementation)
     */
    private double gallagher101Function(double[] x) {
        double sum = 0.0;
        for (double xi : x) {
            sum += xi * xi;
        }
        return sum;
    }
    
    /**
     * F22: Gallagher 21 function (simplified implementation)
     */
    private double gallagher21Function(double[] x) {
        double sum = 0.0;
        for (double xi : x) {
            sum += xi * xi;
        }
        return sum;
    }
    
    /**
     * F23: Katsuura function (simplified implementation)
     */
    private double katsuuraFunction(double[] x) {
        double product = 1.0;
        for (int i = 0; i < x.length; i++) {
            double term = 1.0 + (i + 1) * FastMath.abs(x[i]);
            product *= term;
        }
        return product - 1.0;
    }
    
    /**
     * F24: Lunacek function (simplified implementation)
     */
    private double lunacekFunction(double[] x) {
        double sum = 0.0;
        for (double xi : x) {
            sum += xi * xi;
        }
        return sum;
    }
    
    /**
     * Simple sphere function as default implementation
     */
    private double simpleSphereFunction(double[] x) {
        double sum = 0.0;
        for (double xi : x) {
            sum += xi * xi;
        }
        return sum;
    }
    
    /**
     * Attach logger
     */
    public void attachLogger(IOHLogger logger) {
        this.attachedLogger = logger;
        // logger.info("Attached logger to BBOB problem");
    }
    
    /**
     * Reset problem state
     */
    @Override
    public void reset() {
        this.evaluationCount = 0;
        this.random = new Random();
        if (attachedLogger != null) {
            attachedLogger.reset();
        }
        logger.debug("Reset BBOB problem state");
    }
    
    /**
     * Set random seed
     */
    public void setRandomSeed(int seed) {
        this.random.setSeed(seed);
    }
    
    // Getters
    public int getFunctionId() { return functionId; }
    public int getInstanceId() { return instanceId; }
    public int getDimension() { return dimension; }
    public IOHProblemFactory.ProblemMetaData getMetaData() { return metaData; }
    public int getEvaluationCount() { return evaluationCount; }
    
    // Setters
    public void setMetaData(IOHProblemFactory.ProblemMetaData metaData) {
        this.metaData = metaData;
    }
    
    @Override
    public double getOptimalValue() {
        // BBOB functions typically have optimal value of 0
        return 0.0;
    }
    
    /**
     * Get function name
     * @param functionId Function ID
     * @return Function name
     */
    private String getFunctionName(int functionId) {
        return IOHProblemFactory.FUNCTION_NAMES.getOrDefault(functionId, "Unknown");
    }
}