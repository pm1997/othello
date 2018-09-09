from Player import Player
import random

class PlayerHuman(Player):
    def __init__(self, game_reference):
        self._game_reference = game_reference
        print("Created new Human Player")

    def play(self):
        possible_moves = list(self._game_reference.get_available_moves())
        print("Possible positions:")
        for i in range(len(possible_moves)):
            (x, y) = possible_moves[i]
            print(f"{i}: ({x+1}, {y+1})")

        user_input = int(input("Please enter the number of the position you want to play:\n"))

        self._game_reference.set_stone(possible_moves[user_input])
