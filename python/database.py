import os
import numpy as np
from constants import DATABASE_FILE_NAME, PLAYER_ONE, PLAYER_TWO
from Agents.playerRandom import PlayerRandom
from othello import Othello
import multiprocessing as mp


class Database:
    #     0   1   2   3   4   5   6   7
    #   +---+---+---+---+---+---+---+---+
    # 0 | 0 | 1 | 2 | 3 | 3 | 2 | 1 | 0 |
    #   +---+---+---+---+---+---+---+---+
    # 1 | 1 | 4 | 5 | 6 | 6 | 5 | 4 | 1 |
    #   +---+---+---+---+---+---+---+---+
    # 2 | 2 | 5 | 7 | 8 | 8 | 7 | 5 | 2 |
    #   +---+---+---+---+---+---+---+---+
    # 3 | 3 | 6 | 8 | X | X | 8 | 6 | 3 |
    #   +---+---+---+---+---+---+---+---+
    # 4 | 3 | 6 | 8 | X | X | 8 | 6 | 3 |
    #   +---+---+---+---+---+---+---+---+
    # 5 | 2 | 5 | 7 | 8 | 8 | 7 | 5 | 2 |
    #   +---+---+---+---+---+---+---+---+
    # 6 | 1 | 4 | 5 | 6 | 6 | 5 | 4 | 1 |
    #   +---+---+---+---+---+---+---+---+
    # 7 | 0 | 1 | 2 | 3 | 3 | 2 | 1 | 0 |
    #   +---+---+---+---+---+---+---+---+
    _DATABASE_TO_POSITIONS = {0: [(0, 0), (0, 7), (7, 0), (7, 7)],
                              1: [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)],
                              2: [(0, 2), (0, 5), (2, 0), (2, 7), (5, 0), (5, 7), (7, 2), (7, 5)],
                              3: [(0, 3), (0, 4), (3, 0), (3, 7), (4, 0), (4, 7), (7, 3), (7, 4)],
                              4: [(1, 1), (1, 6), (6, 1), (6, 6)],
                              5: [(1, 2), (1, 5), (2, 1), (2, 6), (5, 1), (5, 6), (6, 2), (6, 5)],
                              6: [(1, 3), (1, 4), (3, 1), (3, 6), (4, 1), (4, 6), (6, 3), (6, 4)],
                              7: [(2, 2), (2, 5), (5, 2), (5, 5)],
                              8: [(2, 3), (2, 4), (3, 2), (3, 5), (4, 2), (4, 5), (5, 3), (5, 4)],
                              'X': [(3, 3), (3, 4), (4, 3), (4, 4)]}

    _POSITION_TO_DATABASE = {}
    for (field_type, fields) in _DATABASE_TO_POSITIONS.items():
        for field in fields:
            _POSITION_TO_DATABASE[field] = field_type

    @staticmethod
    def translate_database_to_positions(field_type):
        return Database._DATABASE_TO_POSITIONS[field_type]

    @staticmethod
    def _translate_position_to_database(move):
        return Database._POSITION_TO_DATABASE[move]

    def __init__(self):
        # check if database file exists
        if not os.path.isfile(DATABASE_FILE_NAME):
            self._create_new_database()
        # load csv in self_data as 3 dim. array
        csv = np.loadtxt(DATABASE_FILE_NAME, delimiter=';', dtype='int64')
        self._data = csv.reshape((60, 9, 3))

    def __del__(self):
        """
        store database in file
        """
        # self._store_database()

    def _create_new_database(self):
        """
        Reset stored played / won games
        """
        # write 1.0 in each cell of _data array
        self._data = np.zeros(shape=(60, 9, 3), dtype='int64')
        # save modified array
        self._store_database()

    def _store_database(self):
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
        position = self._translate_position_to_database(move)
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
            # translate move like "a2" to (1,0)
            # move = UtilMethods.translate_move_to_pair(moves[turn_nr])
            # translate move 1,0 to position 8
            position = self._translate_position_to_database(moves[turn_nr])
            # update array at position position
            self.update_field_stat(turn_nr, position, winner)
            # update next move
            turn_nr += 1

    @staticmethod
    def _play_n_random_games(count):
        multi_stats = []
        for i in range(count):
            if i % 100 == 0:
                print(f"Game No: {i}")
            g = Othello()
            g.init_game()
            while not g.game_is_over():
                g.play_position(PlayerRandom.get_move(g))
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
        print("finished merge")


db = Database()
