from othello import Othello
from util import UtilMethods
import random
import sys
import operator
from machine_learning import Database


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
