import numpy as np
import pandas as pd
from util import UtilMethods
from othello import Othello
from constants import COLUMN_NAMES


class StartTables:
    _start_tables = []

    def _init_start_tables(self):
        """
        read start tables from csv file 'start_moves.csv'
        and store them in _start_tables
        """
        csv = pd.read_csv('start_moves.csv')
        self._start_tables = np.array(csv, dtype="str")
        # print(self._start_tables)
        # ########################################################
        # CAUTION: Call only once or on change of start tables ! #
        # #  self.calculate_missing_start_moves()                #
        # #########################################################

    def get_available_moves_of_start_tables(self, game: Othello):
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
                    if move != "i8" or move != "nan":  # i8 = invalid field
                        available_moves.append(move)
                    break
                turn += 1
        available_moves = list(dict.fromkeys(available_moves))
        if "nan" in available_moves:
            available_moves.remove("nan")
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
            # ---------------------------------------------------------
            # | WARNING: Only call each method once !!!               |
            # ---------------------------------------------------------
            # | new_moves.append(self.calculate_opposite_move(game))  |
            # | new_moves.append(self.calculate_diagonal_moves(game)) |
            # ---------------------------------------------------------
            new_moves.append(game)

        # new_moves = self.remove_duplicates(new_moves)
        # store new start table in file 'start_moves.csv'
        with open('start_moves.csv', 'w') as f:
            for row in new_moves:
                csv_row = ""
                for turn in row:
                    if turn == "nan":
                        break
                    if len(csv_row):
                        csv_row += "," + turn
                    else:
                        csv_row = turn
                f.write("%s\n" % csv_row)

    @staticmethod
    def calculate_opposite_move(moves):
        """calculate the point symmetric moves of one given game"""
        new_turns = list()
        for move in moves:
            if move[0] not in {"a", "b", "c", "d", "e", "f", "g", "h"}:
                break
            # move is a char and a int , eg. 'd3'
            # translate this move to a x and y coordinate
            (row, column) = UtilMethods.translate_move_to_pair(move)
            if column < 8 and row < 7:
                # mirror row and column at point 3.5,3.5 => middle of board
                row -= 7
                row = abs(row) % 7
                column -= 7
                column = abs(column) % 7
            new_turns.append(COLUMN_NAMES[column] + str(row + 1))
        print(f"old:{moves}")
        print(f"new:{new_turns}")
        return new_turns

    @staticmethod
    def calculate_diagonal_moves(moves):
        """calculate the point symmetric moves of one given game"""
        new_turns = list()
        for move in moves:
            if move[0] not in {"a", "b", "c", "d", "e", "f", "g", "h"}:
                break
            # move is a char and a int , eg. 'd3'
            # translate this move to a x and y coordinate
            (row, column) = UtilMethods.translate_move_to_pair(move)
            if column < 8 and row < 7:
                # mirror row and column at diagonal 0,0; 7,7 => middle of board
                row_temp = row
                row = column
                column = row_temp
            new_turns.append(COLUMN_NAMES[column] + str(row + 1))
        print(f"old:{moves}")
        print(f"new:{new_turns}")
        return new_turns
