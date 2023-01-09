## analysing missingness patterns
## missingness similarity betwee two samples captured using jaccard
## distance matrix, todo: clustering
## using scikit-allel, so use conda activate impute
import allel
import numpy as np
import pandas as pd
import sys

def jaccardDist(sid1, sid2, cs):    
    A = set(np.where(cs[:,sid1]!=-2)[0])
    B = set(np.where(cs[:,sid2]!=-2)[0])
    union = len(A.union(B))
    intersection = len(A.intersection(B))
    return 1-intersection/union

reichset=sys.argv[-1]
vcf = f'yemen_clean_reich{reichset}.vcf'

callset = allel.read_vcf(vcf)
samples = callset['samples']
cs = callset['calldata/GT'].sum(axis=2)

DM = np.zeros((len(samples), len(samples)))

for i1 in range(len(samples)):
    for i2 in range(i1+1, len(samples)):
        DM[i1, i2] = jaccardDist(i1, i2, cs)

DM += DM.T

pd.DataFrame(DM, index=samples, columns=samples).to_csv('missingnessDistMat_{reichset}.csv')
