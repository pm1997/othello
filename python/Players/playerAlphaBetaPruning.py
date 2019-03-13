from othello import Othello
from start_tables import StartTables
from util import UtilMethods
import random
from heuristics import Nijssen07Heuristic
from Players.playerMachineLearning import PlayerMachineLearning


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
