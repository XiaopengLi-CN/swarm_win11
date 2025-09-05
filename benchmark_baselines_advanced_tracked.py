#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_baselines_advanced_tracked.py - 使用高级跟踪器的基准测试脚本
"""

import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# 导入高级代码跟踪器
import sys
sys.path.append('.')
from advanced_code_tracker import tracker, track_function, auto_track_modules

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

# 自动跟踪模块
print("开始自动跟踪模块...")
auto_track_modules()
print("模块跟踪完成！")

@track_function
def runParallelFunction(runFunction, arguments):
    """运行并行函数"""
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

@track_function
class Algorithm_Evaluator():
    def __init__(self, optimizer):
        self.alg = optimizer

    @track_function
    def __call__(self, func, n_reps):
        """算法评估器调用"""
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
        
@track_function
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

    print("开始运行带跟踪的基准测试...")

    fids = range(1,2)  # 只测试F1 (Sphere)
    algnames = ["modcma_bipop"]
    iids = range(1,11)  # 测试I1-I10，共10个实例
    
    dims = [10]  # 只测试10维度
    
    args = product(algnames, fids, iids, dims)

    runParallelFunction(run_optimizer, args)
    
    # 完成跟踪报告
    tracker.finalize_report()
    print("高级代码跟踪完成！请查看 benchmark_baselines.txt 文件")
    print(f"总调用次数: {tracker.call_count}")
    print(f"跟踪的env_new文件数量: {len([f for f in tracker.tracked_files if 'env_new' in f])}")
