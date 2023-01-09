library(admixtools)
library(tidyverse)
library(pheatmap)
library(vegan)
library(colorspace)
# adapted from https://www.eupedia.com/forum/threads/41493-R-scripts-for-ADMIXTOOLS-2-Nganasankhan-from-Anthrogenica

setwd("/mnt/Drive1/ahenschel/SambaShare/YemenGenomeAnalysis_Unused/WGS")

# Selected world populations, Yemen on governorate level
#p = "San Mbuti_Pygmies Bantu Pima Surui Maya Yakut Daur Tu Dai Han Japanese Uygur Balochi Pathan Makrani Bayda Lahij Adygei Druze\tRussian\tOrcadian French Tuscan  Mozabite Abyan Hadramout Bedouin Palestinian\tHudayda\tTaizz Mahwit Amran Dhamar Ibb Maarib Saada YEMEN SAUDI"

# switching to district level
p = "San Mbuti_Pygmies Bantu Pima Surui Maya Yakut Daur Tu Dai Han Japanese Uygur Balochi Pathan Makrani Adygei Druze\tRussian\tOrcadian French Tuscan  Mozabite Bedouin Palestinian Hudayda Aden Aljanad Azal Hadramout Sheba Tahamh"

pops1 = strsplit(p, '\\s+')[[1]]
#load(file="selpops.rda") # gives a variable pops

#Only run once
#extract_f2('Yemeni.HGDP.APPG.mask.autos.AF_fix_QC', 'F2autosomeMeta2', pops=pops1, format='plink', auto_only = TRUE)

f = fst('~/YemenGenomeAnalysis_Unused/WGS/F2autosomeMeta2', pop1=pops1, pop2=pops1)
df=as.data.frame(f[,-4])
df2=rbind(df,setNames(df[,c(2,1,3)],names(df)))

t1=xtabs(df2[,3]~df2[,1]+df2[,2])

weights=rowMeans(t1) # sort by average distance to other populations

pheatmap (1000*t1, 
          filename="fstAllNGS3b.pdf", 
          clustering_callback=function(...)hclust(as.dist(t1) ),
#          clustering_callback=function(...)reorder(hclust(as.dist(t)),weights)
          legend=F,border_color=NA,cellwidth=18,cellheight=18,
          treeheight_row=80,treeheight_col=80,
          display_numbers=T,number_format="%.0f",number_color="black",
          colorRampPalette(hex(HSV(c(210,210,130,60,40,20,0) ,c(0,.5,.5,.5,.5,.5,.5),1)))(256))
