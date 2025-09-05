package com.swarm.algorithms;

import com.swarm.benchmark.ObjectiveFunction;
import org.apache.commons.math3.linear.*;
import org.apache.commons.math3.distribution.NormalDistribution;
import org.apache.commons.math3.distribution.ChiSquaredDistribution;
import org.apache.commons.math3.random.RandomGenerator;
import org.apache.commons.math3.random.Well19937c;

import java.util.*;

/**
 * Implementation of BIPOP-CMA-ES algorithm.
 * This is a translation of the Python modcma library's ModularCMAES class.
 */
public class BIPOPCMAES implements OptimizationAlgorithm {
    
    // Algorithm parameters
    private final int lambda; // population size
    private final int mu; // number of parents
    private final double sigma0; // initial step size
    private final double[] lowerBounds;
    private final double[] upperBounds;
    private final String boundCorrection;
    private final String localRestart;
    
    // Internal state
    private double sigma; // current step size
    private double[] m; // mean vector
    private RealMatrix C; // covariance matrix
    private RealMatrix B; // eigenvectors
    private double[] D; // eigenvalues
    private double[] pc; // evolution path for rank-one update
    private double[] ps; // evolution path for step-size control
    private int evaluations;
    private RandomGenerator random;
    
    // Learning rates
    private final double cc;
    private final double cs;
    private final double c1;
    private final double cmu;
    
    public BIPOPCMAES(int dimension, double[] lowerBounds, double[] upperBounds) {
        this.lowerBounds = lowerBounds.clone();
        this.upperBounds = upperBounds.clone();
        this.boundCorrection = "saturate";
        this.localRestart = "BIPOP";
        
        // Default parameters
        this.lambda = 4 + (int) Math.floor(3 * Math.log(dimension));
        this.mu = lambda / 2;
        this.sigma0 = 0.5;
        
        // Learning rates
        this.cc = (4 + 1.0 / dimension) / (dimension + 4 + 2.0 / dimension);
        this.cs = (mu + 2) / (dimension + mu + 5);
        this.c1 = 2 / ((dimension + 1.3) * (dimension + 1.3) + mu);
        this.cmu = Math.min(1 - c1, 2 * (mu - 2 + 1.0 / mu) / ((dimension + 2) * (dimension + 2) + mu));
        
        // Initialize internal state
        this.sigma = sigma0;
        this.m = new double[dimension];
        this.C = MatrixUtils.createRealIdentityMatrix(dimension);
        this.B = MatrixUtils.createRealIdentityMatrix(dimension);
        this.D = new double[dimension];
        Arrays.fill(D, 1.0);
        this.pc = new double[dimension];
        this.ps = new double[dimension];
        this.evaluations = 0;
        this.random = new Well19937c();
    }
    
    @Override
    public OptimizationResult optimize(ObjectiveFunction function, int maxEvaluations, com.swarm.benchmark.IOHLogger logger) {
        long startTime = System.currentTimeMillis();
        
        // Initialize mean at center of bounds
        for (int i = 0; i < m.length; i++) {
            m[i] = (lowerBounds[i] + upperBounds[i]) / 2.0;
        }
        
        double bestFitness = Double.POSITIVE_INFINITY;
        double[] bestSolution = m.clone();
        
        while (evaluations < maxEvaluations) {
            // Generate population
            List<Individual> population = generatePopulation(function, logger);
            
            // Sort by fitness
            population.sort(Comparator.comparingDouble(Individual::getFitness));
            
            // Update best solution
            if (population.get(0).getFitness() < bestFitness) {
                bestFitness = population.get(0).getFitness();
                bestSolution = population.get(0).getSolution().clone();
            }
            
            // Update distribution parameters
            updateDistribution(population);
            
            // Check termination conditions
            if (bestFitness < 1e-8 || sigma < 1e-12) {
                break;
            }
        }
        
        long endTime = System.currentTimeMillis();
        return new OptimizationResult(bestSolution, bestFitness, evaluations, 
                                    endTime - startTime, "BIPOP-CMA-ES");
    }
    
