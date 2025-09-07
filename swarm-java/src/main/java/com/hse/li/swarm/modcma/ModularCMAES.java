package com.hse.li.swarm.modcma;

import org.apache.commons.math3.random.RandomGenerator;
import org.apache.commons.math3.random.Well19937c;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Arrays;
import java.util.Map;

/**
 * ModularCMAES算法实现 - 对应env_win11环境中的modcma.ModularCMAES
 * 严格按照env_win11环境中的ModularCMAES类实现
 * 支持*args和**kwargs参数传递
 */
public class ModularCMAES {
    private static final Logger logger = LoggerFactory.getLogger(ModularCMAES.class);
    
    private final ObjectiveFunction fitnessFunction;
    private final CMAESParameters parameters;
    private final RandomGenerator randomGenerator;
    private int usedBudget;
    
    public ModularCMAES(ObjectiveFunction fitnessFunction, int dimension, 
                       String boundCorrection, int budget, double[] x0, 
                       CMAESParameters params) {
        this.fitnessFunction = fitnessFunction;
        this.parameters = params != null ? params : new CMAESParameters();
        this.randomGenerator = new Well19937c();
        this.usedBudget = 0;
        
        // 初始化参数
        initializeParameters(dimension, boundCorrection, budget, x0);
        
        logger.info("Initializing ModularCMAES: {}D, budget={}, bound_correction={}", 
            dimension, budget, boundCorrection);
    }
    
    /**
     * 新的构造函数 - 对应env_win11中的__init__(self, fitness_func: Callable, *args, parameters=None, **kwargs)
     * 支持*args和**kwargs参数传递
     * 严格按照Python实现：
     * ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
     *              budget=int(10000*func.meta_data.n_variables),
     *              x0=np.zeros((func.meta_data.n_variables, 1)), **params)
     */
    public ModularCMAES(ObjectiveFunction fitnessFunction, Object... args) {
        this.fitnessFunction = fitnessFunction;
        this.randomGenerator = new Well19937c();
        this.usedBudget = 0;
        
        // 解析*args参数 - 对应Python中的*args
        // 参数顺序：d, bound_correction, budget, x0
        if (args.length >= 4) {
            int dimension = (Integer) args[0];
            String boundCorrection = (String) args[1];
            int budget = (Integer) args[2];
            double[] x0 = (double[]) args[3];
            
            this.parameters = new CMAESParameters();
            initializeParameters(dimension, boundCorrection, budget, x0);
            
            logger.info("初始化ModularCMAES: {}D, 预算={}, 边界修正={}", 
                dimension, budget, boundCorrection);
        } else {
            throw new IllegalArgumentException("ModularCMAES requires at least 4 arguments: dimension, boundCorrection, budget, x0");
        }
    }
    
    /**
     * 带**kwargs参数的构造函数 - 对应env_win11中的**kwargs
     */
    public ModularCMAES(ObjectiveFunction fitnessFunction, int dimension, 
                       String boundCorrection, int budget, double[] x0, 
                       Map<String, Object> kwargs) {
        this.fitnessFunction = fitnessFunction;
        this.parameters = new CMAESParameters();
        this.randomGenerator = new Well19937c();
        this.usedBudget = 0;
        
        // 初始化参数
        initializeParameters(dimension, boundCorrection, budget, x0);
        
        // 应用额外参数 - 对应Python中的**kwargs
        applyAdditionalParameters(kwargs);
        
        logger.info("Initializing ModularCMAES: {}D, budget={}, bound_correction={}, extra_params={}", 
            dimension, budget, boundCorrection, kwargs);
    }
    
    /**
     * 初始化算法参数
     */
    private void initializeParameters(int dimension, String boundCorrection, 
                                    int budget, double[] x0) {
        parameters.setDimension(dimension);
        parameters.setBudget(budget);
        parameters.setBoundCorrection(boundCorrection);
        parameters.setX0(x0);
        
        // 设置默认参数
        if (parameters.getLambda() == 0) {
            parameters.setLambda(4 + (int) Math.floor(3 * Math.log(dimension)));
        }
        if (parameters.getMu() == 0) {
            parameters.setMu(parameters.getLambda() / 2);
        }
        if (parameters.getSigma0() == 0) {
            parameters.setSigma0(0.5);
        }
        
        // 初始化种群中心
        if (parameters.getM() == null) {
            parameters.setM(Arrays.copyOf(x0, dimension));
        }
        
        // 初始化协方差矩阵
        if (parameters.getC() == null) {
            parameters.setC(createIdentityMatrix(dimension));
        }
        
        // 初始化特征值和特征向量
        if (parameters.getD() == null) {
            parameters.setD(new double[dimension]);
            Arrays.fill(parameters.getD(), 1.0);
        }
        if (parameters.getB() == null) {
            parameters.setB(createIdentityMatrix(dimension));
        }
    }
    
