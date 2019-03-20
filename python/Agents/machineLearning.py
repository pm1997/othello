from othello import Othello
from util import UtilMethods
import random
import sys
import operator
from ml_database import ml_database
import multiprocessing as mp
from Agents.monteCarlo import PlayerMonteCarlo


class PlayerMachineLearning:
    # store available moves (top level) in dictionary
    move_probability = dict()

    def __init__(self, big_number=0, use_multiprocessing=None):
        if big_number != 0:
            self.big_n = big_number
        else:
            self.big_n = UtilMethods.get_integer_selection("[Player Machinelearning] Select Number of Simulated Games", 100, sys.maxsize)

        if use_multiprocessing is None:
            self.use_multiprocessing = UtilMethods.get_boolean_selection("[Player Machinelearning] Use Multiprocessing?")
        else:
            self.use_multiprocessing = use_multiprocessing
        # init machine learning database
        # self.db.init_database()

    @staticmethod
    def get_weighted_random(possible_moves, turn_nr):
        """
        get weighted random move: prefer moves with higher chance of winning
        :param possible_moves: list of available moves in current game state
        :param turn_nr: actual turn number
        :return: random move
        """
        prob_sum = 0.0
        # get sum of all chances in possible moves
        for move in possible_moves:
            prob_sum += ml_database.get_likelihood(move, turn_nr)

        # choose a random float between 0 and calculated sum
        chose = random.uniform(0.0, prob_sum)

        move_nr = 0
        prob_sum = 0.0
        # iterate over possible move to get
        for move in possible_moves:
            move_nr += 1
            prob_sum += ml_database.get_likelihood(move, turn_nr)
            if prob_sum >= chose:
                # if prob_sum >= chose return move
                return move
        # return last possible move because it's the only remaining move
        return possible_moves[-1]

    def play_weighted_random_game(self, own_symbol, simulated_game):
        """
        :param own_symbol: player symbol (PLAYER_ONE, PLAYER_TWO)
        :param simulated_game: copy of game state
        :return: won, first_move, taken_moves
            won: player wins random game
            first_move: root move of player
            taken_moves: list of all taken moves in simulated game
        """
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

    def play_n_weighted_random_games(self, own_symbol, game_state: Othello, number_of_games):
        winning_statistics = dict()
        # Get the set of legal moves
        possible_moves = game_state.get_available_moves()
        # Add a pair of (won_games, times_played) to the dictionary for each legal move
        for move in possible_moves:
            winning_statistics[move] = (1, 1)  # set games played to 1 to avoid division by zero error

        database_info = list()
        # Simulate big_n games
        for _ in range(number_of_games):
            simulated_game = game_state.deepcopy()
            # select a weighted random move and play remaining game
            won, first_played_move, played_moves = self.play_weighted_random_game(own_symbol, simulated_game)
            # Access the statistics stored for the move selected in the random game
            (won_games, times_played) = winning_statistics[first_played_move]
            # update move stats of actual big_n games
            winning_statistics[first_played_move] = (won_games + won, times_played + 1)
            database_info.append((played_moves, won))

        return winning_statistics, database_info

    def get_move(self, game_state: Othello):
        """
        interface function of all players
        :param game_state: actual game state
        :return: best move in available moves
        """
        # init variables
        own_symbol = game_state.get_current_player()
        move_stats = dict()
        self.move_probability.clear()

        if not self.use_multiprocessing:
            move_stats, db_info = self.play_n_weighted_random_games(own_symbol, game_state, self.big_n)
            for i in range(len(db_info)):
                (played_moves, won) = db_info[i]
                ml_database.update_all_weights(played_moves, won)
        else:
            number_of_processes = mp.cpu_count()
            pool = mp.Pool(processes=number_of_processes)
            list_of_returns = [pool.apply_async(PlayerMachineLearning.play_n_weighted_random_games, args=(self, own_symbol, game_state.deepcopy(), self.big_n//number_of_processes)) for _ in range(number_of_processes)]
            # Base case
            (winning_info, db_info) = list_of_returns[0].get()
            move_stats = winning_info
            for i in range(len(db_info)):
                (played_moves, won) = db_info[i]
                ml_database.update_all_weights(played_moves, won)
            # Other cases
            for single_return in list_of_returns[1:]:
                (winning_info, db_info) = single_return.get()
                PlayerMonteCarlo.combine_statistic_dicts(move_stats, winning_info)
                for i in range(len(db_info)):
                    (played_moves, won) = db_info[i]
                    ml_database.update_all_weights(played_moves, won)
            pool.close()

        # play big_n games
        for i in range(self.big_n):
            # copy game and update database
            simulated_game = game_state.deepcopy()
            # select a weighted random move and play remaining game
            won, first_played_move, played_moves = self.play_weighted_random_game(own_symbol, simulated_game)
            # Access the statistics stored for the move selected in the random game
            (won_games, times_played) = move_stats[first_played_move]
            # update move stats of actual big_n games
            move_stats[first_played_move] = (won_games + won, times_played + 1)
            ml_database.update_all_weights(played_moves, won)

        # save database to csv file
        # self.db.store_database()

        for single_move in move_stats:
            # calculate percentage of won games
            (games_won, times_played) = move_stats[single_move]
            self.move_probability[single_move] = games_won / times_played

        # get move with highest winning percentage
        selected_move = max(self.move_probability.items(), key=operator.itemgetter(1))[0]
        return selected_move

    def get_move_probability(self, move):
        """
        :param move: given move in available moves
        :return: winning change of move
        """
        return self.move_probability[move]
