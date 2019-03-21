import numpy as np
import math


class MachineDatabase:
    # data of csv ml_moves.csv
    _data = list()

    def init_database(self):
        # load csv in self_data as 3 dim. array
        csv = np.loadtxt('ml_moves.csv', delimiter=',')
        self._data = csv.reshape((17, 64, 2))

    #  ###################################################
    #  CAUTION: This will delete the learned factors! '  #
    #  ###################################################
    def _reset_database(self):
        """
        Reset stored played / won games
        """
        # write 1.0 in each cell of _data array
        self._data = np.ones(shape=(17, 64, 2))
        # save modified array
        self.store_database()

    def store_database(self):
        """
        store database on filesystem
        :return:
        """
        with open("ml_moves.csv", 'w') as outfile:
            # write 3 dim. array as list of 2 dim. array's
            for row in self._data:
                # write one row of matrix
                np.savetxt(outfile, row, fmt='%-7.0f', delimiter=',')

    @staticmethod
    def translate_move_to_array(move):
        """
        :param move: stored move like "a1"
        :return: position like (0,1)
        """
        (row, column) = move
        # move is either like "a2" or (0,1)
        if row in {"a", "b", "c", "d", "e", "f", "g", "h", "i"}:
            # if move is like "a1" translate char to int
            column_names = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
            # calculate position in matrix
            return 8 * column_names[row] + column - 1

        # calculate position in matrix
        # row 1 column 1 column 2 .. column 8
        # row 2    ..       ..          ..
        # row 3    ..       ..          ..
        # ...      ..       ..          ..
        # row 8    ..       ..          ..
        position = 8 * row + column
        return position

    def get_likelihood(self, move, turn_nr):
        """
        calculate chance of winning for given move and turn_number
        :param move: move in available_moves
        :param turn_nr: actual turn_number
        :return: chance of winning for given field
        """
        # translate move to position in array
        position = self.translate_move_to_array(move)
        # get chances of winning of turn number
        # eg: turn_number = 5
        #       => look in row 1  (5 / 4).floor()
        #       => look in row 2  (5 / 4).ceil()
        chance1 = self._data[math.ceil(turn_nr / 4)][position][0] / self._data[math.ceil(turn_nr / 4)][position][1]
        chance2 = self._data[math.floor(turn_nr / 4)][position][0] / self._data[math.ceil(turn_nr / 4)][position][1]
        # add chances together
        likelihood = (chance1 * (turn_nr % 4) + chance2 * (4 - turn_nr % 4)) / 4
        return likelihood

    def update_weights(self, turn_nr, move, won):
        """
        :param turn_nr: actual turn number
        :param move:  move of turn number
        :param won: game won ? 1 : 0
        :return:
        """
        # update number of won and turns in last move
        # eg: turn_number = 5
        #       => update row 1  (5 / 4).floor()
        #       => update row 2  (5 / 4).ceil()
        self._data[math.ceil(turn_nr / 4)][move][0] += won
        self._data[math.ceil(turn_nr / 4)][move][1] += 1

        self._data[math.floor(turn_nr / 4)][move][0] += won
        self._data[math.floor(turn_nr / 4)][move][1] += 1

    def update_all_weights(self, moves, won):
        """
        update weights of all moves in game
        :param moves: list of taken moves
        :param won: game won ? 1 : 0
        :return:
        """
        turn_nr = 0
        # update each move in game
        for _ in moves:
            # translate move 1,0 to position 8
            position = self.translate_move_to_array(moves[turn_nr])
            # update array at position position
            self.update_weights(turn_nr, position, won)
            # update next move
            turn_nr += 1
