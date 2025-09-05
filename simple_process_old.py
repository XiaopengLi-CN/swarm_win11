import pandas as pd
import numpy as np
import glob
import os

DATA_FOLDER = "Data"
CSV_FOLDER = "CSV_Results"

budget_factors = [10, 50, 100, 500, 1000, 5000, 10000]

def process_file(fname):
    """简化的文件处理函数"""
    print(f"Processing: {fname}")
    try:
        # 提取维度信息
        dim = int(fname.split('_')[-1][3:-4])
        
        # 读取数据
        with open(fname, 'r') as f:
            content = f.read()
        
        # 分割不同的运行
        runs = content.strip().split('evaluations raw_y')[1:]  # 跳过第一个空的部分
        
        all_data = []
        for run_idx, run_data in enumerate(runs):
            if not run_data.strip():
                continue
                
            # 解析运行数据
            lines = run_data.strip().split('\n')
            run_items = []
            
            for line in lines:
                if line.strip() and ' ' in line:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        try:
                            eval_count = int(parts[0])
                            raw_y = float(parts[1])
                            run_items.append([eval_count, raw_y])
                        except:
                            continue
            
            if run_items:
                # 为每个预算因子计算性能
                for budget_factor in budget_factors:
                    budget_eval = budget_factor * dim
                    
                    # 找到不超过预算的数据点
                    valid_items = [item for item in run_items if item[0] <= budget_eval]
                    
                    if valid_items:
                        min_y = min(item[1] for item in valid_items)
                        all_data.append({
                            'fname': fname,
                            'fx': min_y,
                            'run': run_idx + 1,
                            'budget_factor': budget_factor,
                            'budget': budget_eval
                        })
        
        if all_data:
            return pd.DataFrame(all_data)
        else:
            print(f"No valid data found in {fname}")
            return None
            
    except Exception as e:
        print(f"Error processing {fname}: {e}")
        return None

def parse_filename(base):
    """解析文件名中的信息"""
    parts = base.split('_')
    # 文件名格式: modcma_bipop_F1_I1_2D 或 CS_F1_I1_2D
    fid = int(parts[-3][1:])  # F1 -> 1
    iid = int(parts[-2][1:])  # I1 -> 1
    dim = int(parts[-1][:-1])  # 2D -> 2 (去掉D)
    return fid, iid, dim

def main():
    # 处理所有数据文件
    all_results = []
    
    # 处理Baselines数据
    baselines_files = glob.glob(f"{DATA_FOLDER}/Baselines/*/*/IOHprofiler_f*.dat")
    print(f"Found {len(baselines_files)} Baselines files")
    
    for fname in baselines_files:
        result = process_file(fname)
        if result is not None:
            # 添加算法信息
            base = fname.split('\\')[-3]  # 使用Windows路径分隔符
            algname = 'modcma_bipop'  # 我们知道这是BIPOP-CMA-ES
            
            fid, iid, dim = parse_filename(base)
            
            result['algname'] = algname
            result['fid'] = fid
            result['iid'] = iid
            result['dim'] = dim
            all_results.append(result)
    
    # 处理OPYTIMIZER数据
    optymizer_files = glob.glob(f"{DATA_FOLDER}/OPYTIMIZER/*/*/IOHprofiler_f*.dat")
    print(f"Found {len(optymizer_files)} OPYTIMIZER files")
    
    for fname in optymizer_files:
        result = process_file(fname)
        if result is not None:
            # 添加算法信息
            base = fname.split('\\')[-3]  # 使用Windows路径分隔符
            algname = base.split('_')[0]  # CS or DE
            
            fid, iid, dim = parse_filename(base)
            
            result['algname'] = algname
            result['fid'] = fid
            result['iid'] = iid
            result['dim'] = dim
            all_results.append(result)
    
    # 合并所有结果
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        
        # 保存结果
        output_file = f"{CSV_FOLDER}/FBUDGET_all.csv"
        final_df.to_csv(output_file, index=False)
        print(f"Saved results to {output_file}")
        print(f"Total rows: {len(final_df)}")
        print(f"Algorithms: {final_df['algname'].unique()}")
        print(f"Functions: {final_df['fid'].unique()}")
        print(f"Instances: {final_df['iid'].unique()}")
        print(f"Dimensions: {final_df['dim'].unique()}")
    else:
        print("No data processed successfully")

if __name__ == '__main__':
    main()
