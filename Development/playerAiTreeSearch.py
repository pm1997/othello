from player import Player

from constants import MAX_FORECAST

from utilTreeTreeSearch import UtilTreeTreeSearch


class PlayerAiTreeSearch(Player):

    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        print("Created new Invert AI Player - Tree search")

    def play(self):
        state = self._game_reference.get_game_info()
        tree = UtilTreeTreeSearch(state.turn_number % 2, state, None, MAX_FORECAST)

        # print(str(tree))

        best = tree.get_best_decision()
        self._game_reference.set_stone(best)
