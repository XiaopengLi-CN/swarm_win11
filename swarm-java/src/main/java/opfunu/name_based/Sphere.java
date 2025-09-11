package opfunu.name_based;

import opfunu.Benchmark;

/**
 * Java版本的Sphere函数 - 完全复现Python的sphere.py
 * 
 * Python参考: env_win11/Lib/site-packages/opfunu/name_based/sphere.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Sphere extends Benchmark {
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param ndim Number of dimensions
     */
    public Sphere(int ndim) {
        super("Sphere", ndim, create_bounds(ndim));
        
        // 设置函数特性 - 匹配Python的属性
        this.continuous = true;
        this.linear = false;
        this.convex = true;
        this.unimodal = true;
        this.separable = true;
        this.differentiable = true;
        this.scalable = true;
        this.randomized_term = false;
        this.parametric = false;
        this.shifted = false;
        this.rotated = false;
        
        // 设置全局最优值 - 匹配Python的f_global
        this.f_global = 0.0;
        
        // 设置全局最优点 - 匹配Python的x_global
        this.x_global = new double[ndim];
        for (int i = 0; i < ndim; i++) {
            this.x_global[i] = 0.0;
        }
    }
    
    /**
     * 创建边界 - 匹配Python的bounds设置
     */
    private static double[][] create_bounds(int ndim) {
        double[][] bounds = new double[ndim][2];
        for (int i = 0; i < ndim; i++) {
            bounds[i][0] = -5.12;  // 下界
            bounds[i][1] = 5.12;   // 上界
        }
        return bounds;
    }
    
    /**
     * 评估函数 - 完全匹配Python的evaluate方法
     * 
     * @param x Input vector
     * @return Function value
     */
    @Override
    public double evaluate(double[] x) {
        // 增加函数评估次数
        this.n_fe++;
        
        // 检查边界
        if (!check_bounds(x)) {
            throw new IllegalArgumentException("Input vector is out of bounds");
        }
        
        // 计算Sphere函数值 - 完全匹配Python的实现
        double sum = 0.0;
        for (int i = 0; i < ndim; i++) {
            sum += x[i] * x[i];
        }
        
        return sum;
    }
    
    /**
     * 获取函数参数 - 匹配Python的get_paras方法
     */
    public String get_paras() {
        return String.format("Sphere function: f(x) = sum(x[i]^2) for i in [0, %d)", ndim);
    }
    
    /**
     * 获取函数特性 - 匹配Python的get_characteristics方法
     */
    public String get_characteristics() {
        return "Continuous, Convex, Unimodal, Separable, Differentiable, Scalable";
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Sphere{ndim=%d, f_global=%.6f, n_fe=%d}", 
                           ndim, f_global, n_fe);
    }
}
