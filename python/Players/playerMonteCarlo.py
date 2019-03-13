from othello import Othello
from start_tables import StartTables
from util import UtilMethods
from heuristics import Nijssen07Heuristic
import operator
from Players.playerRandom import PlayerRandom
import sys
import random


class PlayerMonteCarlo:
    """
    The PlayerMonteCarlo determines the best move based on the simplest form of the MonteCarlo-Algorithm
    """

    start_tables = StartTables()
    move_probability = dict()

    def __init__(self, big_number=0, use_start_libs=None, preprocessor_n=0):
        """
        Initialize the Player
        """
        if big_number != 0:
            self.big_n = big_number
        else:
            # Ask the user to enter the number of random games per turn
            self.big_n = UtilMethods.get_integer_selection("[Player MonteCarlo] Select Number of Simulated Games", 100, sys.maxsize)

        if use_start_libs is None:
            # Ask the user to determine whether to use the start library
            self.use_start_lib = UtilMethods.get_boolean_selection("[Player MonteCarlo] Do you want to use the start library?")
        else:
            self.use_start_lib = use_start_libs

        if preprocessor_n == 0:
            # Check whether to use the preprocessor
            self.use_preprocessor_fixed = UtilMethods.get_boolean_selection("[Player MonteCarlo] Do you want to use the fixed length preprocessor?")
            if self.use_preprocessor_fixed:
                self.preprocessor_fixed_Ns = self.big_n = UtilMethods.get_integer_selection("[Player MonteCarlo]>>[FixedLen Preprocessor] Select Number of moves passing through preprocessor", 1, 64)
        elif preprocessor_n == -1:
            self.use_preprocessor_fixed = False
            self.preprocessor_fixed_Ns = 0
        else:
            self.use_preprocessor_fixed = True
            self.preprocessor_fixed_Ns = self.big_n = preprocessor_n

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
        # empty dictionary or win probabilities
        self.move_probability.clear()
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
            self.move_probability[single_move] = games_won / times_played

        # Select the move with the maximum probability of winning
        selected_move = max(self.move_probability.items(), key=operator.itemgetter(1))[0]
        # Return the selected move
        return selected_move

    def get_move_probability(self, move):
        return self.move_probability[move]
