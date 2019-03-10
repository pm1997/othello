#!/bin/bash

wins_w=0;
wins_b=0;
for i in `seq 1 20`;
	do
		echo "round: "  $i
		w1=$( python3 ./main-game.py <<< $(echo 4; sleep 1; echo 100; sleep 1; echo 4; sleep 1; echo 100 ) | grep -e "Winner")
		for word in $w1; do
			if [ $word == "W" ]; then
				wins_w=$(echo  $wins_w + 1 | bc)
			fi
			if [ $word == "B" ]; then
                                wins_b=$( echo $wins_b + 1 | bc)
                        fi
		done
		echo $w1
done
echo "wins B: " $wins_b
echo "wins W: " $wins_w
w2=$(echo "(" $wins_b "*" 100 ") / ( " $wins_b "+" $wins_w ")" | bc )
echo "B wins: " $w2 " %"
