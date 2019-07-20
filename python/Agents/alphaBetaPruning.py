from othello import Othello
from start_tables import StartTables
import util
import random
import heuristics
from Agents.monteCarlo import MonteCarlo
from functools import lru_cache


class AlphaBetaPruning:

    _start_tables = StartTables()

    def __init__(self, heuristic=heuristics.StoredMonteCarloHeuristic.heuristic, search_depth=5, mc_count=10, use_monte_carlo=False, use_start_lib=True):
        """
        init start variables and used modules
        """
        self._search_depth = search_depth
        if self._search_depth == 0:
            self._search_depth = util.get_integer_selection("[Player AlphaBetaPruning] Select Search depth", 1, 10)

        self._heuristic = heuristic
        if self._heuristic is None:
            self._heuristic = heuristics.select_heuristic("Player MonteCarlo")

        self._use_monte_carlo = use_monte_carlo
        if self._use_monte_carlo is None:
            self._use_start_lib = util.get_boolean_selection(
                "[Player AlphaBetaPruning] Do you want to use monte carlo after alpha-beta pruning?")

        if self._use_monte_carlo:
            self._mc_count = mc_count
            if self._mc_count == 0:
                self._mc_count = util.get_integer_selection(
                    "[Player AlphaBetaPruning - Machine Learning] Select number of played Games", 10, 75)

        # Ask the user to determine whether to use the start library
        self._use_start_lib = use_start_lib
        if self._use_start_lib is None:
            self._use_start_lib = util.get_boolean_selection(
                "[Player AlphaBetaPruning] Do you want to use the start library?")

    @staticmethod
    @lru_cache(maxsize=None)
    def value(game_state: Othello, depth, heuristic, alpha=-1, beta=1):
        """
        Get value for game_state according to alpha beta pruning
        :param game_state: The state to evaluate
        :param depth: do alpha beta pruning until this depth is reached
        :param heuristic: Function reference for the heuristic used to score game state after maximum search depth is reached
        :param alpha: value of alpha
        :param beta:  value of beta
        :return: value of move
        Compare https://github.com/karlstroetmann/Artificial-Intelligence/blob/master/SetlX/game-alpha-beta.stlx
        """
        if game_state.game_is_over():
            return game_state.utility(game_state.get_current_player())
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

    @staticmethod
    @lru_cache(maxsize=None)
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
        Compare https://github.com/karlstroetmann/Artificial-Intelligence/blob/master/SetlX/game-alpha-beta.stlx
        """
        if game_state.game_is_over():
            return game_state.utility(game_state.get_current_player())
        if depth == 0:
            # use monte carlo player if enabled
            # mc_count = number of played games
            mc = MonteCarlo(big_number=mc_count, use_start_libs=False, preprocessor_n=-1, heuristic=heuristic, use_multiprocessing=False)
            # get best move
            move = mc.get_move(game_state)
            # return winnings stats of best move
            prob = mc.get_move_probability(move)
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
        Will select the best move according to the value of the resulting game_state according to monte carlo
        :param game_state: current game state
        :return: best move in available moves
        """
        # Use start library if it is selected and still included
        if self._use_start_lib and game_state.get_turn_nr() < 21:  # check whether start move match
            moves = self._start_tables.get_available_moves_of_start_tables(game_state)
            if len(moves) > 0:
                return util.translate_move_to_pair(moves[random.randrange(len(moves))])
        # According to experience the number of moves to consider decreases relevantly after reaching a certain
        # turn number. Therefore it is possible to increase the search depth without loosing to much time.
        # We dynamically increase the search depth after reaching turn_number 40
        search_depth = self._search_depth
        turn_number = game_state.get_turn_nr()
        if turn_number > 40:
            search_depth += turn_number // 10
        # Dict used to store a list of the moves resulting in a state with the respective value
        best_moves = dict()
        # Evaluate each available move
        for move in game_state.get_available_moves():
            # Play the move to get the resulting state
            next_state = game_state.deepcopy()
            next_state.play_position(move)

            # Evaluate the state using the selected function
            if self._use_monte_carlo:
                result = -AlphaBetaPruning.value_monte_carlo(next_state, search_depth - 1, self._heuristic,
                                                             mc_count=self._mc_count)
            else:
                result = -AlphaBetaPruning.value(next_state, self._search_depth - 1, self._heuristic)

            # Append the move to the list of states with that value
            if result not in best_moves.keys():
                best_moves[result] = []
            best_moves[result].append(move)

        # Determine the best result
        best_result = max(best_moves.keys())
        if self._use_monte_carlo:
            print(AlphaBetaPruning.value_monte_carlo.cache_info())
            AlphaBetaPruning.value_monte_carlo.cache_clear()
        else:
            print(AlphaBetaPruning.value.cache_info())
            AlphaBetaPruning.value.cache_clear()
        # Play one random move with the best possible result
        return best_moves[best_result][random.randrange(len(best_moves[best_result]))]