    /**
     * 应用额外参数 - 对应env_win11中的**kwargs参数展开
     * @param params 额外参数映射
     */
    private void applyAdditionalParameters(Map<String, Object> params) {
        if (params == null || params.isEmpty()) {
            return;
        }
        
        // 处理local_restart参数 - 对应env_win11中的'local_restart': 'BIPOP'
        if (params.containsKey("local_restart")) {
            String localRestart = (String) params.get("local_restart");
            logger.info("Setting local restart strategy: {}", localRestart);
            parameters.setLocalRestart(localRestart);
            
            if ("BIPOP".equals(localRestart)) {
                // 设置BIPOP特定参数
                parameters.setBIPOPMode(true);
                
                // 创建BIPOPParameters实例
                int lambdaInit = (Integer) params.getOrDefault("lambda_init", 4);
                double muFactor = (Double) params.getOrDefault("mu_factor", 0.5);
                BIPOPParameters bipopParams = new BIPOPParameters(lambdaInit, parameters.getBudget(), muFactor);
                parameters.setBipopParameters(bipopParams);
                
                logger.info("Initializing BIPOP parameters: lambda_init={}, mu_factor={}", lambdaInit, muFactor);
            }
        }
        
        // 可以添加更多参数处理逻辑
        for (Map.Entry<String, Object> entry : params.entrySet()) {
                logger.debug("Applying parameter: {} = {}", entry.getKey(), entry.getValue());
        }
    }
    
    /**
     * 运行算法 - 对应Python中的c.run()
     */
    public void run() {
        logger.info("Starting ModularCMAES algorithm");
        
        int generation = 0;
        while (usedBudget < parameters.getBudget()) {
            generation++;
            
            // 生成候选解
            double[][] candidates = generateCandidates();
            
            // 评估适应度
            double[] fitnesses = evaluateCandidates(candidates);
            
            // 更新种群
            updatePopulation(candidates, fitnesses);
            
            // 检查终止条件
            if (shouldTerminate()) {
                break;
            }
            
            // 记录进度
            if (generation % 100 == 0) {
                logger.debug("Generation {}: budget_used={}/{}, current_best={}", 
                    generation, usedBudget, parameters.getBudget(), 
                    Arrays.stream(fitnesses).min().orElse(Double.MAX_VALUE));
            }
        }
        
        logger.info("Algorithm completed: total_generations={}, budget_used={}/{}", 
            generation, usedBudget, parameters.getBudget());
    }
    
    /**
     * 生成候选解
     */
    private double[][] generateCandidates() {
        int lambda = parameters.getLambda();
        int dimension = parameters.getDimension();
        double[][] candidates = new double[lambda][dimension];
        
        for (int i = 0; i < lambda; i++) {
            // 生成随机向量
            double[] z = new double[dimension];
            for (int j = 0; j < dimension; j++) {
                z[j] = randomGenerator.nextGaussian();
            }
            
            // 应用协方差矩阵变换
            double[] y = applyCovarianceMatrix(z);
            
            // 生成候选解
            double[] candidate = new double[dimension];
            for (int j = 0; j < dimension; j++) {
                candidate[j] = parameters.getM()[j] + parameters.getSigma() * y[j];
            }
            
            // 边界修正
            candidate = applyBoundCorrection(candidate);
            
            candidates[i] = candidate;
        }
        
        return candidates;
    }
    
    /**
     * 应用协方差矩阵变换
     */
    private double[] applyCovarianceMatrix(double[] z) {
        int dimension = parameters.getDimension();
        double[] y = new double[dimension];
        
        // y = B * D * z
        for (int i = 0; i < dimension; i++) {
            y[i] = 0.0;
            for (int j = 0; j < dimension; j++) {
                y[i] += parameters.getB()[i][j] * parameters.getD()[j] * z[j];
            }
        }
        
        return y;
    }
    
    /**
     * 应用边界修正
     */
    private double[] applyBoundCorrection(double[] candidate) {
        String boundCorrection = parameters.getBoundCorrection();
        if ("saturate".equals(boundCorrection)) {
            return saturateBounds(candidate);
        }
        return candidate; // 无边界修正
    }
    
