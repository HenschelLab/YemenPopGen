library(detectRUNS)
library(dplyr)
######################################################################################
#############                   Genotype Arrays                             ##########
######################################################################################

#setwd("/home/ahenschel/R/Yemen")
## note: ped files need to be space sep, not tab!
#runs0 = slidingRUNS.run('y22.ped', 'y22.map')
#write.csv(runs, 'runs.csv')

## Yemen+OOA, 644K SNPs
pedfile='/home/ahenschel/Dropbox/Yemen/YemenGenomeAnalysis/AdmixTools_Yemen_OOA_geno05/yemen_ooa_geno05.F.ped'
mapfile='/home/ahenschel/Dropbox/Yemen/YemenGenomeAnalysis/AdmixTools_Yemen_OOA_geno05/yemen_ooa_geno05.F.map'

## Yemen, 2.33M SNPs (raw, no LD, no nothing)
pedfile = '~/Dropbox/Yemen/YemenGenomeAnalysis/RawGenotypeData/yemen.ped'
mapfile = '~/Dropbox/Yemen/YemenGenomeAnalysis/RawGenotypeData/yemen.map'

## for more comparison:
setwd('~/Dropbox/Yemen/YemenGenomeAnalysis/YemenGenomeAnalysis/AdmixTools_HO_mind0.01_geno_0.05/')
pedfile = '~/Dropbox/Yemen/YemenGenomeAnalysis/YemenGenomeAnalysis/AdmixTools_HO_mind0.01_geno_0.05/yemen_reichHO_mind0.01_geno_0.05.LD.QC.ped'
mapfile = '~/Dropbox/Yemen/YemenGenomeAnalysis/YemenGenomeAnalysis/AdmixTools_HO_mind0.01_geno_0.05/yemen_reichHO_mind0.01_geno_0.05.LD.QC.map'

precalc = FALSE
if (precalc) {
  runsPed = read.csv('runsPed.csv')
} else {
  runsPed = slidingRUNS.run(pedfile, mapfile)
  write.csv(runsPed, 'runsPed_.csv')
}
meta=read.csv('~/Dropbox/Yemen/YemenGenomeAnalysis/Metadata/yemenRegions.csv')
#"Dal"  "Rsa"  "Mhw"  "Jwf"  "Ibb"  "Dhm"  "Byd"  "Lahj" "Abyn" "Sad"  "San"  "Hdr"  "Mrb"  "Shb"  "Amr"  "Haj"  "Tiz" 

gov2dist3 = c("Sad"="Azal", "Amr"="Azal", "San"="Azal", "Dhm"="Azal", "Mhw"="Tahamh", "Haj"="Tahamh", 
             "Raymah"="Tahamh", "Hdr"="Hadramaut", "Shb"="Hadramaut", "Al Maharah"="Hadramaut", 
             "Ibb"="Aljanad", "Tiz"="Aljanad", "Jwf"="Sheba", "Mrb"="Sheba", "Byd"="Sheba", "Dal"="Aden", 
             "Lahj"="Aden", "Abyn"="Aden", "Aden"="Aden", "Rsa"="Hudayda")

ids=unique(runsPed$group)
for (i in 1:nrow(meta)) {
  id = meta[i,'Id']
  pop = meta[i, 'Region']
  #shortId = tail(str_split(id, '_')[[1]], n=1)  ## R?? WTF?!? id.split('_')[-1]
  longId = ids[grepl(id, ids)]
  runsPed$group[runsPed$id==longId] = gov2dist3[pop]
}

## masking out the centromeric regions, as they inconsistently add some very large RoHs to some
centrom = c(135,93.3,91,50.4,48.4,61,59.9,45.6,49,40.2,53.7,35.8,17.9,17.6,19,36.6,24,
            17.2,26.5,27.5,13.2,14.7,60.6,12.5)

yemen169 = filter(runsPed, grepl('3577STDY', id))
for (chromo in 1:length(centrom)) {
  centromPos = centrom[chromo]
  if (chromo==1) {l=15} else {l=3}
  yemen169 = filter(yemen169, (chrom==chromo & (to<(centromPos-l)*M | from>(centromPos+l)*M)) | chrom!=chromo)
}

## creates violin plots per chromosome
plot_ViolinRuns(yemen169, method='mean')
plot_ViolinRuns(yemen169, method='sum')

## F_RoH
yemen169a = filter(yemen169, lengthBps>300000)
froh=Froh_inbreeding(runs=yemen169a, mapFile = mapfile)
frohst = froh %>% group_by(group) %>% summarise_at(vars(Froh_genome), list(mean=mean, sd=sd))
ggplot(frohst) + geom_bar(aes(x=group, y=mean), stat='identity') + geom_errorbar(aes(x=group, ymin=mean-sd, ymax=mean+sd)) + ylab(TeX("$F_{RoH}$")) + xlab("Yemen District")
plot_Runs(yemen169a, savePlots = TRUE, separatePlots = TRUE, outputName = 'yemen168_300K')

plot_ViolinRuns(yemen169a, method='mean')
plot_ViolinRuns(yemen169a, method='sum')
######################################################################################
#############                   WGS                                         ##########
######################################################################################
setwd('~/YemenGenomeAnalysis_Unused/WGS/RoH')
## Metadata, needs some prepping

pops='/home/ahenschel/Dropbox/Yemen/YemenGenomeAnalysis/Metadata/combined4Lintrack.pop'
pops=read.csv(pops, sep='\t')

#pops=pops[1:46,] ## our samples only 
## governorates to districts
colnames(pops) = c('id', 'gov')
gov2dist = c("Saada"="Azal", "Amran"="Azal", "Sanaa"="Azal", "Dhamar"="Azal", "Mahwit"="Tahamh", "Hajjah"="Tahamh", 
             "Raymah"="Tahamh", "Hadramout"="Hadramaut", "Shabwah"="Hadramaut", "Al Maharah"="Hadramaut", 
             "Ibb"="Aljanad", "Taizz"="Aljanad", "Al Jawf"="Sheba", "Maarib"="Sheba", "Bayda"="Sheba", "Al Dhale'e"="Aden", 
             "Lahij"="Aden", "Abyan"="Aden", "Aden"="Aden", "Hudayda"="Hudayda")
#unique(pops$gov)
for (pop in names(gov2dist)) {
  pops$gov[pops$gov==pop] = gov2dist[pop]
}


## BCFtools RoH (based on HMMs)
## piecing chromosomes from WGS together
## filtering for ROHs>100K bp
## left join with population table, to get a group stats. this is cumbersome to use with 
## other detectRUNs tools like summaryRuns
# single bcftools file too large, split down into chromosomes, see shell scripts
#runs = readExternalRuns(inputFile = roh, program = 'BCFtools')


for (i in 1:22) {
  roh = paste("roh_chr", i, ".txt.gz", sep='')
  sprintf("Dealing with %s", roh)  
  runs = readExternalRuns(inputFile = roh, program = 'BCFtools')
  runs100K = filter(runs, lengthBps>100000)
  #runs100Ka = merge(x = select(runs100K, -group), y = pops, by='id', all.x=TRUE)
  if (i==1) {df=runs100K}
  else {df=rbind(df,runs100K)}
}
write.csv(df, "runs_all.csv")
#plot_Runs(runsG1)
df = read.csv("runs_all.csv")
plot_ViolinRuns(df)
