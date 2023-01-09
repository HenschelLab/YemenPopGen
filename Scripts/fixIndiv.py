import sys
import pandas as pd
from collections import Counter
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
def country2continent(country):
    try:
        return country_alpha2_to_continent_code(country_name_to_country_alpha2(country.strip()))
    except:
        return None
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

contemporaryOnly = False
yemenCombined = ""

if len(sys.argv)==4:
    indfile0, indfile, reichset = sys.argv[-3:]
if len(sys.argv)==5:
    indfile0, indfile, reichset, yemenCombined = sys.argv[-4:]
## Yemen Metadata
yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv', index_col='Id')
if yemenCombined:
    yemenMeta.Population = 'Yemen'

if reichset in ('1240K', "HO"):
    globalyemen = yemenCombined=='global'
    reich = readReich(reichset, combineYemen=globalyemen)
    reich = reich[['Id', 'Group_Label']].set_index('Id')
    reich.columns = ['Population'] 
else:
    print("Context: HGDP")
    hgdpMeta = pd.read_csv("../HGDP/HGDPid_populations.csv.gz")
    hgdpMeta = hgdpMeta[['Id', 'population']].set_index('Id')    
    hgdpMeta.columns=['Population']
    reich = hgdpMeta

## consider merging highly similar 
meta = pd.concat([yemenMeta, reich])

## all (other) pops
opops = [pop for pop, count in Counter(meta.Population).most_common() if (not pop.startswith('Ignore') and count>=10)]

with open(indfile, 'w') as ind:
    for line in open(indfile0):
        fields=line.split()
        f = fields[0]
        ## fixing
        if f.startswith('urn:wtsi'):
            f = '_'.join(f.split('_')[2:])        
        region = meta['Population'].get(f, 'Control')
        print(line[:line.index(fields[2])] + region, file=ind)