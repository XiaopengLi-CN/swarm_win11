import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
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

    fids = range(1,2)  # 只测试F1 (Sphere)
    algnames = ["modcma_bipop"]
    iids = range(1,11)  # 测试I1-I10，共10个实例
    
    dims = [10]  # 只测试10维度
    
    args = product(algnames, fids, iids, dims)

    runParallelFunction(run_optimizer, args)
