#!/bin/bash
# echo 4; sleep 1; echo 100; sleep 1; echo y; sleep 1; echo 4; sleep 1; echo 100
wins_w=0;
wins_b=0;
temp="temp_ab_mc.txt"
durations="";
for i in `seq 1 100`;
	do
		echo "round: "  $i
		# python3 ./main-game.py <<< $(echo 2; sleep 1; echo 100; sleep 1; echo y; sleep 1; echo n; sleep 1;
		python3 ./main-game.py <<< $(echo 3; sleep 1; echo 2; ) | tee $temp
		#w1=$( python3 ./main-game.py <<< $(echo 2; sleep 1; echo 100; sleep 1; echo y; sleep 1; echo n; sleep 1; echo 4; sleep 1; echo 100; sleep 1; echo y; sleep 1; echo 4 ) |  grep -e "Winner")
		w1=$( cat $temp | grep "Winner" )
		for word in $w1; do
			if [ $word == "W" ]; then
				wins_w=$(echo  $wins_w + 1 | bc)
			fi
			if [ $word == "B" ]; then
                                wins_b=$( echo $wins_b + 1 | bc)
                        fi
		done
		echo $w1
		w2=$( cat $temp1 | grep "duration" )
		echo $w2
		durations=$(echo -ne "$durations\n$w2")
done
fileName="result_ab_mc.txt"
echo "wins B: " $wins_b > $fileName
echo "wins W: " $wins_w >> $fileName
w2=$(echo "(" $wins_b "*" 100 ") / ( " $wins_b "+" $wins_w ")" | bc )
echo "B wins: " $w2 " %" >> $fileName
echo -ne "$durations" >> $fileName
