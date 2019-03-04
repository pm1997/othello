from player import Player

from constants import BOARD_SIZE
from constants import INVALID_CELL
from constants import MAX_CARLO_ITERATIONS

from utilMonteCarloTree import UtilMonteCarloTree


class PlayerAiRandomSearch(Player):

    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        self.tree = UtilMonteCarloTree(game_reference.get_game_info().turn_number, BOARD_SIZE, INVALID_CELL[0],
                                       INVALID_CELL[1], game_reference.get_game_info(), None)
        print("Created new Monte Carlo AI Player")

    def play(self):
        state = self._game_reference.get_game_info()
        #  turn_number, size=BOARD_SIZE, row=INVALID_CELL[0], column=INVALID_CELL[1], game_state=None, parent=None
        tree = UtilMonteCarloTree(state.turn_number, BOARD_SIZE, INVALID_CELL[0], INVALID_CELL[1], state, None)
        tree.monte_carlo(MAX_CARLO_ITERATIONS)
        # print(str(tree))

        best = tree.get_best_move(state.turn_number % 2)
        self._game_reference.set_stone(best)
