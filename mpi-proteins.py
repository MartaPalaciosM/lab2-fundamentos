from mpi4py import MPI
import pandas as pd 
from time import time
import matplotlib.pyplot as plt 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# we want the master process (rank 0) to take the input from the user and read the dataset
if rank == 0: 
    pattern=input('Introduce the pattern to search: ').upper()

else: 
    pattern = None

start_time= time()

#share with the rest of processes the pattern
pattern = comm.bcast(pattern, root=0)

if rank==0: 
    mydata= pd.read_csv('proteins.csv', delimiter= ',')
    block_size = len(mydata)// size
else: 
    mydata = None
    block_size = None

#share with the rest of processes the data
block_size = comm.bcast(block_size, root=0)
mydata = comm.bcast(mydata, root=0)

print(MPI.COMM_WORLD.Get_rank())
#distribute the block_data 
block_data = comm.scatter([mydata[i*block_size:(i+1)*block_size] for i in range (size)], root=0)

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
    print('Maximum protein: ', final_data.iloc[0, 0], ' and occurrences: ', final_data.iloc[0,-1])

    plt.bar(final_data['structureId'], final_data['repetitions pattern'])
    plt.xlabel("Proteins's ID")
    plt.ylabel("Occurrences")
    plt.title('Bar plot of Id vs Number of repeated patterns')
    plt.tight_layout()
    plt.show()
