ind=$1
sed -i -E 's/\bLahij\b/Aden/g' $ind
sed -i -E 's/\bDal\b/Aden/g' $ind
sed -i -E 's/\bAbyan\b/Aden/g' $ind

#sed -i -E 's/\bJwf\b/Sheba/g' $ind
sed -i -E 's/\bMaarib\b/Sheba/g' $ind
sed -i -E 's/\bBayda\b/Sheba/g' $ind

#sed -i -E 's/\bHdr\b/Hadramaut/g' $ind
#sed -i -E 's/\bShb\b/Hadramaut/g' $ind

sed -i -E 's/\bIbb\b/Aljanad/g' $ind
sed -i -E 's/\bTaizz\b/Aljanad/g' $ind

sed -i -E 's/\bAmran\b/Azal/g' $ind
sed -i -E 's/\bDhamar\b/Azal/g' $ind
sed -i -E 's/\bSaada\b/Azal/g' $ind

sed -i -E 's/\bMahwit\b/Tahamh/g' $ind


#districts = {'Azal': ["Sa'ada", 'Amran', "Sana'a", 'Dhamar'], 
#             'Tahamh': ['Al Mahwit', 'Hajjah', 'Raymah'], 
#             'Hadramaut':['Hadramaut', 'Shabwah', 'Al Maharah'],  ## East
#             'Aljanad': ['Ibb', 'Taizz'], 
#             'Sheba': ['Al Jawf', 'Marib', 'Al Bayda'], ## North/Desert
#             'Aden': ["Al Dhale'e", 'Lahj', 'Abyan', 'Aden'],  ## South/Coast
#             'Hudaydah': ['Al Hudaydah']}  ## West/Coast


