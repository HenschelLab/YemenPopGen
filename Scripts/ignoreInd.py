import sys
import pandas as pd
'/bmshare/ahenschel/Pierre/GenotypeData/analysis/YemenGenomeAnalysis/AdmixTools_HO_mind0.7_geno_0.5_pop10'
with open(indfile, 'w') as ind:
    for line in open(indfile0):
        fields=line.split()
        f = fields[0]
        region = fields[2].rstrip()
        if f.strip() in ignore:
            region = 'Ignore'
        print(line[:line.index(fields[2])] + region, file=ind)
