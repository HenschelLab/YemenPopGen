#

import sys
import pandas as pd
from collections import Counter

context = sys.argv[-1]

def readReich(reichset, contemporaryOnly=False, QC=True):
    if reichset=='1240K':
        columns2keep = [1,9, 12, 14, 15, 16]
    elif reichset=='HO':
        columns2keep = [1, 5, 7, 9, 10, 11]
    columnNames = 'Id Date Group_Label Country Lat Long'.split()
    reich=pd.read_csv(f"../Reich/v44.3_{reichset}_public.anno", sep='\t')
    reich = reich.iloc[:,columns2keep]
    reich.columns = columnNames

    if QC:
        reich = reich[~reich.Group_Label.str.startswith("Ignore_")]
        reich = reich[~reich.Group_Label.str.endswith("_outlier")]
    if contemporaryOnly:
        reich = reich[reich.Date==0]
    return reich

if not context=='hgdp':
    reich = readReich(context, QC=True)
    reich = reich[['Id', 'Group_Label']].set_index('Id')
    reich.columns = ['Population'] 
else:
    hgdpMeta = pd.read_csv("../HGDP/HGDPid_populations.csv.gz")
    hgdpMeta = hgdpMeta[['Id', 'population']].set_index('Id')     
    hgdpMeta.columns=['Population']
    reich = hgdpMeta

## Yemen Metadata
yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv', index_col='Id')
meta = pd.concat([yemenMeta, reich])

meta.to_csv(f'../Metadata/meta_{context}_Yemen.csv')
