library(admixtools)
library(tidyverse)

setwd('/home/ahenschel/R/Yemen')
data = "yemen_reichHO_mind0.3_geno_0.2.LD.QC"
pops <- scan('popfile_HO_4000.txt', character(), quote="")

yemenpops <- c("Mrb",  "Hdr")
pop1 <- "Chimp.REF"
f4results <- f4(data, pop1, pops, yemenpops, pops)

f4sign = f4results[(f4results$z < -4.0), ]
f4sign = f4sign[f4sign$pop2 != f4sign$pop3,]
f4sign = f4sign[f4sign$pop1 != f4sign$pop4,]
f4sign = f4sign[order(f4sign$z),]
write.csv(f4sign, file = 'f4sign4000.csv')

# f4results2 <- f4(data, pop1, pops, yemenpops, pops, allsnps = FALSE)
# f4sign = f4results2[(f4results2$z < -4.0), ]
# f4sign = f4sign[f4sign$pop2 != f4sign$pop3,]
# f4sign = f4sign[f4sign$pop1 != f4sign$pop4,]
# f4sign = f4sign[order(f4sign$z),]
# write.csv(f4sign, file = 'f4sign2.csv')

