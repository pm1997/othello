from error import InvalidTurnError
from error import PlayerInvalidError
from error import OddBoardSizeError
from error import BoardToSmallError
from error import NonIntegerBoardSizeError
from error import ToManyPlayersError
from player import Player
from othelloGameUtilState import OthelloGameState
from constants import BOARD_SIZE
from constants import PLAYER_ONE
from constants import PLAYER_TWO
from constants import EMPTY_CELL
from constants import MAX_FORECAST
from constants import INVALID_CELL
from constants import MAX_THREADS
from time import time
import timeit

class OthelloGame:

    def __init__(self, board_size=BOARD_SIZE, test_mode=True):
        # input validation
        if not isinstance(board_size, int):
            raise NonIntegerBoardSizeError("Only integer board sizes allowed!")
        elif board_size % 2 != 0:
            raise OddBoardSizeError("No odd board sizes allowed!")
        elif board_size < 4:
            raise BoardToSmallError("Only boards larger than 3 allowed.")
        # create and init object parameter
        self._board = [[EMPTY_CELL for _ in range(board_size)] for _ in range(board_size)]
        self._player = []
        self._player_print_symbol = {0: "W", 1: "B"}
        self._player_time = {0: 0, 1: 0}
        self._start_time = 0
        self._turn_number = 0
        self._last_state_backup = OthelloGameState()
        self._number_of_passes = 0
        # welcome user
        if test_mode:
            return
        print("Welcome to Othello!")
        # initialize board
        self._set_initial_stones()
        # add the two players
        for x in range(2):
            self.add_player()
        # print the board for the first time
        OthelloGame.print_board(self._board, self._player_print_symbol)
        # start the game play
        t = time()
        self._play()
        diff_time = (time() * 1000 - t * 1000)
        print("duration in milli seconds: " + str(diff_time))
        print("duration in seconds: " + str(diff_time / 1000))
        print("duration in minutes: " + str(diff_time / (1000 * 60)))
        print("MAX_FORECAST = " + str(MAX_FORECAST))
        print("MAX_THREADS = " + str(MAX_THREADS))

    def set_turn_number(self, turn_number):
        self._turn_number = turn_number

    def get_turn_number(self):
        return self._turn_number

    def _add_player(self, player):
        if not isinstance(player, Player):
            print(player)
            print(player.__class__)
            raise PlayerInvalidError("Tried to add unknown Type of Player!")
        elif len(self._player) >= 2:
            raise ToManyPlayersError("Number of Players is not allowed to exceed 2!")
        else:
            self._player.append(player)
            print("Player Added")

    def set_board(self, board):
        self._board = board

    def add_player(self):
        player_to_add = None
        valid_selection = 0
        while not valid_selection:
            print("Available Players:")
            print(" 0: Human Player (Max)")
            print(" 1: AI Player - Random (Max)")
            print(" 2: AI Player - Most Inversions (Max)")
            print(" 3: AI Player - Forecast Turns (Patrick)")
            print(" 4: AI Player - Most Inversions - Improved (Max)")
            print(" 5: AI Player - Tree search (Max)")
            print(" 6: AI Player - Tree search multiprocessing (Max)")
            try:
                selection = int(input("Please enter the number for the Player Type to add\n"))
                valid_selection = 1
            except ValueError:
                print("Invalid selection! Please enter an integer.")
                continue
            if selection == 0:
                import playerHuman
                player_to_add = playerHuman.PlayerHuman(self)
            elif selection == 1:
                import playerAiRandom
                player_to_add = playerAiRandom.PlayerAiRandom(self)
            elif selection == 2:
                import playerAiInvertMost
                player_to_add = playerAiInvertMost.PlayerAiInvertMost(self)
            elif selection == 3:
                import playerAiForecastTurns
                player_to_add = playerAiForecastTurns.PlayerAiForecastTurns(self)
            elif selection == 4:
                import playerAiInvertMostImproved
                player_to_add = playerAiInvertMostImproved.PlayerAiInvertMostImpoved(self)
            elif selection == 5:
                import playerAiTreeSearch
                player_to_add = playerAiTreeSearch.PlayerAiTreeSearch(self)
            elif selection == 6:
                import playerAiTreeSearchMultiprocessing
                player_to_add = playerAiTreeSearchMultiprocessing.PlayerAiTreeSearch(self)
            else:
                valid_selection = 0
                print("Invalid selection! Please enter one of the values listed!")

        self._add_player(player_to_add)

    def _set_initial_stones(self):
        pivot_pos = int(len(self._board) / 2)
        self._board[pivot_pos - 1][pivot_pos - 1] = PLAYER_ONE
        self._board[pivot_pos - 1][pivot_pos] = PLAYER_TWO
        self._board[pivot_pos][pivot_pos - 1] = PLAYER_TWO
        self._board[pivot_pos][pivot_pos] = PLAYER_ONE

    @staticmethod
    def print_board(board, player_print_symbol):
        print("    ", end="")
        for i in range(len(board)):
            print(f" {i+1}  ", end="")
        print("\n", end="")
        print("   +" + len(board) * "---+")
        for row in range(len(board)):
            print(f" {row+1} | ", end="")
            for column in range(len(board[row])):
                field_value = board[row][column]
                print((" " if field_value == EMPTY_CELL else player_print_symbol[field_value]) + " | ", end="")
            print("\n", end="")
            print("   +" + len(board) * "---+")

    def _play(self):
        while self._number_of_passes < 2:
            current_player = self._turn_number % 2
            print(f"{self._player_print_symbol[current_player]}'s turn: " + str(self._player[current_player].__class__))
            if (len(self.get_available_moves())) > 0:
                self._player[current_player].play()
            else:
                self._number_of_passes += 1
                self._turn_number += 1
                print(self._player_print_symbol[current_player] + " had to pass. "
                                                                  "There were no possible positions for her.")
            OthelloGame.print_board(self._board, self._player_print_symbol)
        print("end of game")
        OthelloGame.print_stats(self._board, self._player_print_symbol)
        OthelloGame.print_winner(self._board, self._player_print_symbol)
        print(3 * "\n", end="")

    def game_ends(self):
        board_full = True  # whole board is full
        for row in self._board:
            if EMPTY_CELL in row:
                board_full = False
        if board_full:
            return True

        # check whether both player passes
        if (len(self.get_available_moves())) > 0:
            return False
        else:
            self._turn_number += 1
            if (len(self.get_available_moves())) > 0:
                return False
            else:
                return True

    @staticmethod
    def get_stats(board):
        points_dict = {0: 0, 1: 0}
        for row in range(len(board)):
            for column in range(len(board)):
                field_value = board[row][column]
                if field_value == 0:
                    points_dict[0] += 1
                elif field_value == 1:
                    points_dict[1] += 1
        return points_dict

    @staticmethod
    def print_stats(board, player_print_symbol):
        stats = OthelloGame.get_stats(board)
        print("Statistics:")
        for player_no in stats:
            print(f"{player_print_symbol[player_no]}: {stats[player_no]}")

    @staticmethod
    def get_winner(board):
        stats = OthelloGame.get_stats(board)
        points_player_one = stats[0]
        points_player_two = stats[1]
        if points_player_one == points_player_two:
            return None
        elif points_player_one > points_player_two:
            return (0, points_player_one)
        else:
            return (1, points_player_two)

    @staticmethod
    def print_winner(board, player_print_symbol):
        winner = OthelloGame.get_winner(board)
        if winner is not None:
            (player, points) = winner
            print(f"{player_print_symbol[player]} wins with {points} points!")
        else:
            print("There is no winner. It is a draw!\nWhy don't you play again to settle the matter?")

    def print_timing(self):
        print("Computation time needed:")
        for player_no in self._player_time:
            print(f"{self._player_print_symbol[player_no]}: {self._player_time[player_no]}")

    def set_stone(self, position_pair, ai=False):
        stop = timeit.default_timer()
        if position_pair in self.get_available_moves():
            (x, y) = position_pair
            if not ai:
                time_diff = stop - self._start_time
                self._player_time[self._turn_number % 2] += time_diff
                print("It took " + str(time_diff) + " to calculate this move.")
                print(f"Stone is set to ({x+1}, {y+1})")
            self._board[int(x)][y] = self._turn_number % 2
            for stone_to_turn in self.get_stones_to_turn()[position_pair]:
                (turn_x, turn_y) = stone_to_turn
                self._board[int(turn_x)][turn_y] = self._turn_number % 2
            self._turn_number += 1
        elif position_pair == INVALID_CELL:
            self._turn_number += 1
        else:
            print(f"{self._player_print_symbol[self.get_turn_number() % 2]}'s turn")
            OthelloGame.print_board(self)
            raise InvalidTurnError("The given Turn is not allowed!" + str(position_pair[0]) + "  " + str(position_pair[1]))

    @staticmethod
    def set_stone_static(board, turn_number, position_pair):
        calculated_game_state = OthelloGame._compute_moves_and_stones_to_turn(board, turn_number)
        if position_pair in calculated_game_state.available_moves:
            (x, y) = position_pair
            board[x][y] = turn_number % 2
            for stone_to_turn in calculated_game_state.stones_to_turn[position_pair]:
                (turn_x, turn_y) = stone_to_turn
                board[int(turn_x)][turn_y] = turn_number % 2
        else:
            raise InvalidTurnError("The given Turn is not allowed!")

    @staticmethod
    def next_step(position_pair, direction_pair, board_size):
        (x, y), (x_step, y_step) = position_pair, direction_pair
        new_position = (new_x, new_y) = (x + x_step, y + y_step)
        if 0 <= new_x < board_size and 0 <= new_y < board_size:
            return new_position
        else:
            return None

    @staticmethod
    def get_neighbors(position, board):
        neighbors = set()
        directions = OthelloGame.get_directions()
        for direction in directions:
            next_step = OthelloGame.next_step(position, direction, len(board))
            if next_step is not None:
                neighbors.add(next_step)
        return neighbors

    @staticmethod
    def get_number_of_occupied_neighbors(position, board):
        number_of_occupied_neighbors = 0
        for (x, y) in OthelloGame.get_neighbors(position, board):
            if board[x][y] != EMPTY_CELL:
                number_of_occupied_neighbors += 1
        return number_of_occupied_neighbors

    @staticmethod
    def get_directions():
        return [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) not in [(0, 0)]]

    @staticmethod
    def get_positions_to_test(board):
        positions_to_test = set()
        for row in range(len(board)):
            for column in range(len(board[row])):
                current_position = (row, column)
                if board[row][column] == EMPTY_CELL \
                        and OthelloGame.get_number_of_occupied_neighbors(current_position, board) > 0:
                    positions_to_test.add(current_position)
        return positions_to_test

    @staticmethod
    def _compute_moves_and_stones_to_turn(board, turn_number, number_of_passes=0):
        available_moves = set()
        stones_to_turn = dict()
        directions = OthelloGame.get_directions()
        own_symbol = turn_number % 2
        for current_position in OthelloGame.get_positions_to_test(board):
            # print("working on: " + str(current_position))
            this_position_turns = set()
            for direction in directions:
                # print("    working on direction: " + str(direction))
                next_position = OthelloGame.next_step(current_position, direction, len(board))
                stones_in_this_direction = set()
                while next_position is not None:
                    new_current_position = (current_x, current_y) = next_position
                    current_value = board[current_x][current_y]
                    if current_value == EMPTY_CELL:
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
                    next_position = OthelloGame.next_step(new_current_position, direction, len(board))
            if len(this_position_turns) > 0:
                available_moves.add(current_position)
                stones_to_turn[current_position] = this_position_turns
                # print("  position turns " + str(this_position_turns))
            # else:
            #     print("  no turns for this position")
        return OthelloGameState(turn_number, number_of_passes, board, available_moves, stones_to_turn)

    def get_available_moves(self):
        if self._turn_number != self._last_state_backup.turn_number:
            self._last_state_backup = OthelloGame._compute_moves_and_stones_to_turn(self._board.copy(),
                                                                                    int(self._turn_number))
        return self._last_state_backup.available_moves

    def get_board(self):
        return self._board.copy()

    def get_stones_to_turn(self):
        if self._turn_number != self._last_state_backup.turn_number:
            self._last_state_backup = OthelloGame._compute_moves_and_stones_to_turn(self._board.copy(),
                                                                                    int(self._turn_number))
        return self._last_state_backup.stones_to_turn

    def get_game_info(self):
        if self._turn_number != self._last_state_backup.turn_number:
            self._last_state_backup = OthelloGame._compute_moves_and_stones_to_turn(self._board.copy(),
                                                                                    int(self._turn_number))
        return self._last_state_backup.copy_state()

    @staticmethod
    def copy_board(old_board):
        new_board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                new_board[row][column] = old_board[row][column]
        return new_board
