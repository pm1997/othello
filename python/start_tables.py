import numpy as np
import pandas as pd
from util import UtilMethods
from othello import Othello


class StartTables:
    _start_tables = []

    def _init_start_tables(self):
        """
        read start tables from csv file 'start_moves.csv'
        and store them in _start_tables
        """
        csv = pd.read_csv('start_moves.csv')
        self._start_tables = np.array(csv)
        # ########################################################
        # CAUTION: Call only once or on change of start tables ! #
        # #  self.calculate_missing_start_moves()                #
        # #########################################################

    def get_available_start_tables(self, game: Othello):
        """
        search moves with identical game tree and get next element of these start table game tree
        :return: list of available moves
        """
        if len(self._start_tables) == 0:
            self._init_start_tables()

        turn_nr = game.get_turn_nr()
        available_moves = []
        taken_mv = game.get_taken_mvs_text()
        for game in self._start_tables:
            turn = 0
            for move in game:
                # move was played
                if turn < turn_nr:
                    if taken_mv[turn] != move:
                        # move is different to start_table
                        break
                else:  # turn == turn_nr
                    # if start sequence is finished and shorter than longest sequence the gab is filled with "i8" fields
                    if move != "i8":  # i8 = invalid field
                        available_moves.append(move)
                        break
                    else:
                        break
                turn += 1
        return available_moves

    def calculate_missing_start_moves(self):
        """calculate the point symmetric moves of whole database"""
        if len(self._start_tables) == 0:
            self._init_start_tables()

        new_moves = list()

        # add first row in new start table
        # first row == header = 0,1,2, ..
        header_length = len(self._start_tables[0])
        header = list()
        for i in range(header_length):
            header.append(str(i))
        new_moves.append(header)

        # calculate for all start sequences in start table
        for game in self._start_tables:
            # add move and opposite move to new start table
            new_moves.append(UtilMethods.calculate_opposite_move(game))
            new_moves.append(game)

        # store new start table in file 'start_moves.csv'
        with open('start_moves.csv', 'w') as f:
            for row in new_moves:
                csv_row = ""
                for turn in row:
                    if len(csv_row):
                        csv_row += "," + turn
                    else:
                        csv_row = turn
                f.write("%s\n" % csv_row)
