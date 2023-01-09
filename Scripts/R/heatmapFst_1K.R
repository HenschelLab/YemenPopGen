
pops1K <- scan('popfile_HO_1000.txt', character(), quote="")
pops1K = pops1K[-4]

f = fst('F2_1K_Ancient') # F21K
# convert FST or f2 pairs to square matrix
df=as.data.frame(f[,-4])
df2=rbind(df,setNames(df[,c(2,1,3)],names(df)))
t=xtabs(df2[,3]~df2[,1]+df2[,2])
#t = t[-11,-11] ## taking out Jew_Yemenite (2x)
heatmap(as.matrix(t), distfun = as.dist, scale = "none", revC = T)


## some ancient stuff, see tutorial
right = c('Chimp.REF', 'Mbuti', 'Russia_Ust_Ishim.DG', 'Switzerland_Bichon.SG')
left = c('Altai_Neanderthal.DG', 'Vindija_Neanderthal.DG')
target = 'Denisova.DG'
apops = c(left, right, target)

f = fst(prefix, apops, apops, adjust_pseudohaploid = FALSE)
df=as.data.frame(f[,-4])
df2=rbind(df,setNames(df[,c(2,1,3)],names(df)))
t=xtabs(df2[,3]~df2[,1]+df2[,2])
#heatmap(t) ## see above, Dan's email
