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
from constants import COLUMN_NAMES
from start_tables import StartTables


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
            description = f"({COLUMN_NAMES[col]}{row + 1})"
            possibilities.append((description, move))
        # Return the users selection
        return UtilMethods.select_one(possibilities, "Select your move:")


class PlayerAlphaBetaPruning:
    # Compare https://github.com/karlstroetmann/Artificial-Intelligence/blob/master/SetlX/game-alpha-beta.stlx

    start_tables = StartTables()

    def __init__(self, search_depth=None, use_machine_learning=None):
        """
        init start variables and used modules
        :param search_depth: max search depth before heuristic or machine learning is used
        """

        if search_depth is None:
            self.search_depth = UtilMethods.get_integer_selection("[Player AlphaBetaPruning] Select Search depth", 1, 10)
        else:
            self.search_depth = search_depth

        if use_machine_learning is None:
            # Ask the user to determine whether to use the start library
            self.use_ml = UtilMethods.get_boolean_selection(
                    "[Player AlphaBetaPruning] Do you want to use the machine learning after Alpha-Beta Pruning?")

            if self.use_ml:
                self.ml_count = UtilMethods.get_integer_selection("[Player AlphaBetaPruning - Machine Learning] Select number of played Games", 15, 200)
        else:
            self.use_ml = False
            self.ml_count = 1

        # Ask the user to determine whether to use the start library
        self.use_start_lib = UtilMethods.get_boolean_selection("[Player AlphaBetaPruning] Do you want to use the start library?")

    @staticmethod
    def value(game_state: Othello, depth, alpha=-1, beta=1):
        if game_state.game_is_over():
            return game_state.utility(game_state.get_winner()) * 1000
        if depth == 0:
                # return heuristic of game state
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

    @staticmethod
    def value_ml(game_state: Othello, depth, alpha=-1, beta=1, ml_count=100):
        if game_state.game_is_over():
            return game_state.utility(game_state.get_winner()) * 1000
        if depth == 0:
            # use machine learning player again if enabled
            # alpha_beta was used, so disable use of alpha_beta
            # ml_count = number of played games
            ml = PlayerMachineLearning(big_number=ml_count)
            # get best move
            move = ml.get_move(game_state)
            # return winnings stats of best move
            prob = ml.get_move_probability(move)
            print(f"win probability of move {move} calculated: {prob}")
            return prob
        val = alpha
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            val = max({val, -1 * PlayerAlphaBetaPruning.value_ml(next_state, depth - 1, -beta, -alpha)})
            if val >= beta:
                return val
            alpha = max({val, alpha})
        return val

    def get_move(self, game_state: Othello):
        # Use start library if it is selected and still included
        if self.use_start_lib and game_state.get_turn_nr() < 10:  # check whether start move match
            moves = self.start_tables.get_available_start_tables(game_state)
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[random.randrange(len(moves))])
        best_moves = dict()
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)

            # differ between machine learning or heuristic
            if self.use_ml:
                result = -PlayerAlphaBetaPruning.value_ml(next_state, self.search_depth - 1)
            else:
                result = -PlayerAlphaBetaPruning.value(next_state, self.search_depth - 1)

            if result not in best_moves.keys():
                best_moves[result] = []
            best_moves[result].append(move)

        best_move = max(best_moves.keys())

        return best_moves[best_move][random.randrange(len(best_moves[best_move]))]


