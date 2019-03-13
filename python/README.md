Readme of directory python:

In this directory the whole python implementation is located.

# Start game
The start file to play Othello is **'main-game.py'**.
Dependencies:
    - numpy

# Analyse stored moves
To analyse the in 'ml_moves.csv' stored game statistic run **'analyse_ml.py**'
Dependencies:
    - numpy
    - termcolor
 
 # Other files

## constants.py
Often used constants are declared here.

## heuristics.py
Used in Alpha Beta pruning if neither machine learning or Monte Carlo is used.

## machine_learning.py
Contains util functions to use the database and get win probabilities.

## ml_database.py
Contains global instance of machine learning database

## ml_moves.csv
Database of played moves and wins of this moves ordered by fields and turn number.

## othello.py
Skeleton of Game Othello (print board, get available moves ..) without players

## start_moves.csv
Database of start moves

## start_tables.py	
Get available moves from start tables for given game.

## sum_csv.py
Add to ml_moves.csv files to one ml_moves.csv

## test_algo.sh
Bash script to play a specific player 20 times.

## util.py
util functions like integer or boolean selection
