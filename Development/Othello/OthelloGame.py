from Error import InvalidTurnError
from Error import PlayerInvalidError
from Error import OddBoardSizeError
from Error import BoardToSmallError
from Error import NonIntegerBoardSizeError
from Player import Player


class OthelloGame:

    def __init__(self, boardsize=8):
        if not isinstance(boardsize, int):
            raise NonIntegerBoardSizeError("Only integer board sizes allowed!")
        elif boardsize % 2 != 0:
            raise OddBoardSizeError("No odd board sizes allowed!")
        elif boardsize < 4:
            raise BoardToSmallError("Only boards larger than 3 allowed.")

        self._board = [[None for row in range(boardsize)] for column in range(boardsize)]
        self._player = []
        self._player_print_symbol = {0: "W", 1: "B"}
        self._turn_number = 0
        self._number_of_passes = 0
        self._stones_to_turn = dict()

        print("Welcome to Othello!")

        self._set_initial_stones()

        for x in range(2):
            self.add_player()

        self.print_board()

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
        print("Avaliable Players:")
        print(" 0: Human Player")
        print(" 1: Random AI")
        selection = int(input("Please enter the number for the Player Type to add\n"))
        if selection == 0:
            import PlayerHuman
            player_to_add = PlayerHuman.PlayerHuman(self)
        elif selection == 1:
            import PlayerAiRandom
            player_to_add = PlayerAiRandom.PlayerAiRandom(self)

        self._add_player(player_to_add)

    def _set_initial_stones(self):
        pivot_pos = int(len(self._board) / 2)
        self._board[pivot_pos - 1][pivot_pos - 1] = 0
        self._board[pivot_pos - 1][pivot_pos] = 1
        self._board[pivot_pos][pivot_pos - 1] = 1
        self._board[pivot_pos][pivot_pos] = 0

    def get_board(self):
        return self._board.copy()

    # def _get_available_moves(self):
    #     return_list = []
    #     for row in range(len(self._board)):
    #         for column in range(len(self._board[row])):
    #             if self._board[row][column] is None:
    #                 return_list.append((row, column))
    #     return return_list

    def print_board(self):
        print("    ", end="")
        for i in range(len(self._board)):
            print(f" {i+1}  ", end="")
        print("\n", end="")
        print("   +" + len(self._board) * "---+")
        for row in range(len(self._board)):
            print(f" {row+1} | ", end="")
            for column in range(len(self._board[row])):
                field_value = self._board[row][column]
                print((" " if field_value is None else self._player_print_symbol[field_value]) + " | ", end="")
            print("\n", end="")
            print("   +" + len(self._board) * "---+")

    def play(self):
        while self._number_of_passes < 2:
            current_player = self._turn_number % 2
            print(f"{self._player_print_symbol[current_player]}'s turn")
            if (len(self.get_available_moves())) > 0:
                self._player[current_player].play()
            else:
                self._number_of_passes += 1
                self._turn_number += 1
                print(self._player_print_symbol[current_player] + " had to pass. "
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

    def set_stone(self, position_pair):
        if position_pair in self.get_available_moves():
            (x, y) = position_pair
            self._board[x][y] = self._turn_number % 2
            for stone_to_turn in self._stones_to_turn[position_pair]:
                (turn_x, turn_y) = stone_to_turn
                self._board[turn_x][turn_y] = self._turn_number % 2
            self._turn_number += 1
        else:
            raise InvalidTurnError("The given Turn is not allowed!")

    def _next_step(self, position_pair, direction_pair):
        board_size = len(self._board)
        (x, y), (x_step, y_step) = position_pair, direction_pair
        new_position = (new_x, new_y) = (x + x_step, y + y_step)
        if 0 <= new_x < board_size and 0 <= new_y < board_size:
            return new_position
        else:
            return None

    def get_neighbors(self, position):
        neighbors = set()
        directions = OthelloGame.get_directions()
        for direction in directions:
            next_step = self._next_step(position, direction)
            if next_step is not None:
                neighbors.add(next_step)
        return neighbors

    def get_number_of_occupied_neighbors(self, position):
        number_of_occupied_neighbors = 0
        for (x, y) in self.get_neighbors(position):
            if self._board[x][y] is not None:
                number_of_occupied_neighbors += 1
        return number_of_occupied_neighbors

    @staticmethod
    def get_directions():
        return [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) not in [(0, 0)]]

    def get_positions_to_test(self):
        positions_to_test = set()
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                current_position = (row, column)
                if self._board[row][column] is None and self.get_number_of_occupied_neighbors(current_position) > 0:
                    positions_to_test.add(current_position)
        return positions_to_test

    def get_available_moves(self):
        available_moves = set()
        stones_to_turn = dict()
        directions = OthelloGame.get_directions()
        own_symbol = self._turn_number % 2
        for current_position in self.get_positions_to_test():
            # print("working on: " + str(current_position))
            this_position_turns = set()
            for direction in directions:
                # print("    working on direction: " + str(direction))
                next_position = self._next_step(current_position, direction)
                stones_in_this_direction = set()
                while next_position is not None:
                    new_current_position = (current_x, current_y) = next_position
                    current_value = self._board[current_x][current_y]
                    if current_value is None:
                        # print("        encountered empty neighbor")
                        break
                    elif current_value != own_symbol:
                        # print("        encountered opponents stone")
                        stones_in_this_direction.add(new_current_position)
                    elif current_value == own_symbol:
                        # print("        encountered own stone")
                        this_position_turns.update(stones_in_this_direction)
                        # print("            " + str(stones_in_this_direction))
                        # print("            this_position_turns: " + str(this_position_turns))
                        break
                    next_position = self._next_step(new_current_position, direction)
            if len(this_position_turns) > 0:
                available_moves.add(current_position)
                stones_to_turn[current_position] = this_position_turns
                # print("  position turns " + str(this_position_turns))
            # else:
            #     print("  no turns for this position")
        self._stones_to_turn = stones_to_turn
        return available_moves
