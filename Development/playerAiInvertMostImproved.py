from player import Player
from operator import itemgetter
from random import shuffle


class PlayerAiInvertMostImpoved(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        print("Created new Invert AI Player - Most Turns (Improved)")

    def play(self):
        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        # The max function will always return the first maximum value encountered
        # Shuffle the list to avoid to be predictable.
        shuffle(number_inversions)

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)
