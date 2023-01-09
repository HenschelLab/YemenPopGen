ind=$1
sed -i -E 's/\bLahj\b/Aden/g' $ind
sed -i -E 's/\bDal\b/Aden/g' $ind
sed -i -E 's/\bAbyn\b/Aden/g' $ind

sed -i -E 's/\bJwf\b/Sheba/g' $ind
sed -i -E 's/\bMrb\b/Sheba/g' $ind
sed -i -E 's/\bByd\b/Sheba/g' $ind

sed -i -E 's/\bHdr\b/Hadramaut/g' $ind
sed -i -E 's/\bShb\b/Hadramaut/g' $ind

sed -i -E 's/\bRsa\b/Hudaydah/g' $ind

