from othello import Othello
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
