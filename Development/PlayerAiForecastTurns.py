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
        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        new_othello = OthelloGame(BOARD_SIZE, True)
        new_othello.set_board(self._game_reference.get_board().copy())
        new_othello._board[1][0] = 1
        new_othello.print_board()

        new_board = self._game_reference.get_board().copy()
        new_board[0][0] = 1
        self._game_reference.print_board()

        turn_nr = self._game_reference.get_turn_number()
        state = OthelloGame._compute_moves_and_stones_to_turn(new_board, turn_nr)
        print(state.board[1][0])
        self._game_reference.print_board()
        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)
