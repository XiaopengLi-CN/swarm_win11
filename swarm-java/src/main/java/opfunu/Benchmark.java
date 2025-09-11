package opfunu;

/**
 * Java版本的Benchmark类 - 完全复现Python的benchmark.py
 * 
 * Python参考: env_win11/Lib/site-packages/opfunu/benchmark.py
 * 
 * 类名、方法名、参数名完全一致
 */
public abstract class Benchmark {
    
    // 完全匹配Python的属性名
    protected String name;
    protected int ndim;
    protected double[][] bounds;
    protected double f_global;
    protected double[] x_global;
    
    // 函数特性 - 匹配Python的属性
    protected boolean continuous;
    protected boolean linear;
    protected boolean convex;
    protected boolean unimodal;
    protected boolean separable;
    protected boolean differentiable;
    protected boolean scalable;
    protected boolean randomized_term;
    protected boolean parametric;
    protected boolean shifted;
    protected boolean rotated;
    
    // 统计信息
    protected int n_fe; // 函数评估次数
    
    /**
     * 构造函数 - 完全匹配Python的__init__方法
     * 
     * @param name Function name
     * @param ndim Number of dimensions
     * @param bounds Bounds of the function
     */
    protected Benchmark(String name, int ndim, double[][] bounds) {
        this.name = name;
        this.ndim = ndim;
        this.bounds = bounds;
        this.f_global = 0.0;
        this.x_global = new double[ndim];
        
        // 初始化函数特性
        this.continuous = true;
        this.linear = false;
        this.convex = false;
        this.unimodal = false;
        this.separable = false;
        this.differentiable = true;
        this.scalable = true;
        this.randomized_term = false;
        this.parametric = false;
        this.shifted = false;
        this.rotated = false;
        
        // 初始化统计
        this.n_fe = 0;
    }
    
    /**
     * 评估函数 - 完全匹配Python的evaluate方法
     * 
     * @param x Input vector
     * @return Function value
     */
    public abstract double evaluate(double[] x);
    
    /**
     * 获取函数名称 - 匹配Python的get_name方法
     */
    public String get_name() {
        return this.name;
    }
    
    /**
     * 获取维度 - 匹配Python的get_ndim方法
     */
    public int get_ndim() {
        return this.ndim;
    }
    
    /**
     * 获取边界 - 匹配Python的get_bounds方法
     */
    public double[][] get_bounds() {
        return this.bounds;
    }
    
    /**
     * 获取全局最优值 - 匹配Python的get_f_global方法
     */
    public double get_f_global() {
        return this.f_global;
    }
    
    /**
     * 获取全局最优点 - 匹配Python的get_x_global方法
     */
    public double[] get_x_global() {
        return this.x_global;
    }
    
    /**
     * 获取函数评估次数 - 匹配Python的get_n_fe方法
     */
    public int get_n_fe() {
        return this.n_fe;
    }
    
    /**
     * 重置函数评估次数 - 匹配Python的reset_n_fe方法
     */
    public void reset_n_fe() {
        this.n_fe = 0;
    }
    
    /**
     * 检查点是否在边界内 - 匹配Python的check_bounds方法
     */
    public boolean check_bounds(double[] x) {
        for (int i = 0; i < ndim; i++) {
            if (x[i] < bounds[i][0] || x[i] > bounds[i][1]) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * 获取函数信息 - 匹配Python的get_info方法
     */
    public String get_info() {
        return String.format("Function: %s, Dimension: %d, Bounds: [%.2f, %.2f], Global Optimum: %.6f", 
                           name, ndim, bounds[0][0], bounds[0][1], f_global);
    }
    
    /**
     * toString方法 - 匹配Python的__str__方法
     */
    @Override
    public String toString() {
        return String.format("Benchmark{name='%s', ndim=%d, f_global=%.6f}", 
                           name, ndim, f_global);
    }
}
