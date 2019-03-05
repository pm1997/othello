from othello import Othello
from heuristics import Nijssen07Heuristic
from util import UtilMethods
import random
import sys
import operator


class PlayerRandom:
    @staticmethod
    def get_move(game_state: Othello):
        possible_moves = game_state.get_available_moves()
        return possible_moves[random.randrange(len(possible_moves))]


class PlayerHuman:
    @staticmethod
    def get_move(game_state: Othello):
        possibilities = []
        for move in game_state.get_available_moves():
            (row, col) = move
            description = f"({row+1}, {Othello.COLUMN_NAMES[col]})"
            possibilities.append((description, move))
        return UtilMethods.select_one(possibilities, "Select your move:")


class PlayerMonteCarlo:
    def __init__(self):
        self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)

    @staticmethod
    def play_random_game(own_symbol, simulated_game):
        first_move = PlayerRandom.get_move(simulated_game)
        simulated_game.play_position(first_move)
        while not simulated_game.game_is_over():
            move = PlayerRandom.get_move(simulated_game)
            simulated_game.play_position(move)
        won = 1 if simulated_game.get_winner() == own_symbol else 0
        return first_move, won

    def get_move(self, game_state: Othello):
        winning_statistics = dict()
        own_symbol = game_state.get_current_player()
        possible_moves = game_state.get_available_moves()
        for move in possible_moves:
            winning_statistics[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        for i in range(self.big_n):
            simulated_game = game_state.deepcopy()
            first_played_move, won = self.play_random_game(own_symbol, simulated_game)
            (won_games, times_played) = winning_statistics[first_played_move]
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)

        for single_move in winning_statistics:
            (games_won, times_played) = winning_statistics[single_move]
            winning_statistics[single_move] = games_won / times_played

        selected_move = max(winning_statistics.items(), key=operator.itemgetter(1))[0]
        return selected_move


class PlayerMonteCarlo2:
    def __init__(self):
        self.big_n = UtilMethods.get_integer_selection("Select Number of Simulated Games", 100, sys.maxsize)

    @staticmethod
    def play_random_game(own_symbol, simulated_game):
        first_move = PlayerRandom.get_move(simulated_game)
        simulated_game.play_position(first_move)
        while not simulated_game.game_is_over():
            move = PlayerRandom.get_move(simulated_game)
            simulated_game.play_position(move)
        won = 1 if simulated_game.get_winner() == own_symbol else 0
        return first_move, won

    def get_move(self, game_state: Othello):
        if game_state.get_turn_nr() < 10:  # check whether start move match
            moves = game_state.get_available_start_tables()
            if len(moves) > 0:
                return UtilMethods.translate_move_to_pair(moves[0])
        winning_statistics = dict()
        own_symbol = game_state.get_current_player()
        possible_moves = game_state.get_available_moves()
        for move in possible_moves:
            winning_statistics[move] = (0, 1)  # set games played to 1 to avoid division by zero error

        for i in range(self.big_n):
            simulated_game = game_state.deepcopy()
            first_played_move, won = self.play_random_game(own_symbol, simulated_game)
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
            # print("bottom")
            return Nijssen07Heuristic.heuristic(game_state.get_current_player(), game_state)
        val = alpha
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            val = max({val, -1 * PlayerAlphaBetaPruning.value(next_state, depth-1, -beta, -alpha)})
            if val >= beta:
                return val
            alpha = max({val, alpha})
        return val

    def get_move(self, game_state: Othello):
        best_val = PlayerAlphaBetaPruning.value(game_state, self.search_depth)
        print(f"Best Val: {best_val}")
        next_states = dict()
        for move in game_state.get_available_moves():
            next_state = game_state.deepcopy()
            next_state.play_position(move)
            next_states[move] = next_state
        good_moves = list()
        for move in next_states.keys():
            if -1 * PlayerAlphaBetaPruning.value(next_states[move], self.search_depth) == best_val:
                good_moves.append(move)
        return good_moves[random.randrange(len(good_moves))]
