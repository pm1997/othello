import numpy as np
import math


class Database:
    _data = list()

    def init_database(self):
        csv = np.loadtxt('ml_moves.csv', delimiter=',')
        self._data = csv.reshape((17, 64, 2))
        print(self._data)
        print(len(self._data))

    #  ###################################################
    #  CAUTION: This will delete the learned factors! '  #
    #  ###################################################
    @staticmethod
    def _reset_database():
        data = np.zeros(shape=(17, 64, 2))

        with open("ml_moves.csv", 'w') as outfile:
            for row in data:
                np.savetxt(outfile, row, fmt='%-7.0f', delimiter=',')

    @staticmethod
    def translate_move_to_array(move):
        column_names = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        (row, column) = move
        position = 8 * row + column_names[column]
        return position

    def get_likelihood(self, move, turn_nr):
        chance1 = self._data[math.ceil(turn_nr / 4)][move]
        chance2 = self._data[math.floor(turn_nr / 4)][move]
        likelihood = (chance1 * (turn_nr % 4) + chance2 * (4 - turn_nr % 4)) / 4
        return likelihood
