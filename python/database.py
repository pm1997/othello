import os
import numpy as np
from constants import DATABASE_FILE_NAME, PLAYER_ONE, PLAYER_TWO, DATABASE_TO_POSITIONS, POSITION_TO_DATABASE
from Agents.random import Random
from othello import Othello
import multiprocessing as mp


class Database:

    @staticmethod
    def translate_database_to_positions(field_type):
        return DATABASE_TO_POSITIONS[field_type]

    @staticmethod
    def translate_position_to_database(move):
        return POSITION_TO_DATABASE[move]

    def __init__(self):
        # check if database file exists
        if not os.path.isfile(DATABASE_FILE_NAME):
            self._create_new_database()
        # load csv in self_data as 3 dim. array
        csv = np.loadtxt(DATABASE_FILE_NAME, delimiter=';', dtype='int64')
        self._data = csv.reshape((60, 9, 3))

    def _create_new_database(self):
        """
        Reset stored played / won games
        """
        # write 1.0 in each cell of _data array
        self._data = np.zeros(shape=(60, 9, 3), dtype='int64')
        # save modified array
        self.store_database()

    def store_database(self):
        """
        store database on filesystem
        :return:
        """
        with open(DATABASE_FILE_NAME, 'w') as outfile:
            # write 3 dim. array as list of 2 dim. array's
            for row in self._data:
                # write one row of matrix
                np.savetxt(outfile, row, fmt='%d', delimiter=';')

    def get_likelihood(self, move, turn_nr, current_player):
        """
        calculate chance of winning for given move and turn_number
        :param move: move in available_moves
        :param turn_nr: actual turn_number
        :param current_player: actual player
        :return: chance of winning for given field at the given turn number
        """
        # translate move to position in array
        position = self.translate_position_to_database(move)
        won_games_pl1, won_games_pl2, total_games_played = self._data[turn_nr][position]
        if total_games_played == 0:
            return 0
        if current_player == PLAYER_ONE:
            return won_games_pl1 / total_games_played
        return won_games_pl2 / total_games_played

    def update_field_stat(self, turn_nr, field_type, winner):
        (won_games_pl1, won_games_pl2, total_games_played) = self._data[turn_nr][field_type]
        if winner == PLAYER_ONE:
            won_games_pl1 += 1
        elif winner == PLAYER_TWO:
            won_games_pl2 += 1
        self._data[turn_nr][field_type] = (won_games_pl1, won_games_pl2, total_games_played + 1)

    def update_fields_stats_for_single_game(self, moves, winner):
        # update each move in game
        for turn_nr in range(len(moves)):
            # translate move 1,0 to position 8
            position = self.translate_position_to_database(moves[turn_nr])
            # update array at position position
            self.update_field_stat(turn_nr, position, winner)
            # update next move

    @staticmethod
    def _play_n_random_games(count):
        multi_stats = []
        for i in range(count):
            if i % 100 == 0:
                print(f"Game No: {i}")
            g = Othello()
            g.init_game()
            while not g.game_is_over():
                g.play_position(Random.get_move(g))
            winner = g.get_winner()
            multi_stats.append((g.get_taken_mv(), winner))
        return multi_stats

    def train_db_multi_threaded(self, count):
        number_of_processes = mp.cpu_count()
        pool = mp.Pool(processes=number_of_processes)
        list_of_stats = [pool.apply_async(self._play_n_random_games, args=(count // number_of_processes,))
                         for _ in range(number_of_processes)]
        for single_list in list_of_stats:
            list_of_games = single_list.get()
            for single_game in list_of_games:
                moves, winner = single_game
                self.update_fields_stats_for_single_game(moves, winner)

    def sum_databases(self, file):
        csv = np.loadtxt(file, delimiter=';')
        db1 = csv.reshape((60, 9, 3))
        r1 = 0
        for row in self._data:
            c1 = 0
            for column in row:
                column[0] += db1[r1][c1][0]
                column[1] += db1[r1][c1][1]
                column[2] += db1[r1][c1][2]
                c1 += 1
            r1 += 1
        self.store_database()
        print("finished merge")


db = Database()
