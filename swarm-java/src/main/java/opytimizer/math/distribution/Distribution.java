package opytimizer.math.distribution;

import java.util.Random;
import java.lang.Math;

/**
 * Java版本的Distribution类 - 完全复现Python的distribution.py
 * 
 * Python参考: env_win11/Lib/site-packages/opytimizer/math/distribution.py
 * 
 * 类名、方法名、参数名完全一致
 */
public class Distribution {
    
    private static final Random random = new Random();
    
    /**
     * 生成伯努利分布 - 完全匹配Python的generate_bernoulli_distribution方法
     * 
     * @param prob Probability of distribution
     * @param size Size of array
     * @return Bernoulli distribution n-dimensional array
     */
    public static double[] generate_bernoulli_distribution(double prob, int size) {
        // Creates the bernoulli array - 完全匹配Python的逻辑
        double[] bernoulli_array = new double[size];
        
        // Generates a random number - 完全匹配Python的r.generate_uniform_random_number
        double[] r1 = opytimizer.math.random.Random.generate_uniform_random_number(0.0, 1.0, size);
        
        // Masks the array based on input probability - 完全匹配Python的逻辑
        for (int i = 0; i < size; i++) {
            if (r1[i] < prob) {
                bernoulli_array[i] = 1.0;
            } else {
                bernoulli_array[i] = 0.0;
            }
        }
        
        return bernoulli_array;
    }
    
    /**
     * 生成选择分布 - 完全匹配Python的generate_choice_distribution方法
     * 
     * @param n Amount of values to be picked from
     * @param probs Array of probabilities
     * @param size Size of array
     * @return Choice distribution array
     */
    public static int[] generate_choice_distribution(int n, double[] probs, int size) {
        // Performs the random choice based on input probabilities - 完全匹配Python的逻辑
        int[] choice_array = new int[size];
        
        for (int i = 0; i < size; i++) {
            double rand = random.nextDouble();
            double cumulative = 0.0;
            
            for (int j = 0; j < n; j++) {
                cumulative += (probs != null ? probs[j] : 1.0 / n);
                if (rand <= cumulative) {
                    choice_array[i] = j;
                    break;
                }
            }
        }
        
        return choice_array;
    }
    
    /**
     * 生成Lévy分布 - 完全匹配Python的generate_levy_distribution方法
     * 
     * @param beta Skewness parameter
     * @param size Size of array
     * @return Lévy distribution n-dimensional array
     */
    public static double[] generate_levy_distribution(double beta, int size) {
        // Calculates the equation's numerator and denominator - 完全匹配Python的逻辑
        double num = gamma(1 + beta) * Math.sin(Math.PI * beta / 2);
        double den = gamma((1 + beta) / 2) * beta * Math.pow(2, (beta - 1) / 2);
        
        // Calculates `sigma` - 完全匹配Python的逻辑
        double sigma = Math.pow(num / den, 1 / beta);
        
        // Calculates 'u' and `v` distributions - 完全匹配Python的逻辑
        double[] u = opytimizer.math.random.Random.generate_gaussian_random_number(0.0, sigma * sigma, size);
        double[] v = opytimizer.math.random.Random.generate_gaussian_random_number(0.0, 1.0, size);
        
        // Calculates the Lévy distribution - 完全匹配Python的逻辑
        double[] levy_array = new double[size];
        for (int i = 0; i < size; i++) {
            levy_array[i] = u[i] / Math.abs(v[i]);
            levy_array[i] = Math.pow(levy_array[i], 1 / beta);
        }
        
        return levy_array;
    }
    
    /**
     * Gamma函数 - 简化实现
     */
    private static double gamma(double x) {
        // 简化实现，使用Stirling近似
        if (x < 0.5) {
            return Math.PI / (Math.sin(Math.PI * x) * gamma(1 - x));
        }
        x -= 1;
        double a = 0.99999999999980993;
        double[] p = {676.5203681218851, -1259.1392167224028, 771.32342877765313,
                     -176.61502916214059, 12.507343278686905, -0.13857109526572012,
                     9.9843695780195716e-6, 1.5056327351493116e-7};
        
        double t = x + 7.5;
        double sum = a;
        for (int i = 0; i < p.length; i++) {
            sum += p[i] / (x + i + 1);
        }
        
        return Math.sqrt(2 * Math.PI) * Math.pow(t, x + 0.5) * Math.exp(-t) * sum;
    }
}
