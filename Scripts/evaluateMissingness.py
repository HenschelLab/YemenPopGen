import pandas as pd
from scipy.cluster.hierarchy import average, fcluster
from scipy.spatial.distance import squareform

## dm: replace with 'missingnessDistMat_1240K.csv'

dm = pd.read_csv('distanceMatrix_10_HO_ibs.csv', sep=',', index_col=0)
dmc = squareform(dm)
linkage = average(dmc)



