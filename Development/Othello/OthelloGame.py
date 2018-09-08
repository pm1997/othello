from Error import PlayerInvalidError
from Player import Player
class OthelloGame:

    def __init__(self, boardsize=8, numberofplayers=2):
        self._board = [[None for row in range(boardsize)] for column in range(boardsize)]
        self._player = []

        self.print_board()

        for x in range(numberofplayers):
            self.add_player()

    def _add_player(self, player):
        if isinstance(player, Player):
            self._player.append(player)
            print("Player Added")
        else:
            print(player.__class__)
            raise PlayerInvalidError("Tried to add unknown Type of Player")

    def add_player(self):
        player_to_add = None

        print(" 0: Human Player")
        selection = input("Please enter the number for the Player Type to add\n")
        if selection == 0:
            import PlayerHuman
            player_to_add = PlayerHuman()

        self._add_player(player_to_add)

    def print_board(self):
        print("+" + len(self._board) * "---+")
        for row in range(len(self._board)):
            print("| ", end="")
            for column in range(len(self._board[row])):
                field_value = self._board[row][column]
                print((" " if field_value is None else str(field_value)) + " | ", end="")
            print("\n", end="")
            print("+" + len(self._board) * "---+")
