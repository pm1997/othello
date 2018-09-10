from Player import Player
from operator import itemgetter
from OthelloGame import OthelloGame
from Constants import BOARD_SIZE


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        print("Created new Forecast Turns AI Player")

    def play(self):

        new_othello = OthelloGame(BOARD_SIZE, True)
        old_board = self._game_reference.get_board()
        new_board = OthelloGame.copy_board(old_board)
        new_board[0][0] = 0
        new_othello.set_board(new_board)

        print("old board:")
        self._game_reference.print_board()

        print("new instance:")
        new_othello.print_board()

        # old code

        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)



