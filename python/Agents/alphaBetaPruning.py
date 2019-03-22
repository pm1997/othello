from othello import Othello
from start_tables import StartTables
from util import UtilMethods
import random
import heuristics
# from Agents.machineLearning import PlayerMachineLearning
from Agents.monteCarlo import MonteCarlo


class AlphaBetaPruning:
    # Compare https://github.com/karlstroetmann/Artificial-Intelligence/blob/master/SetlX/game-alpha-beta.stlx

    start_tables = StartTables()

    def __init__(self, heuristic=heuristics.StoredMonteCarloHeuristic.heuristic, search_depth=5, use_ml=False, use_monte_carlo=False, use_start_lib=True):
        """
        init start variables and used modules
        """

        self.search_depth = search_depth  # UtilMethods.get_integer_selection("[Player AlphaBetaPruning] Select Search depth", 1, 10)

        self.heuristic = heuristic  # heuristics.select_heuristic("Player MonteCarlo")

        # Ask the user to determine whether to use the start library
        # self.use_ml = UtilMethods.get_boolean_selection(
        #    "[Player AlphaBetaPruning] Do you want to use the machine learning after Alpha-Beta Pruning?")

        self.use_ml = use_ml
        self.use_monte_carlo = use_monte_carlo
        if self.use_ml:
            self.ml_count = UtilMethods.get_integer_selection(
                "[Player AlphaBetaPruning - Machine Learning] Select number of played Games", 10, 75)
            self.use_monte_carlo = False
        else:
            self.use_ml = False
            self.ml_count = 1

            self.use_monte_carlo = False  # UtilMethods.get_boolean_selection(
            #  "[Player AlphaBetaPruning] Do you want to use the Monte Carlo after Alpha-Beta Pruning?")

            if self.use_monte_carlo:
                self.ml_count = UtilMethods.get_integer_selection(
                    "[Player AlphaBetaPruning - Machine Learning] Select number of played Games", 10, 75)
            else:
                self.use_monte_carlo = False
                self.ml_count = 1

        # Ask the user to determine whether to use the start library
        self.use_start_lib = use_start_lib  # UtilMethods.get_boolean_selection(
        #    "[Player AlphaBetaPruning] Do you want to use the start library?")

    @staticmethod
    def value(game_state: Othello, depth, heuristic, alpha=-1, beta=1):
        """
        get score for alpha beta pruning
        :param game_state: actual game state
        :param depth: do alpha beta pruning this depth
        :param heuristic: score game state after alpha beta pruning with this heuristic
        :param alpha: value of alpha
        :param beta:  value of beta
        :return: score of move
        """
        if game_state.game_is_over():
            return game_state.utility(game_state.get_winner()) * 1000
        if depth == 0:
            # return heuristic of game state
            return heuristic(game_state.get_current_player(), game_state)
        val = alpha
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            val = max({val, -1 * AlphaBetaPruning.value(next_state, depth - 1, heuristic, -beta, -alpha)})
            if val >= beta:
                return val
            alpha = max({val, alpha})
        return val

    # @staticmethod
    # def value_ml(game_state: Othello, depth, alpha=-1, beta=1, ml_count=100):
    #     """
    #     get score for alpha beta pruning
    #     :param game_state: actual game state
    #     :param depth: do alpha beta pruning this depth
    #     :param ml_count: number of games which are played in each terminal node after alpha beta pruning
    #     :param alpha: value of alpha
    #     :param beta:  value of beta
    #     :return: score of move
    #     """
    #     if game_state.game_is_over():
    #         return game_state.utility(game_state.get_winner()) * 1000
    #     if depth == 0:
    #         # use machine learning player if enabled
    #         # ml_count = number of played games
    #         ml = PlayerMachineLearning(big_number=ml_count, use_multiprocessing=False)
    #         # get best move
    #         move = ml.get_move(game_state)
    #         # return winnings stats of best move
    #         prob = ml.get_move_probability(move)
    #         print(f"win probability of move {move} calculated: {prob}")
    #         return prob
    #     val = alpha
    #     for move in game_state.get_available_moves():
    #         next_state = game_state.deepcopy()
    #         next_state.play_position(move)
    #         val = max(
    #             {val, -1 * PlayerAlphaBetaPruning.value_ml(next_state, depth - 1, -beta, -alpha, ml_count=ml_count)})
    #         if val >= beta:
    #             return val
    #         alpha = max({val, alpha})
    #     return val

    @staticmethod
    def value_monte_carlo(game_state: Othello, depth, heuristic, alpha=-1, beta=1, mc_count=100):
        """
        get score for alpha beta pruning
        :param game_state: actual game state
        :param depth: do alpha beta pruning this depth
        :param heuristic: score game state after alpha beta pruning with this heuristic
        :param mc_count: number of games which are played in each terminal node after alpha beta pruning
        :param alpha: value of alpha
        :param beta:  value of beta
        :return: score of move
        """
        if game_state.game_is_over():
            return game_state.utility(game_state.get_winner()) * 1000
        if depth == 0:
            # use monte carlo player if enabled
            # ml_count = number of played games
            ml = MonteCarlo(big_number=mc_count, use_start_libs=False, preprocessor_n=-1, heuristic=heuristic, use_multiprocessing=False)
            # get best move
            move = ml.get_move(game_state)
            # return winnings stats of best move
            prob = ml.get_move_probability(move)
            # print(f"win probability of move {move} calculated: {prob}")
            return prob
        val = alpha
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            val = max({val,
                       -1 * AlphaBetaPruning.value_monte_carlo(next_state, depth - 1, heuristic, -beta, -alpha,
                                                               mc_count=mc_count)})
            if val >= beta:
                return val
            alpha = max({val, alpha})
        return val

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
        best_moves = dict()
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)

            # differ between machine learning or heuristic
            if self.use_ml:
                print("not supported")
                result = 0
                # result = -PlayerAlphaBetaPruning.value_ml(next_state, self.search_depth - 1, ml_count=self.ml_count)
            elif self.use_monte_carlo:
                result = -AlphaBetaPruning.value_monte_carlo(next_state, self.search_depth - 1, self.heuristic,
                                                             mc_count=self.ml_count)
            else:
                result = -AlphaBetaPruning.value(next_state, self.search_depth - 1, self.heuristic)

            if result not in best_moves.keys():
                best_moves[result] = []
            best_moves[result].append(move)

        best_move = max(best_moves.keys())

        return best_moves[best_move][random.randrange(len(best_moves[best_move]))]
