package com.hse.li.swarm.modcma;

/**
 * CMA-ES参数类 - 对应env_win11环境中的modcma.parameters.Parameters
 * 严格按照env_win11环境中的Parameters类实现
 * 继承自AnnotatedStruct，包含完整的CMA-ES参数
 */
public class CMAESParameters {
    private int dimension;
    private int budget;
    private String boundCorrection;
    private double[] x0;
    private int lambda;
    private int mu;
    private double sigma0;
    private double sigma;
    private double[] m; // 种群中心
    private double[][] c; // 协方差矩阵
    private double[] d; // 特征值
    private double[][] b; // 特征向量
    private double bestFitness;
    private boolean bipopMode; // BIPOP模式标志
    private BIPOPParameters bipopParameters; // BIPOP参数
    private String localRestart; // 局部重启策略
    
    public CMAESParameters() {
        this.lambda = 0;
        this.mu = 0;
        this.sigma0 = 0.0;
        this.sigma = 0.5;
        this.bestFitness = Double.MAX_VALUE;
        this.bipopMode = false;
    }
    
    // Getters
    public int getDimension() { return dimension; }
    public int getBudget() { return budget; }
    public String getBoundCorrection() { return boundCorrection; }
    public double[] getX0() { return x0; }
    public int getLambda() { return lambda; }
    public int getMu() { return mu; }
    public double getSigma0() { return sigma0; }
    public double getSigma() { return sigma; }
    public double[] getM() { return m; }
    public double[][] getC() { return c; }
    public double[] getD() { return d; }
    public double[][] getB() { return b; }
    public double getBestFitness() { return bestFitness; }
    public boolean isBIPOPMode() { return bipopMode; }
    public BIPOPParameters getBipopParameters() { return bipopParameters; }
    public String getLocalRestart() { return localRestart; }
    
    // Setters
    public void setDimension(int dimension) { this.dimension = dimension; }
    public void setBudget(int budget) { this.budget = budget; }
    public void setBoundCorrection(String boundCorrection) { this.boundCorrection = boundCorrection; }
    public void setX0(double[] x0) { this.x0 = x0; }
    public void setLambda(int lambda) { this.lambda = lambda; }
    public void setMu(int mu) { this.mu = mu; }
    public void setSigma0(double sigma0) { this.sigma0 = sigma0; }
    public void setSigma(double sigma) { this.sigma = sigma; }
    public void setM(double[] m) { this.m = m; }
    public void setC(double[][] c) { this.c = c; }
    public void setD(double[] d) { this.d = d; }
    public void setB(double[][] b) { this.b = b; }
    public void setBestFitness(double bestFitness) { this.bestFitness = bestFitness; }
    public void setBIPOPMode(boolean bipopMode) { this.bipopMode = bipopMode; }
    public void setBipopParameters(BIPOPParameters bipopParameters) { this.bipopParameters = bipopParameters; }
    public void setLocalRestart(String localRestart) { this.localRestart = localRestart; }
}


