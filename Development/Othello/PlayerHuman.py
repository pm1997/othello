from Player import Player
import random

class PlayerHuman(Player):
    def __init__(self, game_reference):
        self._game_reference = game_reference
        print("Created new Player")

    def play(self):
        possible_moves = self._game_reference.get_available_moves()
        rand_item = possible_moves[random.randrange(len(possible_moves))]
        (x, y) = rand_item

        print("Playing " + str(rand_item))
        self._game_reference.set_stone(x,y)
