#taken from fixIndivPopulation.ipynb
## deprecating this, run preparePopsF3Adm with last arg outgroup
# adapting from running 
# qp3Pop -p parfile_qp3Pop_UAE_ME > qp3Pop_UAE_ME.log &
# in YemenGenomeAnalysis/AdmixTools directory
# assume this script is called in a subdir to YemenGenomeAnalysis

import sys
import pandas as pd
from collections import Counter

base, context, threshold = sys.argv[-3:]
threshold = int(threshold)

parfileText = f"""genotypename:   {base}.geno
snpname:        {base}.snp
indivname:      {base}.ind
popfilename:    %s
inbreed:	YES"""

def prepParameterFiles(pop, otherPops, outgrp="Mbuti", popfile='popfile_%s_vAll_out.txt', parameterFile = 'param_qp3Pop_%s_out', dry=False):
    popfilename = popfile % pop
    parfilename = parameterFile % pop

    with open(popfilename, 'w') as popfile:
        for pop2 in otherPops:
            if pop != pop2 and pop!= outgrp and pop2 != outgrp:
                print(pop, pop2, outgrp, file=popfile)
    with open(parfilename, 'w') as parfile:
        print(parfileText % popfilename, file=parfile)
    cmd = f"qp3Pop -p {parfilename} > qp3Pop_{pop}_out.log"
    print(cmd)

def readReich(reichset, contemporaryOnly=False, QC=False):
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

def line2pop(line):
    fields = line.split()
    f = fields[0]
    if f.startswith('urn:wtsi'):
        f = '_'.join(f.split('_')[2:])
    region = meta['Population'].get(f, 'Control')
    if region=='Control':
        print(line.rstrip())
    return f, region

def findSolidPops(indfile):
    data = [line2pop(line) for line in open(indfile)]    
    return Counter(list(zip(*data))[1])


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

#opops = [pop for pop, count in Counter(meta.Population).items() if (not pop.startswith('Ignore') and count>=threshold)]

#opops = [pop for pop, count in findSolidPops(f"{base}.ind").items() if count>=threshold]

yemenPops = ['Dhm','Abyn', 'Sad', 'Mhw', 'Lahj', 'Jwf', 'San', 'Mrb', 'Amr', 'Haj', 'Shb', 'Hdr']
#for ypop in yemenPops:
#    prepParameterFiles(ypop, opops, outgrp='Biaka_Pygmies')
    
