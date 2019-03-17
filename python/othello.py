"""
File contains the "Othello" Data structure representing one State in a Game of Othello.
Functions to calculate available moves, make moves, etc. are included as well.
"""

import copy
from constants import PRINT_SYMBOLS, COLUMN_NAMES, EMPTY_CELL, DIRECTIONS, PLAYER_ONE, PLAYER_TWO


class Othello:
    """
    Data structure representing one state in a Game of Othello.
    Contains functions to calculate available moves, etc. as well
    """

    # Representation of the board. A list of Lists 
    _board = [[0 for _ in range(8)] for _ in range(8)]
    # Stores the player who's turn it is in the current state
    _current_player = None

    # Stores whether the last player had to pass. Used to determine the end of the game. 
    _last_turn_passed = False
    # Is set to 'True' once the Game is finished.
    _game_is_over = False

    # Store all fields next to the ones already taken.
    _fringe = set()
    # Stores legal moves as key and the set of the stones turned after making that move as value
    _turning_stones = dict()
    _taken_moves = dict()
    _turn_nr = 0

    def deepcopy(self):
        """
        Returns a deepcopy of the game.
        copy.deepcopy(self) does not work properly because the rows in the boards won't be copied.
        """
        copied_game = Othello()
        copied_game.init_copy(copy.deepcopy(self._board),
                              copy.deepcopy(self._current_player),
                              copy.deepcopy(self._last_turn_passed),
                              copy.deepcopy(self._game_is_over),
                              copy.deepcopy(self._fringe),
                              copy.deepcopy(self._turning_stones))
        return copied_game

    def print(self):
        """
        Used to print one Othello-Object
        """
        print(f"OthelloGameState[{self}]:")
        print(4 * " " + "board: " + self._get_board_string().replace("\n", "\n" + 11 * " "))
        print(4 * " " + "current_player: " + PRINT_SYMBOLS[self._current_player])
        print(4 * " " + f"last_turn_passed: {self._last_turn_passed}")
        print(4 * " " + f"game_is_over: {self._game_is_over}")
        print(4 * " " + f"_fringe: {self._fringe}")
        print(4 * " " + f"_turning_stones: {self._turning_stones}")

    def init_copy(self, board, current_player, last_turn_passed, game_is_over, fringe, turning_stones):
        """
        Used to initialize a copied game with the provided values
        """
        self._board = board
        self._current_player = current_player
        self._last_turn_passed = last_turn_passed
        self._game_is_over = game_is_over
        self._fringe = fringe
        self._turning_stones = turning_stones

    def init_game(self):
        """
        Initializes a new game
        """

        # Set the stones already on the board prior to the first move
        self._board[3][3] = PLAYER_TWO
        self._board[4][4] = PLAYER_TWO
        self._board[3][4] = PLAYER_ONE
        self._board[4][3] = PLAYER_ONE

        # Add the fields next to these fields to the fringe.
        self._update_fringe((3, 3))
        self._update_fringe((4, 4))
        self._update_fringe((3, 4))
        self._update_fringe((4, 3))

        # Set the current player to the first player
        self._current_player = PLAYER_ONE

        # Compute the legal moves during the first turn
        self._compute_available_moves()

    def game_is_over(self):
        """
        Return whether the game is still active or already over
        """
        return self._game_is_over

    def _get_board_string(self):
        """
        Return a string representing the current state of the board
        """
        board_string = ""
        board_string += "  "
        for i in range(8):
            board_string += f"  {COLUMN_NAMES[i]} "
        board_string += "\n"
        board_string += "  +" + 8 * "---+" + "\n"
        for row in range(8):
            board_string += f"{row + 1} |"
            for col in range(8):
                board_string += f" {PRINT_SYMBOLS[self._board[row][col]]} |"
            board_string += "\n"
            board_string += "  +" + 8 * "---+" + "\n"
        return board_string

    def print_board(self):
        """
        Print the current state of the board
        """
        print(self._get_board_string())

    def get_current_player(self):
        """
        Returns the player who's turn it is if the game is not over; None otherwise
        """
        if not self._game_is_over:
            return self._current_player
        else:
            return None

    def get_statistics(self):
        """
        Iterates over the board and returns the number of Empty and the number of fields occupied by a certain player
        """
        # Create a dictionary with the players and the Empty Cell as key
        # At the beginning each player has 0 stones
        points_dict = {PLAYER_ONE: 0, PLAYER_TWO: 0, EMPTY_CELL: 0}
        # Iterate over the board
        for row in range(8):
            for col in range(8):
                # Add one to the number of fields occupied by a player for each field
                points_dict[self._board[row][col]] += 1
        return points_dict

    def get_board(self):
        """
        Returns a copy of the board
        """
        return copy.deepcopy(self._board)

    def get_turn_nr(self):
        """
        :return: actual turn number
        """
        return self._turn_nr

    def get_taken_mv(self):
        """
        :return: deepcopy of list of taken moves like ["d2","e3"]
        """
        return copy.deepcopy(self._taken_moves)

    def get_winner(self):
        """
        Returns the winner of the game.
        The player with the most stones on the board is the winner.
        If both Players own the same number of stones, the winner is None and it is a tie
        """
        stats = self.get_statistics()
        if stats[PLAYER_ONE] == stats[PLAYER_TWO]:
            return None
        elif stats[PLAYER_ONE] > stats[PLAYER_TWO]:
            return PLAYER_ONE
        else:
            return PLAYER_TWO

    def utility(self, player):
        """
        Returns:
          1: if the give player is the winner
          0: if it is a tie
         -1: If the given player lost
        """
        winner = self.get_winner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

    @staticmethod
    def other_player(player):
        """
        Returns the other player. None if the given Player is unknown
        """
        if player == PLAYER_ONE:
            return PLAYER_TWO
        elif player == PLAYER_TWO:
            return PLAYER_ONE
        else:
            return None

    def _next_player(self):
        """
        Sets current player to the next player
        """
        if self._current_player == PLAYER_ONE:
            self._current_player = PLAYER_TWO
        elif self._current_player == PLAYER_TWO:
            self._current_player = PLAYER_ONE

    def _update_fringe(self, position):
        """
        Adds the fields next to the given one to the fringe
        """
        # Look for neighbouring fields in each direction
        for direction in DIRECTIONS:
            # Get the neighbour in that direction
            next_step = Othello._next_step(position, direction)
            # Test whether the neighbour calculated is still on the board
            if next_step is not None:
                (new_x, new_y) = next_step
                # Add the neighbor to the fringe if it is not occupied by a stone
                if self._board[new_x][new_y] == EMPTY_CELL:
                    self._fringe.add(next_step)

    def _prepare_next_turn(self):
        """
        Prepare the game state for the next turn
        """
        # Set the current player to the next player
        self._next_player()
        # Compute the legal moves for that player
        self._compute_available_moves()

    @staticmethod
    def _next_step(position, direction):
        """
        Calculates the coordinates of the field reached by starting at position and going one step in direction.
        Returns None if the calculated coordinates are not on the board.
        """
        # Access the values stored in the pairs
        (y, x), (y_step, x_step) = position, direction
        # Calculate the new position
        new_position = (new_y, new_x) = (y + y_step, x + x_step)
        # Check whether the new position is still on the board.
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            # If yes return it
            return new_position
        else:
            # If no return None
            return None

    def get_available_moves(self):
        """
        Returns all the legal moves in the current game state
        """
        return list(self._turning_stones.keys())

    def set_available_moves(self, moves: list):
        """
        Function will set the list of Elements as long as they are in the set right now
        """
        # Create a temp dict
        new_moves = dict()
        # Iterate over the moves passed to the function
        for move in moves:
            # Check whether the move is a legal move right now
            if move in self._turning_stones:
                # Add it to the temp dict
                new_moves[move] = self._turning_stones[move]
        # Check whether there are any moves in new-moves
        if len(new_moves) > 0:
            # Set the moves
            self._turning_stones = new_moves

    def play_position(self, position):
        """
        Play the given position as a move. Returns False if the move is illegal
        """
        # Check whether the move is in the set of legal moves
        if position in self.get_available_moves():
            # If yes play the move

            # Access the coordinates in the tuple
            (row, column) = position
            # Get the Symbol of the current player
            current_symbol = self._current_player
            # Mark the given position as taken by the current player
            self._board[row][column] = current_symbol
            # Iterate over the set of stones turned by that move
            for (row2, column2) in self._turning_stones[position]:
                # Turn the stone. The field is now owned by the current player
                self._board[row2][column2] = current_symbol
            self._taken_moves[self._turn_nr] = COLUMN_NAMES[column] + str(row + 1)
            self._turn_nr += 1
            # The position is occupied now. Remove it from fringe
            self._fringe.remove(position)
            # Add the unoccupied neighbors of the position to the fringe.
            self._update_fringe(position)
            # Prepare the next turn
            self._prepare_next_turn()
            return True
        else:
            # If no return false
            return False

    def _compute_available_moves(self):
        """
        Computes the legal moves in the current state and stores them for later use.
        """
        # Delete the moves available in the previous turn
        self._turning_stones = dict()
        # Get the symbol of the current player
        own_symbol = self._current_player
        # Iterate over each position in fringe to test whether it would be a legal move
        for current_position in self._fringe:
            # Create a set to store the stones that would be turned by making that move
            position_turns = set()
            # Iterate over all directions to find the stones turned in each direction
            for direction in DIRECTIONS:
                # Calculate the first field in that direction
                next_step = Othello._next_step(current_position, direction)
                # Create a set to store the stones turned in this direction
                this_direction = set()
                # Continue to go in the give direction while the new field is still on the board
                while next_step is not None:
                    # Access the coordinates in the pair
                    (current_x, current_y) = next_step
                    # Get the value of the calculated position
                    current_value = self._board[current_x][current_y]
                    # If the field is empty no the line is not ended by a stone of the current player
                    # No stone will be turned in that direction. Evaluate the next direction
                    if current_value == EMPTY_CELL:
                        break
                    # If the field is owned by the other player the stone might be turned.
                    # Store the position for future use
                    elif current_value != own_symbol:
                        this_direction.add(next_step)
                    # If the line is ended by a field owned by the current player some stones might be turned.
                    elif current_value == own_symbol:
                        # Add all stones between the starting position and the end of his line to the stones turned
                        position_turns = position_turns | this_direction
                        break
                    # continue to walk in that direction
                    next_step = Othello._next_step(next_step, direction)
            # The position is only a legal turn if at least one field changes its ownership
            if len(position_turns) > 0:
                self._turning_stones[current_position] = position_turns
        # If there are no legal moves the player has to pass
        if len(self._turning_stones) == 0:
            # If the previous player had to pass as well the game is over
            if self._last_turn_passed:
                self._game_is_over = True
            # If the last player did not pass
            else:
                # Store the fact that the current player had to pass
                self._last_turn_passed = True
                # It is the other player's turn now
                self._prepare_next_turn()
        # If the player is able to play a move store the fact, that he did not pass
        else:
            self._last_turn_passed = False
