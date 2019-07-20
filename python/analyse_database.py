import numpy as np
from termcolor import colored
from constants import COLUMN_NAMES, DATABASE_FILE_NAME, DATABASE_TO_POSITIONS


class Analyse:
    """
    calculate winning change of given player with database and print the results
    """

    def __init__(self):
        """
        import csv file and store in self._database
        self._board_grid contains printable winning changes of board positions
        """
        csv = np.loadtxt(DATABASE_FILE_NAME, delimiter=';', dtype='int64')
        # _database contains 9 field categories and 3 value each category (wins player1, wins player2, total played games)
        self._database = csv.reshape((60, 9, 3))

        # _board_grid as % of winning
        # will be printed in analyse(...)
        self._board_grid = np.zeros(shape=(60, 8, 8))

    def analyse(self, player=0):
        """
        analyse self._database
        store winning changes in self._board_grid and print it
        calculate maximum and standard deviation
        """
        for position in range(60):
            print(f"position: {position}")
            field_type = 0
            for cell in self._database[position]:
                moves = DATABASE_TO_POSITIONS[field_type]
                # calculate change of winning
                if cell[2] == 0:
                    a = 0
                else:
                    a = cell[player] / cell[2] * 100

                for row, column in moves:
                    self._board_grid[position][row][column] = "{:.2f}".format(a)
                field_type += 1

            # calculate sum of array
            s1 = np.sum(self._board_grid[position])
            print(f"max: {np.max(self._board_grid[position])}")
            print(f"standard deviation: {np.std(self._board_grid[position], ddof=1)}")
            Analyse.print_board(self._board_grid[position], s1 / 64)

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