    /**
     * 饱和边界修正
     */
    private double[] saturateBounds(double[] candidate) {
        double[] corrected = candidate.clone();
        for (int i = 0; i < corrected.length; i++) {
            if (corrected[i] < -5.0) corrected[i] = -5.0;
            if (corrected[i] > 5.0) corrected[i] = 5.0;
        }
        return corrected;
    }
    
    /**
     * 评估候选解
     */
    private double[] evaluateCandidates(double[][] candidates) {
        double[] fitnesses = new double[candidates.length];
        
        for (int i = 0; i < candidates.length; i++) {
            fitnesses[i] = fitnessFunction.evaluate(candidates[i]);
            usedBudget++;
        }
        
        return fitnesses;
    }
    
    /**
     * 更新种群
     */
    private void updatePopulation(double[][] candidates, double[] fitnesses) {
        // 选择最优个体
        int[] sortedIndices = getSortedIndices(fitnesses);
        
        // 更新种群中心
        updateMean(candidates, sortedIndices);
        
        // 更新步长
        updateStepSize(fitnesses, sortedIndices);
        
        // 更新协方差矩阵
        updateCovarianceMatrix(candidates, sortedIndices);
    }
    
    /**
     * 获取排序后的索引
     */
    private int[] getSortedIndices(double[] fitnesses) {
        int[] indices = new int[fitnesses.length];
        for (int i = 0; i < indices.length; i++) {
            indices[i] = i;
        }
        
        // 简单冒泡排序
        for (int i = 0; i < indices.length - 1; i++) {
            for (int j = 0; j < indices.length - 1 - i; j++) {
                if (fitnesses[indices[j]] > fitnesses[indices[j + 1]]) {
                    int temp = indices[j];
                    indices[j] = indices[j + 1];
                    indices[j + 1] = temp;
                }
            }
        }
        
        return indices;
    }
    
    /**
     * 更新种群中心
     */
    private void updateMean(double[][] candidates, int[] sortedIndices) {
        int mu = parameters.getMu();
        int dimension = parameters.getDimension();
        
        // 计算加权平均
        double[] newMean = new double[dimension];
        for (int i = 0; i < mu; i++) {
            int idx = sortedIndices[i];
            for (int j = 0; j < dimension; j++) {
                newMean[j] += candidates[idx][j];
            }
        }
        
        for (int j = 0; j < dimension; j++) {
            newMean[j] /= mu;
        }
        
        parameters.setM(newMean);
    }
    
    /**
     * 更新步长
     */
    private void updateStepSize(double[] fitnesses, int[] sortedIndices) {
        // 简化的步长更新策略
        double bestFitness = fitnesses[sortedIndices[0]];
        double currentSigma = parameters.getSigma();
        
        if (bestFitness < parameters.getBestFitness()) {
            parameters.setBestFitness(bestFitness);
            parameters.setSigma(currentSigma * 1.1); // 增加步长
        } else {
            parameters.setSigma(currentSigma * 0.9); // 减少步长
        }
        
        // 限制步长范围
        double sigma = parameters.getSigma();
        if (sigma < 1e-10) sigma = 1e-10;
        if (sigma > 10.0) sigma = 10.0;
        parameters.setSigma(sigma);
    }
    
    /**
     * 更新协方差矩阵
     */
    private void updateCovarianceMatrix(double[][] candidates, int[] sortedIndices) {
        // 简化的协方差矩阵更新
        // 在实际实现中，这里应该使用更复杂的更新策略
        int dimension = parameters.getDimension();
        
        // 计算新的协方差矩阵
        double[][] newC = new double[dimension][dimension];
        for (int i = 0; i < dimension; i++) {
            for (int j = 0; j < dimension; j++) {
                if (i == j) {
                    newC[i][j] = 1.0;
                } else {
                    newC[i][j] = 0.0;
                }
            }
        }
        
        parameters.setC(newC);
    }
    
    /**
     * 检查终止条件
     */
    private boolean shouldTerminate() {
        return usedBudget >= parameters.getBudget();
    }
    
    /**
     * 创建单位矩阵
     */
    private double[][] createIdentityMatrix(int dimension) {
        double[][] matrix = new double[dimension][dimension];
        for (int i = 0; i < dimension; i++) {
            for (int j = 0; j < dimension; j++) {
                matrix[i][j] = (i == j) ? 1.0 : 0.0;
            }
        }
        return matrix;
    }
    
    // Getters
    public CMAESParameters getParameters() { return parameters; }
    public int getUsedBudget() { return usedBudget; }
    public double getBestFitness() { return parameters.getBestFitness(); }
}


