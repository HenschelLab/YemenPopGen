for indfile in AdmixTools_1240K_mind0.01_geno_0.05/yemen_reich1240K_mind0.01_geno_0.05.LD.QC.ind AdmixTools_1240K_mind0.3_geno_0.2/yemen_reich1240K_mind0.3_geno_0.2.LD.QC.ind AdmixTools_1240K_mind0.3_geno_0.2_Mbuti/yemen_reich1240K_mind0.3_geno_0.2.LD.QC.ind AdmixTools_1240K_mind0.5_geno_0.5/yemen_reich1240K_mind0.5_geno_0.5.LD.QC.ind AdmixTools_hgdp_mind0.3_geno_0.2/yemen_hgdp_mind0.3_geno_0.2.LD.QC.ind AdmixTools_HO_mind0.01_geno_0.05/yemen_reichHO_mind0.01_geno_0.05.LD.QC.ind AdmixTools_HO_mind0.3_geno_0.05/yemen_reichHO_mind0.3_geno_0.05.LD.QC.ind AdmixTools_HO_mind0.3_geno_0.2/yemen_reichHO_mind0.3_geno_0.2.LD.QC.ind AdmixTools_HO_mind0.7_geno_0.5_pop10/yemen_reichHO_mind0.7_geno_0.5.LD.QC.ind
do
    echo $indfile;
    tr -s ' ' < $indfile | tr '\t' ' ' |sed 's/^ //' |cut -d' ' -f3|sort |uniq -c |sort -n -r > "$indfile.stats"
done



