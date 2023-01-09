from scipy.spatial import distance
import numpy as np
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import sys

def popdistance(pop1, pop2):
    pop1DF = ddf[ddf.Population==pop1]
    pop2DF = ddf[ddf.Population==pop2]
    XA = pop1DF.iloc[:,2:12].to_numpy()
    XB = pop2DF.iloc[:,2:12].to_numpy()
    return distance.cdist(XA, XB, 'euclidean').mean()    

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


pca = pd.read_csv(f'FlashPCAResults/YemenReich{reichset}/pcs.txt', delimiter='\t')
ids = [iid.split('_')[-1] for iid in pca['IID']] ## fixing our yemen ids
pca['FID1'] = ids
pca.set_index('FID1', inplace=True)
ddf = pca.join(meta).dropna(subset=['Population'])

pops = sorted(Counter(ddf.Population))
D = np.zeros((len(pops),len(pops)))
for i1 in range(len(pops)):
    for i2 in range(i1+1, len(pops)):
        D[i1,i2] = popdistance(pops[i1], pops[i2])
D += D.T
D1 = pd.DataFrame(D, index=pops, columns=pops)
D1.to_csv(f'distanceMatrix_{len(pops)}_{reichset}.csv')        
       
