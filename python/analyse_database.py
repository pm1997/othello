import numpy as np
from termcolor import colored
from constants import COLUMN_NAMES, DATABASE_FILE_NAME
from database import Database


class Analyse:

    def __init__(self):
        """
        import csv file and store in self._data
        """
        csv = np.loadtxt(DATABASE_FILE_NAME, delimiter=';', dtype='int64')
        self._data = csv.reshape((60, 9, 3))

        # data as % of winning
        self._data2 = np.zeros(shape=(60, 8, 8))

    def analyse(self, player=0):
        """
        analyse self._data
        get highest probability of winning per turn row
        """
        for position in range(60):
            print(f"position: {position}")
            field_type = 0
            for cell in self._data[position]:
                moves = Database.translate_database_to_positions(field_type)
                # calculate change of winning
                if cell[2] == 0:
                    a = 0
                else:
                    a = cell[player] / cell[2] * 100

                for field in moves:
                    self._data2[position][field[0]][field[1]] = "{:.2f}".format(a)
                # print(a)
                field_type += 1

            # calculate first sum of array
            s1 = np.sum(self._data2[position])
            print(f"max: {np.max(self._data2[position])}")
            field_type = 0
            for cell in self._data[position]:

                # set unused moves to 100 %
                if cell[2] == 0:
                    a = 0
                    moves = Database.translate_database_to_positions(field_type)
                    for field in moves:
                        self._data2[position][field[0]][field[1]] = "{:.2f}".format(a)
                field_type += 1
            print(f"min: {np.min(self._data2[position])}")

            # calculate second sum of array
            s2 = np.sum(self._data2[position])
            # with both arrays, the error in average through unused moves (number of turns == 1), should be minimized
            average = (s1 + s2) / 128
            print(f"average: {average}")

            field_type = 0
            for cell in self._data[position]:
                # set unused moves to average value to minimize error in variance
                if cell[2] == 0:
                    moves = Database.translate_database_to_positions(field_type)
                    for field in moves:
                        self._data2[position][field[0]][field[1]] = "{:.2f}".format(0)
                field_type += 1
            print(f"usual difference: {np.sqrt(np.var(self._data2[position], ddof=1))}")

            # print array (board without column /
            Analyse.print_board(self._data2[position], average)
            # print(self._data2[pos])

            print("_______________________")

    @staticmethod
    def print_board(board, average):
        """
        :param board: actual board matrix
        :param average: average value to color matrix
        :return: stdout of colored matrix
        """
        board_string = ""
        board_string += ""
        for i in range(8):
            board_string += f"      {COLUMN_NAMES[i]} "
        board_string += "\n"
        board_string += "  +" + 8 * "-------+" + "\n"
        for row in range(8):
            board_string += f"{row + 1} |"
            for col in range(8):
                if board[row][col] < average - 0.5:
                    board_string += f" {colored(board[row][col], 'red')} |"
                elif board[row][col] > average + 0.5:
                    board_string += f" {colored(board[row][col], 'green')} |"
                else:
                    board_string += f" {board[row][col]} |"
            board_string += "\n"
            board_string += "  +" + 8 * "-------+" + "\n"
        print(board_string)


an1 = Analyse()
# an1.init()
print("Player 1:")
an1.analyse(0)
print("Player 2:")
an1.analyse(1)
