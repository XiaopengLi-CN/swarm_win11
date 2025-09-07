package com.hse.li.swarm.benchmark;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.hse.li.swarm.ioh.BBOBProblem;
import com.hse.li.swarm.modcma.ModCMAConfig;
import com.hse.li.swarm.modcma.ModularCMAES;

import java.util.Map;

/**
 * Algorithm evaluator - corresponds to Algorithm_Evaluator class in Python
 * Strictly follows Python implementation:
 * class Algorithm_Evaluator():
 *     def __init__(self, optimizer):
 *         self.alg = optimizer
 *     def __call__(self, func, n_reps):
 *         for seed in range(n_reps):
 *             np.random.seed(int(seed))
 *             print(self.alg)
 *             params = modcma_params[self.alg[7:]]
 *             c = ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
 *                          budget=int(10000*func.meta_data.n_variables),
 *                          x0=np.zeros((func.meta_data.n_variables, 1)), **params)
 *             c.run()
 *             func.reset()
 */
public class AlgorithmEvaluator {
    private static final Logger logger = LoggerFactory.getLogger(AlgorithmEvaluator.class);
    
    private final String algorithmName; // Corresponds to self.alg in Python
    
    public AlgorithmEvaluator(String algorithmName) {
        this.algorithmName = algorithmName;
        logger.info("Initializing algorithm evaluator: {}", algorithmName);
    }
    
    /**
     * Execute algorithm evaluation - corresponds to __call__ method in Python
     * Strictly follows Python implementation:
     * def __call__(self, func, n_reps):
     *     for seed in range(n_reps):
     *         np.random.seed(int(seed))
     *         print(self.alg)
     *         params = modcma_params[self.alg[7:]]
     *         c = ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
     *                      budget=int(10000*func.meta_data.n_variables),
     *                      x0=np.zeros((func.meta_data.n_variables, 1)), **params)
     *         c.run()
     *         func.reset()
     * 
     * @param problem BBOB problem instance
     * @param nReps Number of repetitions
     */
    public void evaluate(BBOBProblem problem, int nReps) {
        logger.info("Starting algorithm evaluation: {} on problem F{}", algorithmName, problem.getFunctionId());
        
        for (int seed = 0; seed < nReps; seed++) {
            logger.info("Executing run {} of {}, seed: {}", seed + 1, nReps, seed);
            
            try {
                // Set random seed - corresponds to np.random.seed(int(seed)) in Python
                problem.setRandomSeed(seed);
                
                // Output algorithm name - corresponds to print(self.alg) in Python
                logger.info("Algorithm name: {}", algorithmName);
                
                // Get algorithm parameters - corresponds to params = modcma_params[self.alg[7:]] in Python
                Map<String, Object> algorithmParams = ModCMAConfig.getAlgorithmParams(algorithmName);
                
                // Create ModularCMAES instance - strictly follows Python parameter order
                // ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
                //              budget=int(10000*func.meta_data.n_variables),
                //              x0=np.zeros((func.meta_data.n_variables, 1)), **params)
                ModularCMAES cmaes = new ModularCMAES(
                    problem,                                    // func
                    problem.getMetaData().getNVariables(),       // d=func.meta_data.n_variables
                    "saturate",                                 // bound_correction='saturate'
                    (int) (10000 * problem.getMetaData().getNVariables()), // budget=int(10000*func.meta_data.n_variables)
                    createZeroInitialSolution(problem.getMetaData().getNVariables()), // x0=np.zeros((func.meta_data.n_variables, 1))
                    algorithmParams                             // **params
                );
                
                // Run algorithm - corresponds to c.run() in Python
                cmaes.run();
                
                logger.info("Run {} completed, best fitness: {}", seed + 1, cmaes.getBestFitness());
                
                // Reset problem state - corresponds to func.reset() in Python
                problem.reset();
                
            } catch (Exception e) {
                logger.error("Run {} failed: {}", seed + 1, e.getMessage(), e);
            }
        }
        
        logger.info("Algorithm evaluation completed: {}", algorithmName);
    }
    
    /**
     * Create zero initial solution - corresponds to np.zeros((func.meta_data.n_variables, 1)) in Python
     * @param nVariables Number of variables
     * @return Zero initial solution array
     */
    private double[] createZeroInitialSolution(int nVariables) {
        return new double[nVariables]; // One-dimensional array in Java corresponds to (n_variables, 1) in Python
    }
    
    public String getAlgorithmName() {
        return algorithmName;
    }
}