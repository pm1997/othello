from othello import Othello
from start_tables import StartTables
import operator
from Agents.random import Random
import util
import sys
import random
import heuristics
import multiprocessing as mp
import database


class MonteCarlo:
    """
    The PlayerMonteCarlo determines the best move based on the simplest form of the MonteCarlo-Algorithm
    """

    _start_tables = StartTables()
    _move_probability = dict()
    _ml_database = database.db

    def __init__(self, big_number=2000, use_start_libs=True, preprocessor_n=-1, heuristic=heuristics.StoredMonteCarloHeuristic.heuristic, use_multiprocessing=True, use_weighted_random=False):
        """
        Initialize the Player
        """
        if big_number != 0:
            self._big_n = big_number
        else:
            # Ask the user to enter the number of random games per turn
            self._big_n = util.get_integer_selection("[Player MonteCarlo] Select Number of Simulated Games", 100,
                                                     sys.maxsize)
        if use_weighted_random is None:
            # Ask the user to determine whether to use the start library
            self._use_weighted_random = util.get_boolean_selection(
                "[Player MonteCarlo] Do you want to use a weighted random game selection?")
        else:
            self._use_weighted_random = use_weighted_random

        if use_start_libs is None:
            # Ask the user to determine whether to use the start library
            self._use_start_lib = util.get_boolean_selection(
                "[Player MonteCarlo] Do you want to use the start library?")
        else:
            self._use_start_lib = use_start_libs

        if preprocessor_n == 0:
            # Check whether to use the preprocessor
            self._preprocessor, self._preprocessor_parameter = self.select_preprocessor()
        elif preprocessor_n == -1:
            self._preprocessor = None
        else:
            self._preprocessor = MonteCarlo.preprocess_variable_selectivity
            self._preprocessor_parameter = 1.0

        if heuristic is None:
            self._heuristic = heuristics.select_heuristic("Player MonteCarlo")
        else:
            self._heuristic = heuristic

        if use_multiprocessing is None:
            self._use_multiprocessing = util.get_boolean_selection("[Player Monte Carlo] Use Multiprocessing?")
        else:
            self._use_multiprocessing = use_multiprocessing

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
            ("Fixed Selectivity Preprocessor (FSP)", MonteCarlo.preprocess_fixed_selectivity))
        available_preprocessors.append(
            ("Variable Selectivity Preprocessor (VSP)", MonteCarlo.preprocess_variable_selectivity))
        # Ask the user to select a type of preprocessor.
        preprocessor = util.select_one(available_preprocessors, "[Player MonteCarlo] Select a preprocessor mode")
        preprocessor_parameter = None
        if preprocessor == MonteCarlo.preprocess_fixed_selectivity:
            preprocessor_parameter = util.get_integer_selection(
                "[Player MonteCarlo]>>[Fixed Selectivity Preprocessor] Please select the number of moves passing the preprocessor",
                1, 64)
        elif preprocessor == MonteCarlo.preprocess_variable_selectivity:
            preprocessor_parameter = util.get_float_selection(
                "[Player MonteCarlo]>>[Variable Selectivity Preprocessor] Please select the percentage of the average move value needed to pass the preprocessor",
                0, 1)

        return preprocessor, preprocessor_parameter

    @staticmethod
    def preprocess_fixed_selectivity(game_state: Othello, n_s, heuristic):
        """
        Will preprocess the given game_state by only letting the n_s best moves pass
        :param game_state:
        :param n_s:
        :param heuristic:
        :return:
        """
        # Get a list of moves sorted by their heuristic value
        heuristic_values = sorted(
            MonteCarlo.preprocess_get_heuristic_value(game_state, heuristic=heuristic).items(),
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
        heuristic_value_dict = MonteCarlo.preprocess_get_heuristic_value(game_state, heuristic=heuristic)
        # Get a list of values
        heuristic_values = [v for _, v in heuristic_value_dict.items()]
        # Calculate the Average List Value
        average_heuristic_value = sum(heuristic_values) / len(heuristic_values)
        # Pass the moves with an value of at least p_s of the average move value
        game_state.set_available_moves(
            [m for m, v in heuristic_value_dict.items() if v >= p_s * average_heuristic_value])

    @staticmethod
    def get_weighted_random(possible_moves, turn_nr, player_value):
        """
        get weighted random move: prefer moves with higher chance of winning
        :param possible_moves: list of available moves in current game state
        :param turn_nr: actual turn number
        :param player_value: actual player
        :return: random move
        """
        prob_sum = 0.0
        # get sum of all chances in possible moves
        for move in possible_moves:
            prob_sum += MonteCarlo._ml_database.get_change_of_winning(move, turn_nr, player_value)

        # choose a random float between 0 and calculated sum
        chose = random.uniform(0.0, prob_sum)

        move_nr = 0
        prob_sum = 0.0
        # iterate over possible move to get
        for move in possible_moves:
            move_nr += 1
            prob_sum += MonteCarlo._ml_database.get_change_of_winning(move, turn_nr, player_value)
            if prob_sum >= chose:
                # if prob_sum >= chose return move
                return move
        # return last possible move because it's the only remaining move
        return possible_moves[-1]

    @staticmethod
    def play_weighted_random_game(player_value, simulated_game):
        """
        :param player_value: player value (PLAYER_ONE, PLAYER_TWO)
        :param simulated_game: copy of game state
        :return: won, first_move, taken_moves
            won: player wins random game
            first_move: root move of player
            taken_moves: list of all taken moves in simulated game
        """
        # get possible moves
        possible_moves = simulated_game.get_available_moves()

        # choose winning moves more times than loss moves
        first_move = MonteCarlo.get_weighted_random(possible_moves, simulated_game.get_turn_nr(), player_value)
        # play move
        simulated_game.play_position(first_move)
        # play whole remaining game
        while not simulated_game.game_is_over():
            possible_moves2 = simulated_game.get_available_moves()
            move = MonteCarlo.get_weighted_random(possible_moves2, simulated_game.get_turn_nr(), player_value)
            simulated_game.play_position(move)
        won = 1 if simulated_game.get_winner() == player_value else 0

        return first_move, won  # , simulated_game.get_taken_mv()

    @staticmethod
    def play_random_game(player_value, simulated_game):
        """
        Play the given simulated_game to an end and return the first move and whether the game was won or not
        """
        # Select a random move based on the RandomPlayer and store it
        first_move = Random.get_move(simulated_game)
        # Play the selected move
        simulated_game.play_position(first_move)
        # Continue to Play until the game is over
        while not simulated_game.game_is_over():
            # Get a random move
            move = Random.get_move(simulated_game)
            # Play the random move
            simulated_game.play_position(move)
        # Decide whether the game was won
        won = 1 if simulated_game.get_winner() == player_value else 0
        # Return the first move and whether the game was won or not
        return first_move, won

    @staticmethod
    def play_n_random_games(player_value, game_state: Othello, number_of_games, use_weighted_random):
        """
        Plays number_of_games random games for player_value starting at game_state
        :param player_value: The representation for the observed player
        :param game_state: The game_state to use
        :param number_of_games: The number of games played
        :param use_weighted_random: Boolean determining the algorithm variant
        :return: Dict with available moves as keys and integer pairs of (games_won, times_played)
        """
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
            if use_weighted_random:
                first_played_move, won = MonteCarlo.play_weighted_random_game(player_value, simulated_game)
            else:
                first_played_move, won = MonteCarlo.play_random_game(player_value, simulated_game)
            # Access the statistics stored for the move selected in the random game
            (won_games, times_played) = winning_statistics[first_played_move]
            # Increment the counters accordingly
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)
        return winning_statistics

    @staticmethod
    def combine_statistic_dicts(base, added):
        """
        Combines the two dictionaries base and added by adding the values stored in them
        They have to contain pairs of integers.
        :param base: The base dict
        :param added: The dict to add
        :return: The combined dict
        """
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
        Returns the best move according to the games simulated by MonteCarlo
        :param game_state: actual game state
        :return: best move in available moves
        """
        # Use start library if it is selected and still included
        if self._use_start_lib and game_state.get_turn_nr() < 21:  # check whether start move match
            moves = self._start_tables.get_available_moves_of_start_tables(game_state)
            if len(moves) > 0:
                return util.translate_move_to_pair(moves[random.randrange(len(moves))])
        # Create a dictionary to store information on won/lost ratios
        # winning_statistics = dict()
        # empty dictionary or win probabilities
        self._move_probability.clear()
        # Get the own symbol
        player_value = game_state.get_current_player()
        # Check whether to preprocess the available moves
        if self._preprocessor is not None:
            # Preprocess the available moves
            self._preprocessor(game_state, self._preprocessor_parameter, self._heuristic)

        # Simulate big_n games
        if not self._use_multiprocessing:
            # Simulate the games in the current process
            winning_statistics = MonteCarlo.play_n_random_games(player_value, game_state, self._big_n, self._use_weighted_random)
        else:
            # Create a pool of worker processes. Set the number_of_processes explicitly
            # Workload can be distributed equally on the processes when their number is known
            number_of_processes = mp.cpu_count()
            pool = mp.Pool(processes=number_of_processes)
            # Use Worker processes asynchronous
            list_of_result_objects = [pool.apply_async(MonteCarlo.play_n_random_games, args=(player_value, game_state.deepcopy(), self._big_n // number_of_processes, self._use_weighted_random)) for _ in range(number_of_processes)]
            # Collect the result of the first worker
            winning_statistics = list_of_result_objects[0].get()
            # Collect the result of the other workers and combine them in one single dictionary
            for single_list in list_of_result_objects[1:]:
                MonteCarlo.combine_statistic_dicts(winning_statistics, single_list.get())
            # Close the worker pool.
            pool.close()

        # Reduce the pair of (won_games, times_played) to a winning probability
        for single_move in winning_statistics:
            # print(winning_statistics[single_move])
            # Access the values
            (games_won, times_played) = winning_statistics[single_move]
            # Calculate the fraction
            self._move_probability[single_move] = games_won / times_played

        # Select the move with the maximum probability of winning
        selected_move = max(self._move_probability.items(), key=operator.itemgetter(1))[0]
        # Return the selected move
        return selected_move

    def get_move_probability(self, move):
        """
        :param move: given move in available moves
        :return: win probability of given move
        """
        return self._move_probability[move]
