from Player import Player

class PlayerHuman(Player):
    def __init__(self, game_reference):
        self._game_reference = game_reference
        print("Created new Human Player")

    def play(self):
        possible_moves = list(self._game_reference.get_available_moves())
        valid_selection = 0
        while not valid_selection:
            print("Possible positions:")
            print("Coordinates are (row, column)")
            for i in range(len(possible_moves)):
                (x, y) = possible_moves[i]
                print(f"{i}: ({x+1}, {y+1})")

            try:
                user_input = int(input("Please enter the number of the position you want to play:\n"))
            except ValueError:
                print("Invalid selection! Please enter an Integer.")
                continue

            if 0 <= user_input < len(possible_moves):
                valid_selection = 1
            else:
                print("Invalid selection! Please enter one of the listed values.")

        self._game_reference.set_stone(possible_moves[user_input])
