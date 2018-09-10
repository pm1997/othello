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

    def cells_of_player(self, player):
        count = 0
        for row in range(0, constants.GRID_SIZE):
            for column in range(0, constants.GRID_SIZE):
                if self.board[row][column] == player:
                    count += 1
        return count

    def get_winner(self):
        player1 = 0
        player2 = 0
        for row in range(0, constants.GRID_SIZE):
            for column in range(0, constants.GRID_SIZE):
                if self.board[row][column] == constants.PLAYER_ONE:
                    player1 += 1
                elif self.board[row][column] == constants.PLAYER_TWO:
                    player2 += 1
        if player1 > player2:
            return constants.PLAYER_ONE, player1, player2
        return constants.PLAYER_TWO, player2, player1

    def game_finished(self):
        [winner, p1, p2] = self.get_winner()
        if winner == constants.PLAYER_ONE:
            print("Player 1 wins: " + str(p1) + " : " + str(p2))
        else:
            print("Player 2 wins: " + str(p1) + " : " + str(p2))
