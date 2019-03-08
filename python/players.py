"""
This file contains the available player AIs
"""

from othello import Othello
from heuristics import Nijssen07Heuristic
from util import UtilMethods
import random
import sys
import operator
from machine_learning import Database


class PlayerRandom:
    """
    The PlayerRandom plays a random move taken from the set of legal moves
    """

    @staticmethod
    def get_move(game_state: Othello):
        """
        Return the selected move for the current state
        """
        # Get the legal moves
        possible_moves = game_state.get_available_moves()
        # Return a Random move
        return possible_moves[random.randrange(len(possible_moves))]


class PlayerHuman:
    """
    The PlayerHuman asks the user to select each move
    """

    @staticmethod
    def get_move(game_state: Othello):
        """
        Asks the user for a move and returns the selection
        """
        # Create a data structure to use with UtilMethods.select_one
        possibilities = []
        for move in game_state.get_available_moves():
            (row, col) = move
            description = f"({Othello.COLUMN_NAMES[col]}{row + 1})"
            possibilities.append((description, move))
        # Return the users selection
        return UtilMethods.select_one(possibilities, "Select your move:")


class PlayerMonteCarlo:
    """
    The PlayerMonteCarlo determines the best move based on the simplest form of the MonteCarlo-Algorithm 
    """

    def __init__(self):
        """
        Initialize the Player
        """
        # Ask the user to enter the number of random games per tur
        self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)

    @staticmethod
    def play_random_game(own_symbol, simulated_game):
        """
        Play the given simulated_game to an end and return the first move and whether the game was won or not
        """
        # Select a random move based on the RandomPlayer and store it
        first_move = PlayerRandom.get_move(simulated_game)
        # Play the selected move
        simulated_game.play_position(first_move)
        # Continue to Play until the game is over
        while not simulated_game.game_is_over():
            # Get a random move
            move = PlayerRandom.get_move(simulated_game)
            # Play the random move
            simulated_game.play_position(move)
        # Decide whether the game was won
        won = 1 if simulated_game.get_winner() == own_symbol else 0
        # Return the first move and whether the game was won or not
        return first_move, won

    def get_move(self, game_state: Othello):
        """
        Get the player's selection
        """
        # Create a dictionary to store information on won/lost ratios
        winning_statistics = dict()
        # Get the own symbol
        own_symbol = game_state.get_current_player()
        # Get the set of legal moves
        possible_moves = game_state.get_available_moves()
        # Add a pair of (won_games, times_played) to the dictionary for each legal move
        for move in possible_moves:
            winning_statistics[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        # Simulate big_n games
        for i in range(self.big_n):
            # Copy the current game state
            simulated_game = game_state.deepcopy()
            # Play one random game and access the returned information
            first_played_move, won = self.play_random_game(own_symbol, simulated_game)
            # Access the statistics stored for the move selected in the random game
            (won_games, times_played) = winning_statistics[first_played_move]
            # Increment the counters accordingly
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)

        # Reduce the pair of (won_games, times_played) to a winning probability
        for single_move in winning_statistics:
            # Access the values
            (games_won, times_played) = winning_statistics[single_move]
            # Calculate the fraction
            winning_statistics[single_move] = games_won / times_played

        # Select the move with the maximum probability of winning
        selected_move = max(winning_statistics.items(), key=operator.itemgetter(1))[0]
        # Return the selected move
        return selected_move


class PlayerMonteCarlo2:
    def __init__(self):
        self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)

    def get_move(self, game_state: Othello):
        if game_state.get_turn_nr() < 10:  # check whether start move match
            moves = game_state.get_available_start_tables()
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[random.randrange(len(moves))])
        winning_statistics = dict()
        own_symbol = game_state.get_current_player()
        possible_moves = game_state.get_available_moves()
        for move in possible_moves:
            winning_statistics[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        for i in range(self.big_n):
            simulated_game = game_state.deepcopy()
            first_played_move, won = PlayerMonteCarlo.play_random_game(own_symbol, simulated_game)
            (won_games, times_played) = winning_statistics[first_played_move]
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)

        for single_move in winning_statistics:
            (games_won, times_played) = winning_statistics[single_move]
            winning_statistics[single_move] = games_won / times_played

        selected_move = max(winning_statistics.items(), key=operator.itemgetter(1))[0]
        return selected_move


class PlayerMonteCarlo3:
    db = Database()

    def __init__(self):
        self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)
        self.db.init_database()

    @staticmethod
    def play_weighted_random_game(own_symbol, simulated_game):
        print(f"TODO: {own_symbol}, {simulated_game}")
        # first_move = PlayerRandom.get_move(simulated_game)
        # simulated_game.play_position(first_move)
        # while not simulated_game.game_is_over():
        #     move = PlayerRandom.get_move(simulated_game)
        #     simulated_game.play_position(move)
        # won = 1 if simulated_game.get_winner() == own_symbol else 0
        # return first_move, won

    def get_move(self, game_state: Othello):
        if game_state.get_turn_nr() < 10:  # check whether start move match
            moves = game_state.get_available_start_tables()
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[random.randrange(len(moves))])
        winning_statistics = dict()
        own_symbol = game_state.get_current_player()
        possible_moves = game_state.get_available_moves()
        for move in possible_moves:
            winning_statistics[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        for i in range(self.big_n):
            simulated_game = game_state.deepcopy()
            first_played_move, won = PlayerMonteCarlo.play_random_game(own_symbol, simulated_game)
            (won_games, times_played) = winning_statistics[first_played_move]
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)

        for single_move in winning_statistics:
            (games_won, times_played) = winning_statistics[single_move]
            winning_statistics[single_move] = games_won / times_played

        selected_move = max(winning_statistics.items(), key=operator.itemgetter(1))[0]
        return selected_move


class PlayerAlphaBetaPruning:
    # Compare https://github.com/karlstroetmann/Artificial-Intelligence/blob/master/SetlX/game-alpha-beta.stlx
    def __init__(self, search_depth=None):
        if search_depth is None:
            self.search_depth = UtilMethods.get_integer_selection("Select Search depth", 1, 10)
        else:
            self.search_depth = search_depth

    @staticmethod
    def value(game_state: Othello, depth, alpha=-1, beta=1):
        if game_state.game_is_over():
            return game_state.utility(game_state.get_winner()) * 1000
        if depth == 0:
            return Nijssen07Heuristic.heuristic(game_state.get_current_player(), game_state)
        val = alpha
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            val = max({val, -1 * PlayerAlphaBetaPruning.value(next_state, depth - 1, -beta, -alpha)})
            if val >= beta:
                return val
            alpha = max({val, alpha})
        return val

    def get_move(self, game_state: Othello):
        best_moves = dict()
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            result = -PlayerAlphaBetaPruning.value(next_state, self.search_depth - 1)
            if result not in best_moves.keys():
                best_moves[result] = []
            best_moves[result].append(move)

        best_move = max(best_moves.keys())

        return best_moves[best_move][random.randrange(len(best_moves[best_move]))]
