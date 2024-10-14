from mpi4py import MPI
import pandas as pd 
from time import time
import matplotlib.pyplot as plt 
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def count_lines(file):
    with open(file, 'r') as f: 
        count = sum (1 for line in f)
    return count

#we want the master process (rank 0) to take the input from the user and read the dataset
if rank == 0: 
    pattern=input('Introduce the pattern to search: ')
    pattern = pattern.upper()
else: 
    pattern = None

start_time= time()

#share with the rest of processes the pattern
pattern = comm.bcast(pattern, root=0)
if rank==0: 
    #mydata= pd.read_csv('proteins.csv', delimiter= ',')
    num_lines = count_lines('proteins.csv')
    block_size = num_lines// size
    remainder = num_lines % size # in case the number of lines cant be divided evenly
else: 
    num_lines = None
    block_size = None
    remainder= 0

#share with the rest of processes the data
block_size = comm.bcast(block_size, root=0)
num_lines = comm.bcast(num_lines, root=0)

#find the lines each rank will need to read
start_line = rank*block_size
end_line = start_line+block_size

# ensure if lines where uneven, they are added to the las process 
if rank == size-1: 
    end_line += remainder

#read the corresponding block_data 
headers = pd.read_csv('proteins.csv', nrows=0).columns.tolist()
block_data = pd.read_csv('proteins.csv', skiprows=range(0, start_line), nrows= end_line-start_line, header = None, names = headers, dtype={0:str, 1:str})


#each process will look for the pattern in their corresponding block and count the repetitions
block_data['contains pattern'] = block_data['sequence'].str.contains(pattern)
ids_true = block_data[block_data['contains pattern']==True].copy()
ids_true.loc[:, 'repetitions pattern'] = ids_true['sequence'].str.count(pattern)

#gather back all the results 
join = comm.gather(ids_true, root=0)

if rank == 0: 
    final_data = pd.concat(join)
    final_data = final_data.sort_values(by= ['repetitions pattern'], ascending=False)
    final_data['structureId'] = final_data['structureId'].astype(str)

    final_data= final_data.head(10)
    end_time=time()
    print('Execution time: ', end_time-start_time, 'seconds')

    if final_data.empty: 
        print('Pattern not found')
    else:
        print('Maximum protein: ', final_data.iloc[0, 0], ' and occurrences: ', final_data.iloc[0,-1])
        plt.bar(final_data['structureId'], final_data['repetitions pattern'])
        plt.xlabel("Proteins's ID")
        plt.ylabel("Occurrences")
        plt.title('Bar plot of Id vs Number of repeated patterns')
        plt.tight_layout()
        plt.show()