    private List<Individual> generatePopulation(ObjectiveFunction function, com.swarm.benchmark.IOHLogger logger) {
        List<Individual> population = new ArrayList<>();
        
        for (int i = 0; i < lambda; i++) {
            // Generate random vector from normal distribution
            double[] z = new double[m.length];
            for (int j = 0; j < z.length; j++) {
                z[j] = random.nextGaussian();
            }
            
            // Transform to search space
            double[] y = B.operate(z);
            for (int j = 0; j < y.length; j++) {
                y[j] *= D[j];
            }
            
            // Create solution
            double[] solution = new double[m.length];
            for (int j = 0; j < solution.length; j++) {
                solution[j] = m[j] + sigma * y[j];
            }
            
            // Apply bound correction
            solution = correctBounds(solution);
            
            // Evaluate fitness
            double fitness = function.evaluate(solution);
            evaluations++;
            
            // Log evaluation
            logger.logEvaluation(solution, fitness, evaluations);
            
            population.add(new Individual(solution, fitness));
        }
        
        return population;
    }
    
    private void updateDistribution(List<Individual> population) {
        // Calculate weighted mean
        double[] newMean = new double[m.length];
        double[] weights = calculateWeights();
        
        for (int i = 0; i < mu; i++) {
            double[] solution = population.get(i).getSolution();
            for (int j = 0; j < m.length; j++) {
                newMean[j] += weights[i] * solution[j];
            }
        }
        
        // Update evolution paths
        double[] dm = new double[m.length];
        for (int i = 0; i < m.length; i++) {
            dm[i] = newMean[i] - m[i];
        }
        
        // Update step-size evolution path
        for (int i = 0; i < ps.length; i++) {
            ps[i] = (1 - cs) * ps[i] + Math.sqrt(cs * (2 - cs) * mu) * dm[i] / sigma;
        }
        
        // Update covariance evolution path
        for (int i = 0; i < pc.length; i++) {
            pc[i] = (1 - cc) * pc[i] + Math.sqrt(cc * (2 - cc) * mu) * dm[i] / sigma;
        }
        
        // Update mean
        m = newMean;
        
        // Update covariance matrix (simplified rank-one update)
        RealMatrix pcMatrix = MatrixUtils.createRealMatrix(m.length, 1);
        for (int i = 0; i < m.length; i++) {
            pcMatrix.setEntry(i, 0, pc[i]);
        }
        
        RealMatrix pcTranspose = pcMatrix.transpose();
        RealMatrix rankOneUpdate = pcMatrix.multiply(pcTranspose);
        
        C = C.scalarAdd(1 - c1 - cmu).add(rankOneUpdate.scalarMultiply(c1));
        
        // Update step size
        double psNorm = 0;
        for (double p : ps) {
            psNorm += p * p;
        }
        psNorm = Math.sqrt(psNorm);
        
        sigma *= Math.exp((cs / 1.0) * (psNorm / Math.sqrt(m.length) - 1));
    }
    
    private double[] calculateWeights() {
        double[] weights = new double[mu];
        for (int i = 0; i < mu; i++) {
            weights[i] = Math.log(lambda / 2.0 + 0.5) - Math.log(i + 1.0);
        }
        
        // Normalize weights
        double sum = 0;
        for (double w : weights) {
            sum += w;
        }
        for (int i = 0; i < weights.length; i++) {
            weights[i] /= sum;
        }
        
        return weights;
    }
    
    private double[] correctBounds(double[] solution) {
        if ("saturate".equals(boundCorrection)) {
            for (int i = 0; i < solution.length; i++) {
                solution[i] = Math.max(lowerBounds[i], Math.min(upperBounds[i], solution[i]));
            }
        }
        return solution;
    }
    
    @Override
    public String getName() {
        return "BIPOP-CMA-ES";
    }
    
    @Override
    public Map<String, Object> getParameters() {
        Map<String, Object> params = new HashMap<>();
        params.put("lambda", lambda);
        params.put("mu", mu);
        params.put("sigma0", sigma0);
        params.put("boundCorrection", boundCorrection);
        params.put("localRestart", localRestart);
        return params;
    }
    
    /**
     * Individual in the population.
     */
    private static class Individual {
        private final double[] solution;
        private final double fitness;
        
        public Individual(double[] solution, double fitness) {
            this.solution = solution.clone();
            this.fitness = fitness;
        }
        
        public double[] getSolution() {
            return solution.clone();
        }
        
        public double getFitness() {
            return fitness;
        }
    }
}
