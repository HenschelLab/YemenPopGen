
for K in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
    admixture --cv yemen_clean_reich1240K4.bed $K | tee log_y1240_${K}.out &
done
