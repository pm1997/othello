from player import Player
from operator import itemgetter


class PlayerAiInvertMost(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        print("Created new Invert AI Player - Most Turns")

    def play(self):
        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)
