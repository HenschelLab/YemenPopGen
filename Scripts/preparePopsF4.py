#taken from fixIndivPopulation.ipynb
# adapting from running 
# qp3Pop -p parfile_qp3Pop_UAE_ME > qp3Pop_UAE_ME.log &
# assume this script is called in a subdir to YemenGenomeAnalysis, eg:
# 
# AdmixTools_HO_mind0.3_geno_0.2]$ python ../Scripts/preparePopsF4.py $base $dataset 10 none > qpDstat.sh 
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

popmerge = ""
base, context, threshold, popmerge = sys.argv[-4:]
if popmerge.lower()=="none":
    popmerge=""
threshold = int(threshold)

parfileText = f"""genotypename:   {base}.geno
snpname:        {base}.snp
indivname:      {base}%s.ind
popfilename:    %s
f4mode:         YES"""

def popPairs(regionstats, downSample=10000):
    poppairs = []
    for r1, r2 in combinations(regionstats, 2):
        poppairs += [(pop1, pop2) for pop1 in r1 for pop2 in r2]
    if downSample and downSample < len(poppairs):
        poppairs = [poppairs[i] for i in np.random.choice(range(10), 3)]
    return poppairs

def prepParameterFiles2(popA, popB, popC, popD="Chimp.REF", popfile='popfile_F4_%s.txt', parameterFile = 'param_F4_%s', popmerge=''):
    ## F3 in Admixture mode, not outgroup-mode
    popmerge1 = popmerge
    if popmerge: popmerge1 = '_'+popmerge
    popfilename = popfile % (f"{popA}_{popB}_{popmerge}")
    parfilename = parameterFile % ( f"{popA}_{popB}_{popmerge}")

    with open(popfilename, 'w') as popfile:    
        for pop in popC:
            print(popA, popB, pop, popD, file=popfile)
                
    with open(parfilename, 'w') as parfile:
        ptext = parfileText % (popmerge1, popfilename)

        print(ptext, file=parfile)

    cmd = f"qpDstat -p {parfilename} > qpDstat_{popA}_{popB}_{popmerge1}.log"
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

def filterPops(rdf, minMembers=10, column='population'):
    return [pop for pop, popC in Counter(rdf[column]).most_common() if popC>minMembers]

reich = readReich(context, QC=True, addRegion=True, popmerge=popmerge)
ancientEurasian = reich[(reich.Date>0) & (reich.Region.isin(["AF", "EU", "AS"]))] 
#popC = list(set(ancientEurasian.Group_Label))
popC = list(set(reich.Group_Label))
indfile = f"{base}.ind"
popstats = Counter([line.split()[-1] for line in open(indfile)])
popC = [pop for pop in popC if popstats.get(pop,0)>threshold]

if popmerge:
    yemenPops=["Yemen"]
else:
    yemenPops = ['Dhm','Abyn', 'Sad', 'Mhw', 'Lahj', 'Jwf', 'San', 'Mrb', 'Amr', 'Haj', 'Shb', 'Hdr']
    yemenPops = ['Abyn', 'Mrb', 'Hdr'] ## start small ;-)

popA = ["Lebanese", "Shaigi.WGA"][0]

for popB in yemenPops:
    prepParameterFiles2(popA, popB, popC, popmerge=popmerge)
    
