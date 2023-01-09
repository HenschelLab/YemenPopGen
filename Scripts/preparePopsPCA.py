#taken from fixIndivPopulation.ipynb
# adapting from running 
# qp3Pop -p parfile_qp3Pop_UAE_ME > qp3Pop_UAE_ME.log &
# in PCA_gencall/AdmixTools directory
# assume this script is called in a subdir to YemenGenomeAnalysis (was PCA_gencall)
import sys
import pandas as pd
from collections import Counter

base, context, threshold = sys.argv[-3:]
threshold = int(threshold)

parfileText = f"""genotypename:   {base}.geno
snpname:        {base}.snp
indivname:      {base}.ind
evecoutname:    {base}.pcs.txt
evaloutname:    {base}.pve.txt
poplistname:    %s
lsqproject: %s
"""
#8001717
def prepParameterFiles(otherPops, lsqproject="YES", popfilename='popfile.txt', parameterFile='param_pca', dry=False):
    with open(popfilename, 'w') as popfile:
        for pop in otherPops:
            print(pop, file=popfile)
    with open(parameterFile, 'w') as parfile:
        print(parfileText % (popfilename, lsqproject), file=parfile)
    cmd = f"smartpca -p {parameterFile} > smartpca.log"
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
    region = meta['Population'].get(f, 'Not found')
    if region=='Control' or region == 'Not found':
        #print(region, line.rstrip(), file=sys.stderr)
        pass
    return f, region

def findSolidPops(indfile):
    data = [line2pop(line) for line in open(indfile)]    
    return Counter(list(zip(*data))[1])

yemenMeta = pd.read_csv('../Metadata/yemenPopulations.csv', index_col='Id')

if not context=='hgdp':
    reich = readReich(context, QC=True, contemporaryOnly=True)
    reich = reich[['Id', 'Group_Label']].set_index('Id')
    reich.columns = ['Population'] 
else:
    hgdpMeta = pd.read_csv("../HGDP/HGDPid_populations.csv.gz")
    hgdpMeta = hgdpMeta[['Id', 'population']].set_index('Id')     
    hgdpMeta.columns=['Population']
    reich = hgdpMeta

## Yemen Metadata

meta = pd.concat([yemenMeta, reich])

#opops = [pop for pop, count in Counter(meta.Population).items() if (not pop.startswith('Ignore') and count>=threshold)]

opops = [pop for pop, count in findSolidPops(f"{base}.ind").items() if count>=threshold and pop in set(meta.Population)] #use only contemporary populations for spanning the PCs

prepParameterFiles(opops)
    
