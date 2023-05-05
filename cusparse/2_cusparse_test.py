#!/usr/bin/env python3

import argparse
import numpy as np
import os
from AIPowerMeter.deep_learning_power_measure.power_measure import experiment, parsers
from datetime import datetime
import warnings
import pandas as pd
import pickle

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(
    description='To illustrate how the consumption can be recorded for non python program, here is the measure the consumption of a small R script. R must be previously installed.'
    )
parser.add_argument('--output_folder',
                    help='directory to save the energy consumption records',
                    default='measure_power', type=str)

parser.add_argument('--repetitions', help='number of repetitions of the algorithm', default=200, type=int)

parser.add_argument('--name_exe', help='Executable name', default='cusparse_blocked_ell_spmm.o', type=str)

#parser.add_argument('--repetitions', help='number of repetitions of the algorithm', default=20, type=int)

args = parser.parse_args()

size_matrices = [
                # 512, 
                # 2048, 
                4096
                ]
number_blocks = 32
block_sizes = [16]
dim = 16
number_repetitions = vars(args)['repetitions']
NAME_EXE = vars(args)['name_exe']

# mean_time = {}
# mean_time_cublas = {}
# dict_results = {}

# driver = parsers.JsonParser(args.output_folder)
# #instantiating the experiment.
# exp = experiment.Experiment(driver)
# # starting the record, and wait two seconds between each energy consumption measurement
# p, q = exp.measure_yourself(period=2)



for size_matrix in size_matrices:
    # block_sizes = [2**i for i in range(5, int(np.log(size_matrix)/np.log(2))+1)]

    # print(block_sizes)
    # print('*************Beginning sparse multiplications with matrices of size****************'+str(size_matrix))
    # dict_block_sizes = {}
    # dict_block_sizes_cublas = {}
    for block_size in block_sizes:
        print('A_row/col: {}, B_col: {}, Blocksize: {}'.format(size_matrix, dim, block_size))
        
        A_ell_cols = block_size * number_blocks
        A_num_blocks = A_ell_cols * size_matrix /(block_size * block_size);
        total_params = A_num_blocks*block_size*block_size;
        total_elems = (size_matrix*size_matrix);
        sparsity = (total_elems - total_params) * 100 / total_elems
        print('Sparsity: '+str(sparsity))
        
        # os.system('./'+NAME_EXE+' '+str(size_matrix)+' '+str(size_matrix)+' '+str(block_size)+ ' '+str(number_blocks)+' '+str(number_repetitions)+' >/dev/null 2>&1') 
        os.system('./'+NAME_EXE+' '+str(size_matrix)+' '+str(dim)+' '+str(block_size)+ ' '+str(number_blocks)+' '+str(number_repetitions)) 

        #read the computation times from a text file generated by the C program.
        # with open('results.txt') as f:
        #     lines = f.readlines()

        # dict_block_sizes[block_size] =  float(lines[0].rstrip("\n"))
        # dict_block_sizes_cublas[block_size] =  float(lines[1].rstrip("\n"))   
    # mean_time[size_matrix] = dict_block_sizes
    # mean_time_cublas[size_matrix] = dict_block_sizes_cublas
# q.put(experiment.STOP_MESSAGE)

# driver = parsers.JsonParser(args.output_folder)
# exp_result = experiment.ExpResults(driver)
# exp_result.print()

#print(dict_results)
# print()
# print('Dict results with cuSparse:')
# print(mean_time)

# print()
# print('Dict results with cuBlas: ')
# print(mean_time_cublas)

# #print(pd.DataFrame(mean_time))

# #Saving the results in the directory
# with open('results_cusparse.pickle', 'wb') as handle:
#     pickle.dump(mean_time, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
# with open('results_cublas.pickle', 'wb') as handle:
#     pickle.dump(mean_time_cublas, handle, protocol=pickle.HIGHEST_PROTOCOL)