from Player import Player
import random


class PlayerAiRandom(Player):
    def __init__(self, game_reference):
        self._game_reference = game_reference
        print("Created new Random AI Player")

    def play(self):
        possible_moves = list(self._game_reference.get_available_moves())
        rand_item = possible_moves[random.randrange(len(possible_moves))]

        self._game_reference.set_stone(rand_item)
