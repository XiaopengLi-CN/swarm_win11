import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# 导入代码执行跟踪器
from code_execution_tracer import start_tracing, stop_tracing, trace_function, trace_class

# 开始跟踪
tracer = start_tracing(
    log_file="benchmark_execution_trace.log",
    detailed_mode=True,
    trace_imports=True
)

import ioh
from itertools import product
from functools import partial
from multiprocessing import Pool, cpu_count

import sys
import argparse
import warnings
import os

import pandas as pd

import numpy as np

import time
from copy import deepcopy

from modcma import ModularCMAES

DATA_FOLDER = "Data"
MAX_THREADS = 32

@trace_function
def runParallelFunction(runFunction, arguments):
    """并行运行函数"""
    tracer.log(f"开始并行执行，参数数量: {len(list(arguments))}")
    
    arguments = list(arguments)
    p = Pool(min(MAX_THREADS, len(arguments)))
    results = p.map(runFunction, arguments)
    p.close()
    
    tracer.log(f"并行执行完成，结果数量: {len(results)}")
    return results

modcma_params = { 'base' : {},
                  'bipop' : {
                  'local_restart' : 'BIPOP'
                  }
}

@trace_class
class Algorithm_Evaluator():
    """算法评估器 - 跟踪所有方法调用"""
    
    def __init__(self, optimizer):
        tracer.log(f"初始化算法评估器: {optimizer}")
        self.alg = optimizer

    @trace_function
    def __call__(self, func, n_reps):
        tracer.log(f"开始评估算法 {self.alg}，重复次数: {n_reps}")
        
        for seed in range(n_reps):
            tracer.log(f"开始第 {seed+1} 次重复，种子: {seed}")
            np.random.seed(int(seed))
            
            # 只保留BIPOP-CMA-ES的处理逻辑
            print(self.alg)
            params = modcma_params[self.alg[7:]]  # 提取'bipop'参数
            
            tracer.log(f"创建ModularCMAES实例，参数: {params}")
            c = ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
                         budget=int(10000*func.meta_data.n_variables),
                         x0=np.zeros((func.meta_data.n_variables, 1)), **params)
            
            tracer.log("开始运行优化算法")
            c.run()
            tracer.log("优化算法运行完成")
            
            func.reset()
            tracer.log(f"第 {seed+1} 次重复完成")

@trace_function
def run_optimizer(temp):
    """运行优化器 - 跟踪详细执行过程"""
    algname, fid, iid, dim = temp
    tracer.log(f"开始运行优化器: {algname}, F{fid}, I{iid}, {dim}D")
    print(algname, fid, iid, dim)
    
    algorithm = Algorithm_Evaluator(algname)

    tracer.log(f"创建IOH日志器: {DATA_FOLDER}/Baselines/{algname}_F{fid}_I{iid}_{dim}D")
    logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/Baselines/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")

    tracer.log(f"获取问题函数: F{fid}, 维度{dim}, 实例{iid}")
    func = ioh.get_problem(fid, dimension=dim, instance=iid)
    func.attach_logger(logger)
    
    tracer.log("开始算法评估")
    algorithm(func, 5)
    
    logger.close()
    tracer.log(f"优化器运行完成: {algname}, F{fid}, I{iid}, {dim}D")

if __name__ == '__main__':
    tracer.log("程序主入口开始")
    warnings.filterwarnings("ignore", category=RuntimeWarning) 
    warnings.filterwarnings("ignore", category=FutureWarning)

    fids = range(20,25)  # 测试F20-F24
    algnames = ["modcma_bipop"]
    iids = range(1,11)  # 测试I1-I10，共10个实例
    
    dims = [10]  # 只测试10维度
    
    tracer.log(f"测试配置: 函数{fids}, 算法{algnames}, 实例{iids}, 维度{dims}")
    
    args = product(algnames, fids, iids, dims)
    total_tasks = len(list(args))
    tracer.log(f"总任务数: {total_tasks}")

    # 重新生成参数（因为product是迭代器）
    args = product(algnames, fids, iids, dims)
    
    tracer.log("开始执行所有任务")
    runParallelFunction(run_optimizer, args)
    
    tracer.log("所有任务执行完成")
    
    # 停止跟踪并保存摘要
    stop_tracing("benchmark_execution_summary.json")