class PlayerMonteCarlo:
    """
    The PlayerMonteCarlo determines the best move based on the simplest form of the MonteCarlo-Algorithm 
    """

    start_tables = StartTables()

    def __init__(self):
        """
        Initialize the Player
        """
        # Ask the user to enter the number of random games per turn
        self.big_n = UtilMethods.get_integer_selection("[Player MonteCarlo] Select Number of Simulated Games", 100, sys.maxsize)
        # Ask the user to determine whether to use the start library
        self.use_start_lib = UtilMethods.get_boolean_selection("[Player MonteCarlo] Do you want to use the start library?")
        # Check whether to use the preprocessor
        self.use_preprocessor_fixed = UtilMethods.get_boolean_selection("[Player MonteCarlo] Do you want to use the fixed length preprocessor?")
        if self.use_preprocessor_fixed:
            self.preprocessor_fixed_Ns = self.big_n = UtilMethods.get_integer_selection("[Player MonteCarlo]>>[FixedLen Preprocessor] Select Number of moves passing through preprocessor", 1, 64)

    @staticmethod
    def preprocess_fixed(game_state: Othello, number_of_elements):
        # Create Dict to store the value of every move
        ratings = dict()
        # Iterate over the moves to calculate each moves's value
        for move in game_state.get_available_moves():
            # Create a copy of the game_state to be able to manipulate it without side effects
            copy_of_state = game_state.deepcopy()
            # Play the move to evaluate the value of the game after making the move
            copy_of_state.play_position(move)
            # Get the value of the current state
            ratings[move] = Nijssen07Heuristic.heuristic(game_state.get_current_player(), copy_of_state)
        # Sort the dict by value
        ratings = sorted(ratings.items(), key=operator.itemgetter(1))
        game_state.set_available_moves(ratings[:number_of_elements][0])

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
        # Use start library if it is selected and still included
        if self.use_start_lib and game_state.get_turn_nr() < 10:  # check whether start move match
            moves = self.start_tables.get_available_start_tables(game_state)
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[random.randrange(len(moves))])
        # Create a dictionary to store information on won/lost ratios
        winning_statistics = dict()
        # Get the own symbol
        own_symbol = game_state.get_current_player()
        # Check whether to preprocess the available moves
        if self.use_preprocessor_fixed:
            # Preprocess the available moves
            PlayerMonteCarlo.preprocess_fixed(game_state, self.preprocessor_fixed_Ns)
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


class PlayerMachineLearning:
    db = Database()
    # store available moves (top level) in dictionary
    move_probability = dict()

    def __init__(self, big_number=0):
        if big_number != 0:
            self.big_n = big_number
        else:
            self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)

        # init machine learning database
        self.db.init_database()

    def get_weighted_random(self, possible_moves, turn_nr):
        prob_sum = 0.0
        # get sum of all chances in possible moves
        for move in possible_moves:
            prob_sum += self.db.get_likelihood(move, turn_nr)

        # choose a random float between 0 and calculated sum
        chose = random.uniform(0.0, prob_sum)

        move_nr = 0
        prob_sum = 0.0
        # iterate over possible move to get
        for move in possible_moves:
            move_nr += 1
            prob_sum += self.db.get_likelihood(move, turn_nr)
            if prob_sum >= chose:
                # if prob_sum >= chose return move
                return move
        # return last possible move because it's the only remaining move
        return possible_moves[-1]

    def play_weighted_random_game(self, own_symbol, simulated_game):
        # get possible moves
        possible_moves = simulated_game.get_available_moves()

        # choose winning moves more times than loss moves
        first_move = self.get_weighted_random(possible_moves, simulated_game.get_turn_nr())
        # play move
        simulated_game.play_position(first_move)
        # play whole remaining game
        while not simulated_game.game_is_over():
            possible_moves2 = simulated_game.get_available_moves()
            move = self.get_weighted_random(possible_moves2, simulated_game.get_turn_nr())
            simulated_game.play_position(move)
        won = 1 if simulated_game.get_winner() == own_symbol else 0

        return won, first_move, simulated_game.get_taken_mv()

    def get_move(self, game_state: Othello):
        # init variables
        own_symbol = game_state.get_current_player()
        possible_moves = game_state.get_available_moves()

        move_stats = dict()
        self.move_probability.clear()

        for move in possible_moves:
            move_stats[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        # play big_n games
        for i in range(self.big_n):
            # copy game and update database
            simulated_game = game_state.deepcopy()
            # select a weighted random move and play remaining game
            won, first_played_move, played_moves = self.play_weighted_random_game(own_symbol, simulated_game)
            (won_games, times_played) = move_stats[first_played_move]
            # update move stats of actual big_n games
            move_stats[first_played_move] = (won_games + won, times_played + 1)
            self.db.update_all_weights(played_moves, won)

        # save database to csv file
        self.db.store_database()

        for single_move in move_stats:
            # calculate percentage of won games
            (games_won, times_played) = move_stats[single_move]
            self.move_probability[single_move] = games_won / times_played

        # get move with highest winning percentage
        selected_move = max(self.move_probability.items(), key=operator.itemgetter(1))[0]
        return selected_move

    def get_move_probability(self, move):
        return self.move_probability[move]
