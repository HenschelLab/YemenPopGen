import sys
import pandas as pd
from collections import Counter


def readReich(reichset, contemporaryOnly=False, QC=False, addRegion=False, combineYemen=False):
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
    if addRegion:
        reich["Region"] = [country2continent(country) for country in reich.Country]
        reich = reich.dropna(subset=['Region']) # drop few entries where we couldnt find the continent
    if combineYemen:
        reich.loc[reich.Country=='Yemen', 'Group_Label'] = 'Yemen'        
    return reich

## combining many datasets into one
reich = readReich("HO")
#reich = reich[['Id', 'Group_Label']].set_index('Id')
reichDict = dict(zip(reich.Id, reich.Group_Label))

## Luca Pagani's dataset (Egypt+Ethiopia)
lucaMeta = pd.read_csv('../Metadata/PaganiEtAl2015_Sample_RELEASE_List.txt', sep='\t')
lucaD = dict(zip(lucaMeta.Vcf_ID, lucaMeta.Population))

indfile0, indfile  = sys.argv[-2:]

yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv')
ooa = pd.read_excel('../Metadata/ooa_meta.xlsx')

meta = dict(zip(yemenMeta.Id, yemenMeta.Population))
meta.update(dict(zip(map(str, ooa.Sample), ooa.Population)))
meta.update(reichDict)
meta.update(lucaD)

with open(indfile, 'w') as ind:
    for line in open(indfile0):
        fields=line.split()
        iid = fields[0]
        ## fixing
        if iid.startswith('urn:wtsi:'): 
            if '3577STDY' in iid: iid = iid.split('_')[-1]
            else: iid = iid.split(':')[-1]

        region = meta.get(iid, 'Control')
        print(line[:line.index(fields[2])] + region, file=ind)
