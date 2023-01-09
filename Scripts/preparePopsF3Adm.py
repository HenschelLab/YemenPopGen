#taken from fixIndivPopulation.ipynb
# adapting from running 
# qp3Pop -p parfile_qp3Pop_UAE_ME > qp3Pop_UAE_ME.log &
# in PCA_gencall/AdmixTools directory
# assume this script is called in a subdir to PCA_gencall
import sys
import pandas as pd
from collections import Counter
from itertools import combinations
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import numpy as np

## popmerge modes: 
# none (nothing); 
# local (our yemen districts);
# global (our yemen as well as the Yemen populations in Reich HO)
# all (TODO) based on clustering
## F3 mode: admix vs outgroup

## these scripts should be run after conversion to EIGENSTRAT format

popmerge = "none"
base, context, threshold, popmerge, f3mode = sys.argv[-5:]

threshold = int(threshold)

parfileText = f"""genotypename:   {base}.geno
snpname:        {base}.snp
indivname:      {base}_%s.ind
popfilename:    %s
inbreed:	YES%s"""
outgrpText = "\noutgroupmode: YES"

def popPairs(regionstats, downSample=10000):
    poppairs = []
    for r1, r2 in combinations(regionstats, 2):
        poppairs += [(pop1, pop2) for pop1 in r1 for pop2 in r2]
    if downSample and downSample < len(poppairs):
        poppairs = [poppairs[i] for i in np.random.choice(range(10), 3)]
    return poppairs

def prepParameterFiles2(pop, poppairs, popfile='popfile_%s_%s.txt', parameterFile = 'param_qp3Pop_%s_%s', 
                        popmerge='none', f3mode="Adm", outgrp="Mbuti"):
    ## F3 in Admixture mode, not outgroup-mode
    popfilename = popfile % (f3mode, f"{pop}_{popmerge}_{outgroup}")
    parfilename = parameterFile % (f3mode, f"{pop}_{popmerge}_{outgroup}")

    with open(popfilename, 'w') as popfile:    
        if f3mode=='outgroup':
            ## little hack: poppairs just a single list
            for pop2 in poppairs:
                if pop != pop2 and pop!= outgrp and pop2 != outgrp:
                    print(pop, pop2, outgrp, file=popfile)           
        else:
            for pop1, pop2 in poppairs:
                print(pop1, pop2, pop, file=popfile)
                
    with open(parfilename, 'w') as parfile:
        ptext = parfileText % (popmerge, popfilename, '')
        if f3mode=='outgroup':
            ptext += outgrpText
        print(ptext, file=parfile)

    cmd = f"qp3Pop -p {parfilename} > qp3Pop_{pop}_{popmerge}_{f3mode}_{outgrp}.log"
    print(cmd)

def country2continent(country):
    try:
        return country_alpha2_to_continent_code(country_name_to_country_alpha2(country.strip()))
    except:
        return None

def readReich(reichset, contemporaryOnly=False, QC=False, addRegion=False, popmerge=False):
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
    if popmerge=='global':
        reich.loc[reich.Country=='Yemen', 'Group_Label'] = 'Yemen'   
        ## TODO: combine also other populations based on HC     
    return reich
def line2pop(line):
    fields = line.split()
    f = fields[0]
    if f.startswith('urn:wtsi'):
        f = '_'.join(f.split('_')[2:])
    region = meta['Population'].get(f, 'Control')
    #if region=='Control':
    #    print(line.rstrip())
    return f, region
def findSolidPops(indfile):
    data = [line2pop(line) for line in open(indfile)]    
    return Counter(list(zip(*data))[1])
def filterPops(rdf, minMembers=10, column='population'):
    return [pop for pop, popC in Counter(rdf[column]).most_common() if popC>minMembers]

if not context=='hgdp':
    reich = readReich(context, QC=True, addRegion=True, popmerge=popmerge)
    regionstats = [filterPops(rdf, minMembers=threshold, column='Group_Label') for r, rdf in reich.groupby('Region')]
    reich = reich[['Id', 'Group_Label']].set_index('Id')
    reich.columns = ['Population'] 
else:
    hgdpMeta = pd.read_csv("../HGDP/HGDPid_populations.csv.gz")
    regionstats = [filterPops(r, rdf, minMembers=threshold) for r, rdf in hgdpMeta.groupby('Region')]    
    hgdpMeta = hgdpMeta[['Id', 'population']].set_index('Id')     
    hgdpMeta.columns=['Population']
    reich = hgdpMeta

## Yemen Metadata

yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv', index_col='Id')
meta = pd.concat([yemenMeta, reich])
regionPops = [line.strip() for line in open(f"../Data/popfile_{context}_3000.txt")][:-17]
if f3mode=='outgroup':
    pairs = [pop for pop, count in findSolidPops(f"{base}.ind").items() if count>=threshold and pop in regionPops]
else:
    pairs = popPairs(regionstats)

if popmerge:
    yemenPops=["Yemen"]
else:
    yemenPops = ['Dhm','Abyn', 'Sad', 'Mhw', 'Lahj', 'Jwf', 'San', 'Mrb', 'Amr', 'Haj', 'Shb', 'Hdr']

for outgroup in "Spanish Han Tibetan Druze Iranian GIH.SG LWK.SG".split():
    for ypop in yemenPops:
        prepParameterFiles2(ypop, pairs, popmerge=popmerge, f3mode=f3mode, outgrp=outgroup)
    
