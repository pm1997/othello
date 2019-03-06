import copy
import numpy as np
import pandas as pd
from util import UtilMethods


class Othello:
    """Is the Othello Game class"""
    EMPTY_CELL = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    PRINT_SYMBOLS = {EMPTY_CELL: " ", PLAYER_ONE: "B", PLAYER_TWO: "W", None: "None"}
    COLUMN_NAMES = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

    DIRECTIONS = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

    _board = [[0 for _ in range(8)] for _ in range(8)]
    _current_player = None

    _last_turn_passed = False
    _game_is_over = False

    _fringe = set()
    _turning_stones = dict()
    _taken_moves = dict()
    _turn_nr = 0

    _start_tables = []

    def _init_start_tables(self):
        csv = pd.read_csv('start_moves.csv')
        self._start_tables = np.array(csv)
        # ########################################################
        # CAUTION: Call only once or on change of start tables ! #
        # #  self.calculate_missing_start_moves()                #
        # #########################################################

    def get_available_start_tables(self):
        if len(self._start_tables) == 0:
            self._init_start_tables()

        turn_nr = self.get_turn_nr()
        available_moves = []
        taken_mv = self.get_taken_mv()
        for game in self._start_tables:
            turn = 0
            same = True
            for move in game:
                if turn < turn_nr:
                    if taken_mv[turn] != move:
                        break
                else:  # turn == turn_nr
                    if same and move != "i8":
                        available_moves.append(move)
                        break
                    else:
                        break
                turn += 1
        return available_moves

    def calculate_missing_start_moves(self):
        """calculate the point symmetric moves of whole database"""
        if len(self._start_tables) == 0:
            self._init_start_tables()

        new_moves = list()
        header_length = len(self._start_tables[0])
        header = list()
        for i in range(header_length):
            header.append(str(i))
        new_moves.append(header)

        for game in self._start_tables:
            new_moves.append(self._calculate_opposite_move(game))
            new_moves.append(game)
        print(f"games:{new_moves}")
        with open('start_moves.csv', 'w') as f:
            for row in new_moves:
                csv_row = ""
                for turn in row:
                    if len(csv_row):
                        csv_row += "," + turn
                    else:
                        csv_row = turn
                f.write("%s\n" % csv_row)

    def _calculate_opposite_move(self, moves):
        """calculate the point symmetric moves of one given game"""
        new_turns = list()
        for move in moves:
            (row, column) = UtilMethods.translate_move_to_pair(move)
            if column < 8 and row < 7:
                row -= 7
                row = abs(row) % 7
                column -= 7
                column = abs(column) % 7
            new_turns.append(self.COLUMN_NAMES[column] + str(row + 1))
        print(f"old:{moves}")
        print(f"new:{new_turns}")
        return new_turns

    def deepcopy(self):
        copied_game = Othello()
        copied_game.init_copy(copy.deepcopy(self._board),
                              copy.deepcopy(self._current_player),
                              copy.deepcopy(self._last_turn_passed),
                              copy.deepcopy(self._game_is_over),
                              copy.deepcopy(self._fringe),
                              copy.deepcopy(self._turning_stones))
        return copied_game

    def print(self):
        print(f"OthelloGameState[{self}]:")
        print(4 * " " + "board: " + self._get_board_string().replace("\n", "\n" + 11 * " "))
        print(4 * " " + "current_player: " + self.PRINT_SYMBOLS[self._current_player])
        print(4 * " " + f"last_turn_passed: {self._last_turn_passed}")
        print(4 * " " + f"game_is_over: {self._game_is_over}")
        print(4 * " " + f"_fringe: {self._fringe}")
        print(4 * " " + f"_turning_stones: {self._turning_stones}")

    def init_copy(self, board, current_player, last_turn_passed, game_is_over, fringe, turning_stones):
        self._board = board
        self._current_player = current_player
        self._last_turn_passed = last_turn_passed
        self._game_is_over = game_is_over
        self._fringe = fringe
        self._turning_stones = turning_stones

    def init_game(self):
        self._board[3][3] = self.PLAYER_TWO
        self._board[4][4] = self.PLAYER_TWO
        self._board[3][4] = self.PLAYER_ONE
        self._board[4][3] = self.PLAYER_ONE

        self._update_fringe((3, 3))
        self._update_fringe((4, 4))
        self._update_fringe((3, 4))
        self._update_fringe((4, 3))

        self._current_player = self.PLAYER_ONE

        self._compute_available_moves()

    def game_is_over(self):
        return self._game_is_over

    def _get_board_string(self):
        board_string = ""
        board_string += "  "
        for i in range(8):
            board_string += f"  {self.COLUMN_NAMES[i]} "
        board_string += "\n"
        board_string += "  +" + 8 * "---+" + "\n"
        for row in range(8):
            board_string += f"{row+1} |"
            for col in range(8):
                board_string += f" {self.PRINT_SYMBOLS[self._board[row][col]]} |"
            board_string += "\n"
            board_string += "  +" + 8 * "---+" + "\n"
        return board_string

    def print_board(self):
        print(self._get_board_string())

    def get_current_player(self):
        if not self._game_is_over:
            return self._current_player
        else:
            return None

    def get_statistics(self):
        points_dict = {self.PLAYER_ONE: 0, self.PLAYER_TWO: 0, self.EMPTY_CELL: 0}
        for row in range(8):
            for col in range(8):
                points_dict[self._board[row][col]] += 1
        return points_dict

    def get_board(self):
        return copy.deepcopy(self._board)

    def get_turn_nr(self):
        return self._turn_nr

    def get_taken_mv(self):
        return copy.deepcopy(self._taken_moves)

    def get_winner(self):
        stats = self.get_statistics()
        if stats[self.PLAYER_ONE] == stats[self.PLAYER_TWO]:
            return None
        elif stats[self.PLAYER_ONE] > stats[self.PLAYER_TWO]:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def utility(self, player):
        winner = self.get_winner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

    @staticmethod
    def other_player(player):
        if player == Othello.PLAYER_ONE:
            return Othello.PLAYER_TWO
        elif player == Othello.PLAYER_TWO:
            return Othello.PLAYER_ONE
        else:
            return None

    def _next_player(self):
        if self._current_player == self.PLAYER_ONE:
            self._current_player = self.PLAYER_TWO
        elif self._current_player == self.PLAYER_TWO:
            self._current_player = self.PLAYER_ONE

    def _update_fringe(self, position):
        # (x, y) = position
        for direction in self.DIRECTIONS:
            next_step = Othello._next_step(position, direction)
            if next_step is not None:
                (new_x, new_y) = next_step
                if self._board[new_x][new_y] == self.EMPTY_CELL:
                    self._fringe.add(next_step)

    def _prepare_next_turn(self):
        self._next_player()
        self._compute_available_moves()

    @staticmethod
    def _next_step(position, direction):
        (y, x), (y_step, x_step) = position, direction
        new_position = (new_y, new_x) = (y + y_step, x + x_step)
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            return new_position
        else:
            return None

    def get_available_moves(self):
        return list(self._turning_stones.keys())

    def play_position(self, position):
        if position in self.get_available_moves():
            (row, column) = position
            current_symbol = self._current_player
            self._board[row][column] = current_symbol
            for (row2, column2) in self._turning_stones[position]:
                self._board[row2][column2] = current_symbol
            self._taken_moves[self._turn_nr] = self.COLUMN_NAMES[column] + str(row + 1)
            self._turn_nr += 1
            self._fringe.remove(position)
            self._update_fringe(position)
            self._prepare_next_turn()
            return True
        else:
            return False

    def _compute_available_moves(self):
        self._turning_stones = dict()
        own_symbol = self._current_player
        for current_position in self._fringe:
            position_turns = set()
            for direction in self.DIRECTIONS:
                next_step = Othello._next_step(current_position, direction)
                this_direction = set()
                while next_step is not None:
                    (current_x, current_y) = next_step
                    current_value = self._board[current_x][current_y]
                    if current_value == self.EMPTY_CELL:
                        break
                    elif current_value != own_symbol:
                        this_direction.add(next_step)
                    elif current_value == own_symbol:
                        if len(this_direction) > 0:
                            position_turns = position_turns | this_direction
                        break
                    next_step = Othello._next_step(next_step, direction)
            if len(position_turns) > 0:
                self._turning_stones[current_position] = position_turns
        if len(self._turning_stones) == 0:
            if self._last_turn_passed:
                self._game_is_over = True
            else:
                self._last_turn_passed = True
                self._prepare_next_turn()
        else:
            self._last_turn_passed = False
