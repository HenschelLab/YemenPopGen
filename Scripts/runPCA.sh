# conda activate vcf
## run like so:
#PCA_gencall]$ bash ../runPCA.sh 


#context=hgdp
#contextDir=HGDP
#context=reich1240K
context=reichHO
contextDir=Reich
study=swAsia

## extract overlap
snpfile=${study}_${context}.snps 

## Specific for Reich's data: 1234 coding into ACGT
plink --bfile ${contextDir}/${context} --alleleACGT --make-bed --out ${contextDir}/${context}_ACGT
plink --bfile $study --extract $snpfile --make-bed --out ${study}_ov${context}
plink --bfile ${contextDir}/${context}_ACGT --extract $snpfile --make-bed --out ${contextDir}/${context}_ov${study}

## merge (fails usually when combining Affy and Illumina - because of strand confusion)
plink --bfile ${contextDir}/${context}_ov${study} --bmerge ${study}_ov${context}.bed ${study}_ov${context}.bim ${study}_ov${context}.fam --make-bed --out ${study}_${context}
## yields missnp file, really looks like strand confusion
## Investigating Strand confusion (breaks the merging)
#plink  --bfile ${study}_ov${context} --flip ${study}_${context}-merge.missnp --make-bed --out ${study}_ov${context}2

#plink  --bfile ${contextDir}/${context}_ov${study} --bmerge ${study}_ov${context}2.bed ${study}_ov${context}2.bim ${study}_ov${context}2.fam --make-bed --out ${study}_${context}3
#this might have still led to some (genuine?) triallelic SNPs, check how many they are. Assuming they are few: phew. Exclude them:
plink  --bfile ${contextDir}/${context}_ov${study} --exclude ${study}_${context}3-merge.missnp --make-bed --out ${contextDir}/${context}_ov${study}2
plink  --bfile ${study}_ov${context}2 --exclude ${study}_${context}3-merge.missnp --make-bed --out ${study}_ov${context}3
plink  --bfile ${contextDir}/${context}_ov${study}2 --bmerge ${study}_ov${context}3.bed ${study}_ov${context}3.bim ${study}_ov${context}3.fam --allow-no-sex --make-bed --out ${study}_${context}4

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
