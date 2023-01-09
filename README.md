# Yemen Population Genetics and genetic history

Running all scripts with conda environment admix:
conda activate admix (contains plink as well as admixtools, jupyter, ipython, etc)
See yaml file in Scripts.

See also small READMEs in subdirs (particularly Scripts/README)

## Reduction of the dataset from 480 to 169 yemeni using plink:
```
conda activate vcf
cd /bmshare/ahenschel/Pierre/GenotypeData/analysis
grep "3577STDY" omni2.5-8_yemcha_20150605.zcall.fam | cut -d$'\t' -f1 > yemen.txt
plink --bfile omni2.5-8_yemcha_20150605.gencall.smajor --keep-fam yemen.txt  --make-bed --out yemen
```
## Merging datasets,
see Scripts/README

## Running Admixtools (not provided ins GitHub)

See directories AdmixTools_(dataset)_mind(indiv.missingness)_geno(genotype.missingness):
```
drwxrwxr-x 2 ahenschel ahenschel  4096 Sep 12 10:34 AdmixTools_1240K_mind0.01_geno_0.05/
drwxrwxr-x 3 ahenschel ahenschel  4096 Jul  2 15:00 AdmixTools_1240K_mind0.3_geno_0.2/
drwxrwxr-x 2 ahenschel ahenschel  4096 Sep 12 10:14 AdmixTools_1240K_mind0.3_geno_0.2_Mbuti/
drwxrwxr-x 2 ahenschel ahenschel  4096 Sep 10 17:03 AdmixTools_1240K_mind0.5_geno_0.5/
drwxrwxr-x 2 ahenschel ahenschel 12288 Jun 30 16:54 AdmixTools_hgdp_mind0.3_geno_0.2/
drwxrwxr-x 2 ahenschel ahenschel  4096 Sep  5 10:21 AdmixTools_HO_mind0.01_geno_0.05/
drwxrwxr-x 2 ahenschel ahenschel  4096 May 31 10:54 AdmixTools_HO_mind0.3_geno_0.05/
drwxrwxr-x 5 ahenschel ahenschel 12288 Sep  5 10:36 AdmixTools_HO_mind0.3_geno_0.2/
drwxrwxr-x 2 ahenschel ahenschel 12288 May 31 10:49 AdmixTools_HO_mind0.7_geno_0.5_pop10/
```

## Visualization:
See Notebooks directory

### For Flash-PCA
Run jupyter notebook
change into conda env with Python 3 (impute, vcf)
Adapting 
cp /bmshare/syafiq/flashpca/UKBioBankPCA.ipynb .
renamed to yemenPCA.ipynb
jupyter notebook --no-browser --ip=0.0.0.0
10.10.3.109:8888/
copy the token

## Running PCA
flashpca (now deprecated, as this is rerun with smartPCA)

docker run -d -it --name flashpca-yemen -v /bmshare/ahenschel/Pierre/GenotypeData/analysis/:/home/flashpca-user/data flashpca/latest
docker exec -it flashpca-yemen bash # execute a bash
(it requires that anaylis (the dir holding bed/bim/fam) is readable to all
chmod -R a+r analysis

