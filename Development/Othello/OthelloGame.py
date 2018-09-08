import PlayerHuman
from Error import InvalidTurnError
from Error import PlayerInvalidError
from Player import Player


class OthelloGame:

    def __init__(self, boardsize=8):
        self._board = [[None for row in range(boardsize)] for column in range(boardsize)]
        self._player = []
        self._player_print_symbol = {0: "W", 1: "B"}
        self._turn_number = 0
        self._number_of_passes = 0

        self._set_initial_stones()

        self.print_board()

        for x in range(2):
            self.add_player()

        self.play()

    def _add_player(self, player):
        if isinstance(player, Player):
            self._player.append(player)
            print("Player Added")
        else:
            print(player)
            print(player.__class__)
            raise PlayerInvalidError("Tried to add unknown Type of Player")

    def add_player(self):
        player_to_add = None

        print(" 0: Human Player")
        selection = int(input("Please enter the number for the Player Type to add\n"))
        if selection == 0:
            player_to_add = PlayerHuman.PlayerHuman(self)

        self._add_player(player_to_add)

    def _set_initial_stones(self):
        pivot_pos = int(len(self._board) / 2)
        if len(self._board) % 2 == 0:
            self._board[pivot_pos - 1][pivot_pos - 1] = 0
            self._board[pivot_pos - 1][pivot_pos] = 1
            self._board[pivot_pos][pivot_pos - 1] = 1
            self._board[pivot_pos][pivot_pos] = 0
        else:
            self._board[pivot_pos - 1][pivot_pos - 1] = 0
            self._board[pivot_pos - 1][pivot_pos + 1] = 0
            self._board[pivot_pos + 1][pivot_pos - 1] = 0
            self._board[pivot_pos + 1][pivot_pos + 1] = 0
            self._board[pivot_pos - 1][pivot_pos] = 1
            self._board[pivot_pos + 1][pivot_pos] = 1
            self._board[pivot_pos][pivot_pos - 1] = 1
            self._board[pivot_pos][pivot_pos + 1] = 1

    def get_board(self):
        return self._board.copy()

    def get_available_moves(self):
        return_list = []
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                if self._board[row][column] is None:
                    return_list.append((column, row))
        return return_list

    def print_board(self):
        print("+" + len(self._board) * "---+")
        for row in range(len(self._board)):
            print("| ", end="")
            for column in range(len(self._board[row])):
                field_value = self._board[row][column]
                print((" " if field_value is None else self._player_print_symbol[field_value]) + " | ", end="")
            print("\n", end="")
            print("+" + len(self._board) * "---+")

    def play(self):
        while self._number_of_passes < 2:
            print(self.get_available_moves())
            if (len(self.get_available_moves())) > 0:
                self._player[self._turn_number % 2].play()
            else:
                self._number_of_passes +=1
                print(self._player_print_symbol[self._turn_number % 2] + "had to pass. "
                                                                         "There were no possible positions for her.")
            self.print_board()
        stats = self.get_stats()
        print(self._player_print_symbol[0] + " : " + str(stats[0])
              + " | " + self._player_print_symbol[1] + " : " + str(stats[1]))
        if max(stats) == stats[0]:
            print(self._player_print_symbol[0], end="")
        else:
            print(self._player_print_symbol[1], end="")
        print(" wins!")


    def get_stats(self):
        counter_a, counter_b = 0, 0
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                field_value = self._board[row][column]
                if field_value == 0:
                    counter_a += 1
                elif field_value == 1:
                    counter_b += 1
        return (counter_a, counter_b)


    def set_stone(self, x, y):
        if (x, y) in self.get_available_moves():
            self._board[x][y] = self._turn_number % 2
            self._turn_number += 1
        else:
            raise InvalidTurnError("The given Turn is not allowed!")
