import tabix
wdir = '/media/shared/hgdp/neansnps'
asn = pd.read_csv('ASN/nderived.snp', sep=' ', header=None)
import pandas as pd
import pandas as pd
asn = pd.read_csv('ASN/nderived.snp', sep=' ', header=None)
cd ..
asn = pd.read_csv('ASN/nderived.snp', sep=' ', header=None)
asn
pwd
ll ../isec/Yemeni.HGDP.APPG.mask.autos.*
vcf= "../isec/Yemeni.HGDP.APPG.mask.autos.vcf.gz"
yemen = tabix.open(vcf)
yemen.query("22", 51042000, 510420010)
yemen.query("22")
yemen.query?
yemen.query("22", 51000000, 520420010)
yemen.query("22", 50000000, 520420010)
yemen.query("22", 40000000, 520420010)
yemen.query("22", 30000000, 520420010)
yemen.query("chr22", 30000000, 520420010)
yemen
yemen.query("22", 30000000, 520420010)
yemen.query("22c", 30000000, 520420010)
asn
asn[asn[1]==22]
asn[asn[1]==22]
asn[asn[22]]
#asn = pd.read_csv('ASN/nderived.snp', sep=' ', header=None)
pos22 = [line.strip() for line in open('/tmp/pos22.chr')]
pos22 = set([line.strip() for line in open('/tmp/pos22.chr')])
len(pos22)
asn22 = asn[asn[1]==22]
asn22
len([pos for pos in asn[3] if str(pos) in pos22])
!conda install -c bioconda -y liftover
!pip install liftover
len([pos for pos in asn[3] if str(pos) in pos22])
from liftover import get_lifter
convert = get_lifter('hg19', 'hg38')
chrom = '22'
len([pos for pos in asn22[3] if str(pos) in pos22])
pos = 17616151
converter['22'][pos]
convert['22'][pos]
def check(chrom, pos):
    lift = convert[chrom][pos][0][1]
    if lift and len(lift)>0:
        liftpos = lift[0][1]
        if str(liftpos) in pos22:
            return liftpos
[pos for pos in asn[3] if check('22', pos) is not None]
def check(chrom, pos):
    lift = convert[chrom][pos]
    if lift and len(lift)>0:
        liftpos = lift[0][1]
        if str(liftpos) in pos22:
            return liftpos
[pos for pos in asn[3] if check('22', pos) is not None]
history
len([pos for pos in asn[3] if check('22', pos) is not None])
len(pos22)
len(asn[3])
asn22[3]
asn
[pos for pos in asn[3] if check('22', pos) is not None][:10]
[(check('22',pos), pos) for pos in asn[3] if check('22', pos) is not None][:10]
p10 = [(check('22',pos), pos) for pos in asn[3] if check('22', pos) is not None][:10]
asn[asn[3]==p10[1]]
p10[1]
p10
p10[0][1]
asn[asn[3]==p10[0][1]]
yemen.query("22", 30613131, 30613131)
yemen.query("chr22", 30613131, 30613131)
history
