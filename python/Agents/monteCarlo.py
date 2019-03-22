from othello import Othello
from start_tables import StartTables
from util import UtilMethods
import operator
from Agents.playerRandom import PlayerRandom
import sys
import random
import heuristics
import multiprocessing as mp
import database

class PlayerMonteCarlo:
    """
    The PlayerMonteCarlo determines the best move based on the simplest form of the MonteCarlo-Algorithm
    """

    start_tables = StartTables()
    move_probability = dict()

    def __init__(self, big_number=0, use_start_libs=None, preprocessor_n=0, heuristic=None, use_multiprocessing=None):
        """
        Initialize the Player
        """
        if big_number != 0:
            self.big_n = big_number
        else:
            # Ask the user to enter the number of random games per turn
            self.big_n = UtilMethods.get_integer_selection("[Player MonteCarlo] Select Number of Simulated Games", 100,
                                                           sys.maxsize)

        if use_start_libs is None:
            # Ask the user to determine whether to use the start library
            self.use_start_lib = UtilMethods.get_boolean_selection(
                "[Player MonteCarlo] Do you want to use the start library?")
        else:
            self.use_start_lib = use_start_libs

        if preprocessor_n == 0:
            # Check whether to use the preprocessor
            self.preprocessor, self.preprocessor_parameter = self.select_preprocessor()
        elif preprocessor_n == -1:
            self.preprocessor = None
        else:
            self.preprocessor = PlayerMonteCarlo.preprocess_variable_selectivity
            self.preprocessor_parameter = 1.0

        if heuristic is None:
            self.heuristic = heuristics.select_heuristic("Player MonteCarlo")
        else:
            self.heuristic = heuristic

        if use_multiprocessing is None:
            self.use_multiprocessing = UtilMethods.get_boolean_selection("[Player Monte Carlo] Use Multiprocessing?")
        else:
            self.use_multiprocessing = use_multiprocessing

    @staticmethod
    def preprocess_get_heuristic_value(game_state: Othello, heuristic):
        """
        Returns a dict of each move's value
        :param game_state: game with actual board, player ...
        :param heuristic:  list of heuristics
        :return:
        """
        # Create Dict to store the value of every move
        heuristic_values = dict()
        # Iterate over the moves to calculate each moves's value
        for move in game_state.get_available_moves():
            # Create a copy of the game_state to be able to manipulate it without side effects
            copy_of_state = game_state.deepcopy()
            # Play the move to evaluate the value of the game after making the move
            copy_of_state.play_position(move)
            # Get the value of the current state
            heuristic_values[move] = heuristic(game_state.get_current_player(), copy_of_state)
        # return the heuristic_values
        return heuristic_values

    @staticmethod
    def select_preprocessor():
        """
        select one preprocessor with specific parameters
        :return: number of preprocessor (0 for none), parameter
        """
        # Create a list of Preprocessors
        available_preprocessors = list()
        # Use pairs of the form (description: String, class: Player) to store a player type
        available_preprocessors.append(("None", None))
        available_preprocessors.append(
            ("Fixed Selectivity Preprocessor (FSP)", PlayerMonteCarlo.preprocess_fixed_selectivity))
        available_preprocessors.append(
            ("Variable Selectivity Preprocessor (VSP)", PlayerMonteCarlo.preprocess_variable_selectivity))
        # Ask the user to select a type of preprocessor.
        preprocessor = UtilMethods.select_one(available_preprocessors, "[Player MonteCarlo] Select a preprocessor mode")
        preprocessor_parameter = None
        if preprocessor == PlayerMonteCarlo.preprocess_fixed_selectivity:
            preprocessor_parameter = UtilMethods.get_integer_selection(
                "[Player MonteCarlo]>>[Fixed Selectivity Preprocessor] Please select the number of moves passing the preprocessor",
                1, 64)
        elif preprocessor == PlayerMonteCarlo.preprocess_variable_selectivity:
            preprocessor_parameter = UtilMethods.get_float_selection(
                "[Player MonteCarlo]>>[Variable Selectivity Preprocessor] Please select the percentage of the average move value needed to pass the preprocessor",
                0, 1)

        return preprocessor, preprocessor_parameter

    @staticmethod
    def preprocess_fixed_selectivity(game_state: Othello, n_s, heuristic):
        """
        Will preprocess the given game_state by only letting the N_s best moves pass
        :param game_state:
        :param n_s:
        :param heuristic:
        :return:
        """
        # Get a list of moves sorted by their heuristic value
        heuristic_values = sorted(
            PlayerMonteCarlo.preprocess_get_heuristic_value(game_state, heuristic=heuristic).items(),
            key=operator.itemgetter(1))
        # Pass the first n_s moves on
        game_state.set_available_moves(heuristic_values[:n_s][0])

    @staticmethod
    def preprocess_variable_selectivity(game_state: Othello, p_s, heuristic):
        """
        Will preprocess the given game_state by only letting moves with an value of at least p_s of the average move value pass
        :param game_state:
        :param p_s:
        :param heuristic
        :return:
        """
        # Calculate each move's value
        heuristic_value_dict = PlayerMonteCarlo.preprocess_get_heuristic_value(game_state, heuristic=heuristic)
        # Get a list of values
        heuristic_values = [v for _, v in heuristic_value_dict.items()]
        # Calculate the Average List Value
        average_heuristic_value = sum(heuristic_values) / len(heuristic_values)
        # Pass the moves with an value of at least p_s of the average move value
        game_state.set_available_moves(
            [m for m, v in heuristic_value_dict.items() if v >= p_s * average_heuristic_value])

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

    @staticmethod
    def play_n_random_games(own_symbol, game_state: Othello, number_of_games):
        winning_statistics = dict()
        # Get the set of legal moves
        possible_moves = game_state.get_available_moves()
        # Add a pair of (won_games, times_played) to the dictionary for each legal move
        for move in possible_moves:
            winning_statistics[move] = (1, 1)  # set games played to 1 to avoid division by zero error

        # Simulate big_n games
        for _ in range(number_of_games):
            # Copy the current game state
            simulated_game = game_state.deepcopy()
            # Play one random game and access the returned information
            first_played_move, won = PlayerMonteCarlo.play_random_game(own_symbol, simulated_game)
            # Access the statistics stored for the move selected in the random game
            (won_games, times_played) = winning_statistics[first_played_move]
            # Increment the counters accordingly
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)
        return winning_statistics

    @staticmethod
    def combine_statistic_dicts(base, added):
        for move in base:
            if move in added:
                (b_won, b_played) = base[move]
                (a_won, a_played) = added[move]
                base[move] = (b_won + a_won, b_played + a_played)
        for move in added:
            if move not in base:
                base[move] = added[move]

    def get_move(self, game_state: Othello):
        """
        interface function of all players
        :param game_state: actual game state
        :return: best move in available moves
        """
        # Use start library if it is selected and still included
        if self.use_start_lib and game_state.get_turn_nr() < 10:  # check whether start move match
            moves = self.start_tables.get_available_start_tables(game_state)
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[random.randrange(len(moves))])
        # Create a dictionary to store information on won/lost ratios
        # winning_statistics = dict()
        # empty dictionary or win probabilities
        self.move_probability.clear()
        # Get the own symbol
        own_symbol = game_state.get_current_player()
        # Check whether to preprocess the available moves
        if self.preprocessor is not None:
            # Preprocess the available moves
            self.preprocessor(game_state, self.preprocessor_parameter, self.heuristic)

        # Simulate big_n games
        if not self.use_multiprocessing:
            winning_statistics = PlayerMonteCarlo.play_n_random_games(own_symbol, game_state, self.big_n)
        else:
            number_of_processes = mp.cpu_count()
            pool = mp.Pool(processes=number_of_processes)
            list_of_stats = [pool.apply_async(PlayerMonteCarlo.play_n_random_games, args=(own_symbol, game_state.deepcopy(), self.big_n//number_of_processes)) for _ in range(number_of_processes)]
            winning_statistics = list_of_stats[0].get()
            for single_list in list_of_stats[1:]:
                PlayerMonteCarlo.combine_statistic_dicts(winning_statistics, single_list.get())
            pool.close()

        # Reduce the pair of (won_games, times_played) to a winning probability
        for single_move in winning_statistics:
            # print(winning_statistics[single_move])
            # Access the values
            (games_won, times_played) = winning_statistics[single_move]
            # Calculate the fraction
            self.move_probability[single_move] = games_won / times_played

        # Select the move with the maximum probability of winning
        selected_move = max(self.move_probability.items(), key=operator.itemgetter(1))[0]
        # Return the selected move
        database.db._store_database()
        return selected_move

    def get_move_probability(self, move):
        """
        :param move: given move in available moves
        :return: win probability of given move
        """
        return self.move_probability[move]
