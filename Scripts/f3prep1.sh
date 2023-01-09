# Preparing the merged (but unrefined) plink file containing our samples + reich context data
# conda activate admix (now has plink also)
# usage bash f3prep1.sh 0.3 0.2 1240K 1
set -e

#cd /bmshare/ahenschel/Pierre/GenotypeData/analysis/PCA_gencall
#cd /home/ahenschel/Dropbox/Yemen/YemenGenomeAnalysis
#t1=0.3 ## keeps all yemen samples
#t2=0.2
#dataset=HO
t1=$1
t2=$2
dataset=$3
minpopsize=$4

## 4 is the last step in the merging procedure, see other script
## /bmshare/ahenschel/Pierre/GenotypeData/analysis/merge3runPCA.sh

if [ $dataset = "hgdp"]
then
    base0="yemen_clean_${dataset}2"
    base1="yemen_${dataset}"
else
    base0="yemen_clean_reich${dataset}4"
    base1="yemen_reich${dataset}"
fi

base=${base1}_mind${t1}_geno_${t2}
wdir="AdmixTools_${dataset}_mind${t1}_geno_${t2}_pop${minpopsize}"

## Filtering for missingness
## https://www.cog-genomics.org/plink/1.9/filter#missing
plink --bfile $base0 --mind $t1 --geno $t2 --make-bed --out $base
plink --bfile $base --missing --out $base
## LD: also include linkage disequilibrium based variant pruning
plink --bfile $base --indep 50 5 2 --out ${base}.LD
plink --bfile $base --exclude ${base}.LD.prune.out --make-bed --out ${base}.LD
#see LD pruning stats: more yemen_reich1240K_mind0.1_geno_0.2.LD.log

mkdir -p $wdir
mv ${base}* $wdir
cd $wdir
base=${base}.LD

## QC (better earlier) remove outliers/Ignore annotated samples
python ../fixReichPlink.py $base $dataset > $base.2brm
plink --bfile $base --remove $base.2brm --make-bed --out ${base}.QC
base=${base}.QC

## BED to PED
plink --bfile $base --recode --out $base

## Fixing phenotype column (convertf ignores samples with phenotype -9)
awk 'BEGIN{FS=OFS=" "} $6=="-9"{$6="1"} 1' ${base}.ped > ${base}_tmp.ped
mv ${base}_tmp.ped ${base}.ped 

#cd $wdir
## Admixtools
# create parameter file for Plink->EIGENSTRAT conversion
bash ../Missingness/f3prep_cat.sh $dataset $base

## also automizing the par(ameter) file generation
convertf -p convertfPparams_${dataset}.txt

## retrofitting population info into EIGENSTRAT's ind file
python ../fixIndiv.py ${base}0.ind ${base}.ind $dataset
ln -s ${base}.ind ${base}_none.ind
python ../fixIndiv.py ${base}0.ind ${base}_local.ind $dataset local
python ../fixIndiv.py ${base}0.ind ${base}_global.ind $dataset global

## creating population files (input for admixtools)
python ../preparePops.py $base $dataset $minpopsize > qp3Pop_cmds.sh
python ../preparePopsF3Adm.py $base $dataset $minpopsize none admix >> qp3Pop_cmds.sh
python ../preparePopsF3Adm.py $base $dataset $minpopsize local outgroup >> qp3Pop_cmds.sh
python ../preparePopsF3Adm.py $base $dataset $minpopsize global admix >> qp3Pop_cmds.sh
python ../preparePopsPCA.py $base $dataset 1 >> qp3Pop_cmds.sh

parallel < qp3Pop_cmds.sh

for i in qp3Pop_*.log
do 
    grep -v "^  no data" $i > $i.csv
done
