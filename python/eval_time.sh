#!/bin/bash
t=$(cat $1 )
sum=0
w=0
for word in $t; do
	w=$( echo "$w + 1" | bc)
	if [ "$w" == "3" ]; then
		echo $word
		w2=$(echo $word | cut -d'.' -f 1)
		sum=$(echo "$sum + $w2" | bc )
	fi
	if [ "$w" == "4" ]; then
                w=0
        fi
done
echo $sum
echo $(echo "$sum / 100" | bc)
echo "fertig"
