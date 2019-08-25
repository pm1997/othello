import numpy as np
from termcolor import colored
from constants import COLUMN_NAMES, DATABASE_FILE_NAME, DATABASE_TO_POSITIONS


class Analyse:
    """
    calculate winning chance of given player with database and print the results
    """

    def __init__(self):
        """
        import csv file and store in self._database
        self._board_grid contains printable winning chances of board positions
        """
        csv = np.loadtxt(DATABASE_FILE_NAME, delimiter=';', dtype='int64')
        # _database contains 9 field categories and 3 value per category (wins player1, wins player2, total played games)
        self._database = csv.reshape((60, 9, 3))

        # _board_grid as percent of winning
        # will be printed in analyse(...)
        self._board_grid = np.zeros(shape=(60, 8, 8))

    def analyse(self, player=0):
        """
        analyse self._database
        store winning chances in self._board_grid and print it
        calculate maximum and standard deviation
        """
        for turn_nr in range(60):
            print(f"turn_nr: {turn_nr}")
            # field_category = 0
            for field_category in range(9):
                cell = self._database[turn_nr][field_category]
                moves = DATABASE_TO_POSITIONS[field_category]
                # calculate chance of winning
                if cell[2] == 0:
                    a = 0
                else:
                    a = cell[player] / cell[2] * 100

                for row, column in moves:
                    self._board_grid[turn_nr][row][column] = "{:.2f}".format(a)

            # calculate sum of array
            s1 = np.sum(self._board_grid[turn_nr])
            print(f"max: {np.max(self._board_grid[turn_nr])}")
            print(f"standard deviation: {np.std(self._board_grid[turn_nr], ddof=1)}")
            Analyse.print_board(self._board_grid[turn_nr], s1 / 64)

            print("_______________________")

    @staticmethod
    def print_board(board, average):
        """
        :param board: actual board matrix
        :param average: average value to color matrix
        :return: stdout of colored matrix
        """
        board_string = ''
        board_string += ''
        for i in range(8):
            board_string += f'      {COLUMN_NAMES[i]} '
        board_string += '\n'
        board_string += '  +' + 8 * '-------+' + '\n'
        for row in range(8):
            board_string += f'{row + 1} |'
            for col in range(8):
                if board[row][col] < average - 0.5:
                    board_string += colored('{: 6.2f}'.format(board[row][col]), 'red') + ' |'
                elif board[row][col] > average + 0.5:
                    board_string += colored('{: 6.2f}'.format(board[row][col]), 'green') + ' |'
                else:
                    board_string += colored('{: 6.2f}'.format(board[row][col]), 'blue') + ' |'
            board_string += '\n'
            board_string += '  +' + 8 * '-------+' + '\n'
        print(board_string)


an1 = Analyse()
print("Player 1:")
an1.analyse(0)
print("Player 2:")
an1.analyse(1)
