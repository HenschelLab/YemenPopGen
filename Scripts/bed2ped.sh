 ## this could be done systematically for more thresholds
 
 base0=yemen_clean_reich1240K4
 base1=yemen_reich1240K
 t1=0.1
 t2=0.2
 plink --bfile $base0 --mind $t1 --geno $t2 --make-bed --out ${base1}_mind${t1}_geno_${t2}
 mv ${base1}_mind${t1}_geno_${t2}* Missingness

#cd Missingness
#base=yemen_reich1240K_mind0.1_geno_0.2
#plink --bfile $base --recode --out $base