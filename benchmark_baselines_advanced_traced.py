import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# 导入高级代码执行跟踪器
from advanced_code_tracer import start_advanced_tracing, stop_advanced_tracing

# 开始高级跟踪 - 跟踪每一行代码的执行
tracer = start_advanced_tracing(
    log_file="benchmark_advanced_trace.log",
    trace_lines=True,      # 跟踪每行代码
    trace_calls=True,     # 跟踪函数调用
    trace_returns=True,   # 跟踪函数返回
    trace_exceptions=True # 跟踪异常
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

def runParallelFunction(runFunction, arguments):
    """并行运行函数"""
    arguments = list(arguments)
    p = Pool(min(MAX_THREADS, len(arguments)))
    results = p.map(runFunction, arguments)
    p.close()
    return results

modcma_params = { 'base' : {},
                  'bipop' : {
                  'local_restart' : 'BIPOP'
                  }
}

class Algorithm_Evaluator():
    """算法评估器"""
    
    def __init__(self, optimizer):
        self.alg = optimizer

    def __call__(self, func, n_reps):
        for seed in range(n_reps):
            np.random.seed(int(seed))
            
            # 只保留BIPOP-CMA-ES的处理逻辑
            print(self.alg)
            params = modcma_params[self.alg[7:]]  # 提取'bipop'参数
            c = ModularCMAES(func, d=func.meta_data.n_variables, bound_correction='saturate',
                         budget=int(10000*func.meta_data.n_variables),
                         x0=np.zeros((func.meta_data.n_variables, 1)), **params)
            c.run()
            
            func.reset()
        
def run_optimizer(temp):
    """运行优化器"""
    algname, fid, iid, dim = temp
    print(algname, fid, iid, dim)
    
    algorithm = Algorithm_Evaluator(algname)

    logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/Baselines/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")

    func = ioh.get_problem(fid, dimension=dim, instance=iid)
    func.attach_logger(logger)
    
    algorithm(func, 5)
    
    logger.close()

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=RuntimeWarning) 
    warnings.filterwarnings("ignore", category=FutureWarning)

    fids = range(20,25)  # 测试F20-F24
    algnames = ["modcma_bipop"]
    iids = range(1,11)  # 测试I1-I10，共10个实例
    
    dims = [10]  # 只测试10维度
    
    args = product(algnames, fids, iids, dims)

    runParallelFunction(run_optimizer, args)
    
    # 停止高级跟踪并保存摘要
    stop_advanced_tracing("benchmark_advanced_summary.json")
