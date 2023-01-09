## assuming that this is run standing in Missingness subdir
import sys
import pandas as pd
from collections import Counter

contemporaryOnly = False

plinkfile, reichset = sys.argv[-2:]
if reichset=='1240K':
    columns2keep = [1,9, 12, 14, 15, 16]
elif reichset=='HO':
    columns2keep = [1, 5, 7, 9, 10, 11]
columnNames = 'Id Date Group_Label Country Lat Long'.split()

reich=pd.read_csv(f"../Reich/v44.3_{reichset}_public.anno", sep='\t')
reich = reich.iloc[:,columns2keep]
reich.columns = columnNames

## QC
#reich = reich[~reich.Group_Label.str.startswith("Ignore_")]
#reich = reich[~reich.Group_Label.str.endswith("_outlier")]

if contemporaryOnly:
    reich = reich[reich.Date==0]
reichYemen = reich[reich.Country=='Yemen']
reich = reich[['Id', 'Group_Label']].set_index('Id')
reich.columns = ['Population'] 

## Yemen Metadata
yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv', index_col='Id')
meta = pd.concat([yemenMeta, reich])

## all (other) pops
opops = [pop for pop, count in Counter(meta.Population).most_common() if (not pop.startswith('Ignore') and count>=10)]

#with open('removeLowQCids.txt', 'w') as out:

for line in open(f'{plinkfile}.fam'):
    famid, iid = line.split()[:2]
    if iid.startswith('urn:wtsi'):
        iid = '_'.join(iid.split('_')[2:]) 
    population = meta.Population.get(iid, "None")
    if population.startswith("Ignore_") or "outlier" in population or population == "None":
        print(famid, iid)

