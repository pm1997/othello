import constants


class Grid:
    board = [[0 for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
    actual_player = constants.PLAYER_ONE

    def grid_full(self):
        for row in range(0, constants.GRID_SIZE):
            for column in range(0, constants.GRID_SIZE):
                if self.board[row][column] == 0:
                    return False
        return True

    def other_player(self):
        if self.actual_player == constants.PLAYER_ONE:
            return constants.PLAYER_TWO
        return constants.PLAYER_ONE

    def reverse_cell(self, row, column):
        print("changed cell " + str(row) + " , " + str(column))
        self.board[row][column] = self.actual_player
