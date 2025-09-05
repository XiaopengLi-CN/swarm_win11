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
from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.spaces import SearchSpace

from opytimizer.optimizers.swarm import CS
from opytimizer.optimizers.evolutionary import DE


import time

DATA_FOLDER = "Data"
MAX_THREADS = 32

def runParallelFunction(runFunction, arguments):

    

    arguments = list(arguments)
    p = Pool(min(MAX_THREADS, len(arguments)))
    results = p.map(runFunction, arguments)
    p.close()
    return results


class Algorithm_Evaluator():
    def __init__(self, optimizer):
        self.alg = optimizer

    def __call__(self, func, n_reps):
        def helper(x):
            return func(x.reshape(-1))
        space = SearchSpace(30, func.meta_data.n_variables, func.bounds.lb, func.bounds.ub)
        optimizer = eval(f"{self.alg}()")
        function = Function(helper)

        for seed in range(n_reps):
            np.random.seed(int(seed))
            
            Opytimizer(space, optimizer, function).start(n_iterations=int((func.meta_data.n_variables * 10000) / 30))
            func.reset()
        
def run_optimizer(temp):
    
    algname, fid, iid, dim = temp
    print(algname, fid, iid, dim)
    
    algorithm = Algorithm_Evaluator(algname)

    logger = ioh.logger.Analyzer(root=f"{DATA_FOLDER}/OPYTIMIZER/", folder_name=f"{algname}_F{fid}_I{iid}_{dim}D", algorithm_name=f"{algname}")

    func = ioh.get_problem(fid, dimension=dim, instance=iid)

    func.attach_logger(logger)
    
    algorithm(func, 5)
    
    logger.close()

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=RuntimeWarning) 
    warnings.filterwarnings("ignore", category=FutureWarning)

    fids = range(20,25)  # 只测试F1 (Sphere)
    algnames = ["CS", "DE"]
    iids = range(1,11)  # 测试I1-I10，共10个实例
    
    dims = [10]  # 只测试10维度
    
    args = product(algnames, fids, iids, dims)

    runParallelFunction(run_optimizer, args)
