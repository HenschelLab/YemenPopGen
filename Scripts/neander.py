## conda activate bio (don't use mamba)
import pandas as pd
import allel
from liftover import get_lifter
import tabix
import pandas as pd
#wgsdata = "YemenGenomeAnalysis/WGS/Yemeni.HGDP.APPG.mask.autos.filtered.maf_0_005._chr22.vcf.gz" ## chr 22, only loci with MAF > 0.5%
wgsdata = "YemenGenomeAnalysis/WGS/Yemeni.HGDP.APPG.mask.autos.AF_fix.vcf.gz" ## comprehensive!
def extract(match):
    genotype=match.split(':')[0]
    zeros =  genotype.count('0')
    ones = genotype.count('1')
    if ones+zeros<2: return None
    return ones
def lift(chrom, pos):
    liftdata = convert[chrom][pos]
    if liftdata: return liftdata[0][1]

## fields did not work, all ALT_1 were NaN
## YEMEN
#y22=allel.vcf_to_dataframe("YemenGenomeAnalysis/WGS/Yemeni.HGDP.APPG.mask.autos.filtered.maf_0_005._chr22.vcf.gz")
tb = tabix.open(wgsdata)

##ASian Neanderthal (ASN)
neand = 'EUR-ASN'
asn = pd.read_csv(f'YemenGenomeAnalysis/Neanderthal/neansnps/{neand}/nderived.snp', sep=' ', header=None)
convert = get_lifter('hg19', 'hg38')
sids=pd.read_csv('YemenGenomeAnalysis/WGS/sampleIDs.csv', index_col=0)


for chrom, asn22 in asn.groupby(1):
    
    asn22[6] = [lift(str(chrom) ,pos) for pos in asn22[3]]
    asn22 = asn22.dropna(subset=[6])
    asn22[6] = asn22[6].astype(int)
    neanderData = []
    for pos in asn22[6]:
        matches = tb.query(f"chr{chrom}", pos-1, pos)
        try:
            match = next(matches)
            neanderData.append([pos]+[extract(sinfo) for sinfo in match[9:]])
        except StopIteration:
            pass
    df=pd.DataFrame(neanderData, columns=['Pos']+list(sids['0'])).set_index('Pos')
    df0=df.fillna(0) ## CAUTION: This assumes: absence of evidence (no call) -> hom/ref
    outfile = f'YemenGenomeAnalysis/Neanderthal/neanderPandas_{neand}_{chrom}.csv'
    df0.to_csv(outfile)
    print(f'saved {outfile}')
