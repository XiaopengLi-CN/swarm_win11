# 群智能算法基准测试项目

## 项目简介
本项目实现了三种优化算法的基准测试：
- BIPOP-CMA-ES (来自modcma库)
- Cuckoo Search (CS) (来自opytimizer库)
- Differential Evolution (DE) (来自opytimizer库)

## 实验设置
- **函数**: F1 (Sphere)
- **实例**: 10个实例 (I1-I10)
- **维度**: 10D
- **运行次数**: 每个实例5次独立运行
- **评估预算**: B = 10000 * d
- **固定预算因子**: {10, 50, 100, 500, 1000, 5000, 10000}

## 项目结构
```
├── benchmark_baselines.py    # BIPOP-CMA-ES测试脚本
├── benchmark_optymizer.py    # CS和DE测试脚本
├── simple_process.py         # 数据处理脚本
├── dt_fb.py                  # 固定预算数据处理脚本
├── requirements.txt          # 项目依赖
└── README.md                 # 项目说明
```

## 环境设置
1. 创建虚拟环境：
   ```bash
   python -m venv env_new
   ```

2. 激活环境：
   ```bash
   env_new\Scripts\activate  # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行实验
1. 运行基准测试：
   ```bash
   python benchmark_baselines.py
   python benchmark_optymizer.py
   ```

2. 处理数据：
   ```bash
   python simple_process.py
   ```

3. 生成可视化：
   ```bash
   python dt_fb.py
   ```

## 依赖包
- ioh==0.3.14 (IOHexperimenter框架)
- opytimizer==3.1.2 (CS和DE算法)
- modcma==1.0.2 (BIPOP-CMA-ES算法)
- numpy, pandas, matplotlib等科学计算包
