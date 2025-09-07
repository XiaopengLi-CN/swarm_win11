package com.hse.li.swarm.modcma;

/**
 * BIPOP参数类 - 对应env_win11环境中的modcma.parameters.BIPOPParameters
 * 严格按照env_win11环境中的BIPOPParameters类实现
 */
public class BIPOPParameters {
    private int lambdaInit;
    private int budget;
    private double muFactor;
    private Integer lambdaLarge;
    private Integer budgetSmall;
    private Integer budgetLarge;
    private int usedBudget;
    
    public BIPOPParameters(int lambdaInit, int budget, double muFactor) {
        this.lambdaInit = lambdaInit;
        this.budget = budget;
        this.muFactor = muFactor;
        this.usedBudget = 0;
    }
    
    /**
     * 判断是否使用大种群 - 对应env_win11中的large属性
     */
    public boolean isLarge() {
        if (budgetLarge != null && budgetSmall != null) {
            return (budgetLarge >= budgetSmall) && budgetLarge > 0;
        }
        return false;
    }
    
    /**
     * 计算剩余预算 - 对应env_win11中的remaining_budget属性
     */
    public int getRemainingBudget() {
        return budget - usedBudget;
    }
    
    /**
     * 获取lambda值 - 对应env_win11中的lambda_属性
     */
    public int getLambda() {
        return isLarge() ? getLambdaLarge() : getLambdaSmall();
    }
    
    /**
     * 获取sigma值 - 对应env_win11中的sigma属性
     */
    public double getSigma() {
        if (isLarge()) {
            return 2.0;
        } else {
            return 2e-2 * Math.random();
        }
    }
    
    /**
     * 获取mu值 - 对应env_win11中的mu属性
     */
    public int getMu() {
        return (int) Math.floor(getLambda() * muFactor);
    }
    
    /**
     * 自适应参数 - 对应env_win11中的adapt()方法
     */
    public void adapt(int usedBudget) {
        int usedPreviousIteration = usedBudget - this.usedBudget;
        this.usedBudget += usedPreviousIteration;
        
        if (lambdaLarge == null) {
            lambdaLarge = lambdaInit * 2;
            budgetSmall = getRemainingBudget() / 2;
            budgetLarge = getRemainingBudget() - budgetSmall;
        } else if (isLarge()) {
            budgetLarge -= usedPreviousIteration;
            lambdaLarge *= 2;
        } else {
            budgetSmall -= usedPreviousIteration;
        }
    }
    
    // Getters and Setters
    public int getLambdaInit() { return lambdaInit; }
    public void setLambdaInit(int lambdaInit) { this.lambdaInit = lambdaInit; }
    
    public int getBudget() { return budget; }
    public void setBudget(int budget) { this.budget = budget; }
    
    public double getMuFactor() { return muFactor; }
    public void setMuFactor(double muFactor) { this.muFactor = muFactor; }
    
    public Integer getLambdaLarge() { return lambdaLarge; }
    public void setLambdaLarge(Integer lambdaLarge) { this.lambdaLarge = lambdaLarge; }
    
    public Integer getBudgetSmall() { return budgetSmall; }
    public void setBudgetSmall(Integer budgetSmall) { this.budgetSmall = budgetSmall; }
    
    public Integer getBudgetLarge() { return budgetLarge; }
    public void setBudgetLarge(Integer budgetLarge) { this.budgetLarge = budgetLarge; }
    
    public int getUsedBudget() { return usedBudget; }
    public void setUsedBudget(int usedBudget) { this.usedBudget = usedBudget; }
    
    private int getLambdaSmall() {
        return lambdaInit;
    }
}


