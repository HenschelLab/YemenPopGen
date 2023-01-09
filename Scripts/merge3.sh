## merging 3 datasets e.g. context data (Reich/HGDP) + study 1 + study 2
## directories need adjustment
# conda activate vcf
## run like so:
#PCA_gencall]$ bash ../merge3.sh 


#context=hgdp
#contextDir=HGDP
#context=reich1240K
context=reichHO
contextDir=Reich
study1=swAsia
study2=${study2}

## extract overlap
snpfile=${study1}_${study2}_${context}.snps 

## Specific for Reich's data: 1234 coding into ACGT
#plink --bfile ${contextDir}/${context} --alleleACGT --make-bed --out ${contextDir}/${context}_ACGT

## limiting the 3 datasets to the intersection of variants
sco1=${study1}_ovl_${context}
sco2=${study2}_ovl_${context}
sco12=${contextDir}/${context}_ovl_${study1}_${study2}
#plink --bfile $study1 --extract $snpfile --make-bed --out $sco1
#plink --bfile $study2 --extract $snpfile --make-bed --out $sco2
#plink --bfile ${contextDir}/${context} --extract $snpfile --make-bed --out $sco12

## merge (fails usually when combining Affy and Illumina - because of strand confusion)
#plink  --bfile ${sco12} --bmerge $sco1.bed $sco1.bim $sco1.fam --make-bed --out ${study1}_${context}
## yields missnp file, really looks like strand confusion
## Investigating Strand confusion (breaks the merging)
## plink  --bfile ${sco1} --flip ${study1}_${context}-merge.missnp --make-bed --out ${sco1}2

plink  --bfile ${sco12} --bmerge ${sco1}2.bed ${sco1}2.bim ${sco1}2.fam --make-bed --out ${sco1}3
## this might have still led to some (genuine?) triallelic SNPs, check how many they are. Assuming they are few: phew. Exclude them:
plink  --bfile ${sco12} --exclude ${sco1}3-merge.missnp --make-bed --out ${sco12}2
plink  --bfile ${sco1}2 --exclude ${sco1}3-merge.missnp --make-bed --out ${sco1}4
plink  --bfile ${sco12}2 --bmerge ${sco1}4.bed ${sco1}4.bim ${sco1}4.fam --allow-no-sex --make-bed --out ${study1}_${context}_final

## Adding study2 to study1+context
plink  --bfile ${sco2} --exclude ${sco1}3-merge.missnp --make-bed --out ${sco2}2
plink --bfile ${study1}_${context}_final --bmerge ${sco2}2.bed ${sco2}2.bim ${sco2}2.fam --allow-no-sex --make-bed --out ${study1}_${study2}_${context}_final


## again, this might lead to 
plink  --bfile ${sco2} --flip ${study1}_${study2}_${context}_final-merge.missnp --make-bed --out ${sco2}2

## QC on the final merged set
plink --bfile ${study1}_${study2}_${context}_final --maf 0.05 --make-bed --out ${study1}_${study2}_${context}_final_QC
plink --bfile ${study1}_${study2}_${context}_final_QC --indep-pairwise 1000 10 0.4 --allow-no-sex --out ${study1}_${study2}_${context}_final_QC1

## Deprecated (better to exclude with --exclude, see above) Some snps keep being problematic, remove them
#grep -v -f  ${study}_${context}-merge.missnp  ${study}_${context}.snps > ${study}_${context}2.snps
#plink  --bfile ${study}_ovhgdp2 --bmerge HGDP/hgdp_ov${study}.bed HGDP/hgdp_ov${study}.bim HGDP/hgdp_ov${study}.fam --make-bed --out ${study}_hgdp2

#plink --bfile ${study} --extract yemen_hgdp.snps --make-bed --out ${study}_ovhgdp
#plink --bfile HGDP/hgdp --extract yemen_hgdp.snps --make-bed --out HGDP/hgdp_ov${study}

## Trying again
#plink  --bfile ${study}_ovhgdp2 --bmerge HGDP/hgdp_ov${study}.bed HGDP/hgdp_ov${study}.bim HGDP/hgdp_ov${study}.fam --make-bed --out ${study}_hgdp2
#--flip: 164572 SNPs flipped.

#while read p; do grep -w "$p" ${study}.bim ${contextDir}/${context}.bim; done < ${study}_${context}-merge100.missnp > checkStrandconfusion_yemen_hgdp.log
#docker exec -it flashpca-yemen bash