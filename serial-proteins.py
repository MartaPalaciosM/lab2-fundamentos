import pandas as pd 
from time import time
import matplotlib.pyplot as plt 

pattern=input('Introduce the pattern to search: ')
pattern = pattern.upper()

start_time = time()

mydata= pd.read_csv('proteins.csv', delimiter= ',')
mydata['contains_pattern']= mydata['sequence'].str.contains(pattern)

ids_true = mydata[mydata['contains_pattern']==True].copy()
ids_true.loc[:, 'repetitions_pattern']= ids_true['sequence'].str.count(pattern)
ids_true = ids_true.sort_values(by = ['repetitions_pattern'], ascending=False)
ids_true['structureId'] = ids_true['structureId'].astype(str)
end_time = time()

## plot the barchar of the top 10 ids and the id and max occurrences of the protein ##
ids_true = ids_true.head(10)

print('Execution time: ', end_time-start_time, 'seconds')
if ids_true.empty: 
    print('Pattern not found')
else: 
    print('Maximum protein: ', ids_true.iloc[0, 0], ' and occurrences: ', ids_true.iloc[0,-1])

    plt.bar(ids_true['structureId'], ids_true['repetitions_pattern'])
    plt.xlabel("Proteins's ID")
    plt.ylabel("Occurrences")
    plt.title('Bar plot of Id vs Number of repeated patterns')
    plt.tight_layout()
    plt.show()
