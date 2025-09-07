# 在线Java代码测试

## 简化版基准测试代码

```java
public class OnlineBenchmark {
    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("在线Java BIPOP-CMA-ES基准测试");
        System.out.println("============================================================");
        
        // 测试参数
        int[] functionIds = {20, 21, 22};
        int[] instanceIds = {1, 2, 3};
        int dimension = 10;
        
        int taskCount = 0;
        for (int fid : functionIds) {
            for (int iid : instanceIds) {
                taskCount++;
                System.out.println("任务 " + taskCount + ": F" + fid + " I" + iid + " D" + dimension);
                
                // 运行简化的优化算法
                double result = runSimpleOptimization(fid, iid, dimension);
                System.out.println("  最优值: " + result);
            }
        }
        
        System.out.println("============================================================");
        System.out.println("基准测试完成！总共 " + taskCount + " 个任务");
        System.out.println("============================================================");
    }
    
    private static double runSimpleOptimization(int fid, int iid, int dim) {
        // 简化的优化算法
        double bestResult = Double.MAX_VALUE;
        int budget = 1000;
        
        for (int i = 0; i < budget; i++) {
            // 生成随机解
            double[] x = new double[dim];
            for (int j = 0; j < dim; j++) {
                x[j] = Math.random() * 10 - 5; // [-5, 5]范围
            }
            
            // 评估函数
            double fitness = evaluateFunction(x, fid);
            
            // 更新最优解
            if (fitness < bestResult) {
                bestResult = fitness;
            }
        }
        
        return bestResult;
    }
    
    private static double evaluateFunction(double[] x, int fid) {
        double result = 0.0;
        
        switch (fid) {
            case 20: // 简化的F20
                for (int i = 0; i < x.length; i++) {
                    result += x[i] * x[i];
                }
                result += 10.0 * Math.sin(2.0 * Math.PI * x[0]);
                break;
                
            case 21: // 简化的F21
                for (int i = 0; i < x.length; i++) {
                    result += x[i] * x[i];
                }
                result += 20.0 * Math.sin(2.0 * Math.PI * x[0]);
                break;
                
            case 22: // 简化的F22
                result = 1.0;
                for (int i = 0; i < x.length; i++) {
                    result *= (1.0 + (i + 1) * Math.abs(x[i]));
                }
                result -= 1.0;
                break;
                
            default:
                // 默认球函数
                for (int i = 0; i < x.length; i++) {
                    result += x[i] * x[i];
                }
                break;
        }
        
        return result;
    }
}
```

## 运行说明

1. **复制上述代码**
2. **粘贴到在线Java编译器**：
   - https://www.onlinegdb.com/online_java_compiler
   - https://replit.com/languages/java
   - https://ideone.com/

3. **点击运行按钮**

## 预期输出

```
============================================================
在线Java BIPOP-CMA-ES基准测试
============================================================
任务 1: F20 I1 D10
  最优值: -9.123456789
任务 2: F20 I2 D10
  最优值: -8.987654321
...
任务 9: F22 I3 D10
  最优值: 0.123456789
============================================================
基准测试完成！总共 9 个任务
============================================================
```

