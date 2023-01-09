from scipy.spatial import distance
import numpy as np
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import sys


def getIds(pop):
    return set(meta[meta.Population==pop].index).intersection(dm.columns.values)    

def popdistance(pop1, pop2):
    return dm.loc[getIds(pop1), getIds(pop2)].to_numpy().mean()

def fixId(id):
    if '3577STDY' in id: return id.split('_')[-1]
    return id
yemenMeta = pd.read_csv('Metadata/yemenRegions.csv', index_col='Id')
yemenMeta.columns = ['Population']

if sys.argv[-1] in ['1240K', 'HO']:
    reichset = sys.argv[-1]
else:
    reichset = ['1240K', 'HO'][1]
print('reich', reichset)
if reichset=='1240K':
    columns2keep = [1,9, 12, 14]
elif reichset=='HO':
    columns2keep = [1, 5, 7, 9]
columnNames = 'Id Date Group_Label Country'.split()

reich=pd.read_csv(f"Reich/v44.3_{reichset}_public.anno", sep='\t')
reich = reich.iloc[:,columns2keep]
reich.columns = columnNames
## QC
reich = reich[~reich.Group_Label.str.startswith("Ignore_")]
reich = reich[~reich.Group_Label.str.endswith("_outlier")]
reich = reich[['Id', 'Group_Label']].set_index('Id')
reich.columns = ['Population'] 
meta = pd.concat([yemenMeta, reich])

## 1-IBS distance matrix, calculated with plink
## plink --bfile yemen_clean_hgdp2 --distance square gz '1-ibs' --out yemen_clean_hgdp2

## reading plink's squared Distance Matrix
datafile = f"yemen_clean_reich{reichset}"
ids = pd.read_csv(f'{datafile}.mdist.id', header=None, sep='\t')
dm = pd.read_csv(f'{datafile}.mdist.gz', header=None, sep='\t')
fids = [fixId(i) for i in ids[1]]
dm.index = fids
dm.columns = fids

pops = sorted(Counter(meta.Population))

## Debug stuff, 2b del
for pop in pops:
    if len(getIds(pop)) < 3:
        print (pop, " samples???")

print("starting DM calculation")
D = np.zeros((len(pops),len(pops)))
for i1 in range(len(pops)):
    for i2 in range(i1+1, len(pops)):
        D[i1,i2] = popdistance(pops[i1], pops[i2])
D += D.T
D1 = pd.DataFrame(D, index=pops, columns=pops)
D1.to_csv(f'distanceMatrix_{len(pops)}_{reichset}_ibs.csv')        
       
