import numpy as np
import math
from util import UtilMethods


class Database:
    _data = list()

    def init_database(self):
        csv = np.loadtxt('ml_moves.csv', delimiter=',')
        self._data = csv.reshape((17, 64, 2))

    #  ###################################################
    #  CAUTION: This will delete the learned factors! '  #
    #  ###################################################
    def _reset_database(self):
        """
        Reset stored played / won games
        """
        self._data = np.ones(shape=(17, 64, 2))
        self.store_database()

    def store_database(self):
        with open("ml_moves.csv", 'w') as outfile:
            for row in self._data:
                np.savetxt(outfile, row, fmt='%-7.0f', delimiter=',')

    @staticmethod
    def translate_move_to_array(move):
        """
        :param move: stored move like "a1"
        :return: position like (0,1)
        """
        (row, column) = move
        if row in {"a", "b", "c", "d", "e", "f", "g", "h", "i"}:
            column_names = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
            return 8 * column_names[row] + column_names - 1

        position = 8 * row + column
        return position

    def get_likelihood(self, move, turn_nr):
        """
        calculate chance of winning for given move and turn_number
        :param move: move in available_moves
        :param turn_nr: actual turn_number
        :return: chance of winning for given field
        """
        move2 = self.translate_move_to_array(move)
        chance1 = self._data[math.ceil(turn_nr / 4)][move2][0] / self._data[math.ceil(turn_nr / 4)][move2][1]
        chance2 = self._data[math.floor(turn_nr / 4)][move2][0] / self._data[math.ceil(turn_nr / 4)][move2][1]
        likelihood = (chance1 * (turn_nr % 4) + chance2 * (4 - turn_nr % 4)) / 4
        return likelihood

    def update_weights(self, turn_nr, move, won):
        self._data[math.ceil(turn_nr / 4)][move][0] += won
        self._data[math.ceil(turn_nr / 4)][move][1] += 1
        self._data[math.floor(turn_nr / 4)][move][0] += won
        self._data[math.floor(turn_nr / 4)][move][1] += 1

    def update_all_weights(self, moves, won):
        turn_nr = 0
        for move in moves:
            m1 = UtilMethods.translate_move_to_pair(moves[turn_nr])
            position = self.translate_move_to_array(m1)
            self.update_weights(turn_nr, position, won)
            turn_nr += 1
