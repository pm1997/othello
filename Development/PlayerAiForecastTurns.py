from Player import Player
from OthelloGame import OthelloGame
from StateForecastTree import StateForecastTree
from Constants import MAX_FORECAST
from Constants import INVALID_CELL
from Constants import MAX_THREADS
# from threading import Thread
# from queue import Queue
from multiprocessing import Pool
# from multiprocessing import Process


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        self.new_othello = None
        self.state_root_tree = StateForecastTree(game_reference.get_turn_number(),
                                                 len(game_reference.get_board()), None)
        self.tread_number = 0

        print("Created new Forecast Turns AI Player")
        print("MAX_FORECAST = " + str(MAX_FORECAST))
        print("MAX_THREADS = " + str(MAX_THREADS))

    def play(self):

        turn_number = self._game_reference.get_turn_number()
        old_board = self._game_reference.get_board()

        turn_number -= 1

        limit = turn_number + MAX_FORECAST

        self.new_othello = OthelloGame(len(old_board), True)
        new_board = OthelloGame.copy_board(old_board)
        self.new_othello.set_board(new_board)
        self.new_othello.set_turn_number(self._game_reference.get_turn_number())

        self.state_root_tree = self.state_root_tree.search_node(new_board, turn_number)
        if self.state_root_tree is None:
            self.state_root_tree = StateForecastTree(turn_number, len(old_board), None)
        self.state_root_tree.parent = None

        self.state_root_tree = self.find_next_moves(self.state_root_tree, turn_number, limit, self.new_othello, 0)
        StateForecastTree.update_stats(self.state_root_tree, (turn_number + 1) % 2)

        print("Paths: " + str(self.state_root_tree.paths))
        # StateForecastTree.print_tree(self.state_root_tree)

        # print("global min: " + str(tree.min_points) + " max: " + str(tree.max_points))

        # for node in tree.nodes:
        #    print("----------------")
        #    print(node.turn_number)
        #    print("row:" + str(node.row + 1) + " column:" + str(node.column + 1))
        #    print("min: " + str(node.min_points) + " max: " + str(node.max_points))
        #    print("win: " + str(node.wins) + " lose: " + str(node.loss))
        #    print("paths: " + str(node.paths))
        #    print("----------------")
        #    print(" + ")

        (best_row, best_column) = PlayerAiForecastTurns.get_best_move(self.state_root_tree)
        self._game_reference.set_stone((best_row, best_column))

    @staticmethod
    def use_threads(tree, turn_number, limit, new_othello, tread_number):
        print("Treads used")

        if tree.turn_number == limit:
            # print("limit reached-----------------")
            tree.paths = 1
            return

        turn_number += 1
        new_othello.set_turn_number(turn_number)
        print("Treads used2")
        if len(tree.nodes) == 0:
            tree.game_state = OthelloGame._compute_moves_and_stones_to_turn(new_othello.get_board(), turn_number)
        print("Treads used3")
        if len(tree.game_state.available_moves) == 0 and new_othello.game_ends():
            # print("turn end reached--------------")
            winner = OthelloGame.get_winner(new_othello.get_board())
            if turn_number % 2 == winner:
                tree.wins = 1
            else:
                tree.loss = 1
            return
        elif len(tree.game_state.available_moves) == 0:
            print("Treads used4")
            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)
            temp_othello.set_stone(INVALID_CELL, True)

            tree.add_node(turn_number, INVALID_CELL[0], INVALID_CELL[1], len(temp_board),
                          OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

            PlayerAiForecastTurns.find_next_moves(tree.nodes[0], turn_number, limit, temp_othello, tread_number)
        elif len(tree.nodes) == len(tree.game_state.available_moves):
            print("Treads used5")
            for node in tree.nodes:
                temp_othello = OthelloGame(len(new_othello.get_board()), True)
                temp_board = OthelloGame.copy_board(node.game_state.board)
                temp_othello.set_board(temp_board)
                temp_othello.set_turn_number(turn_number)
                PlayerAiForecastTurns.find_next_moves(node, turn_number, limit, temp_othello, tread_number)
        else:
            # threads_list = list()
            print("Treads used6")
            print("before init")
            # a1 = []
            p_pool = []
            # temp_othello = [OthelloGame(len(new_othello.get_board()), True) for _ in
            #                range(len(tree.game_state.available_moves))]
            print("array inited")
            # index = 0
            # res = None
            pool = Pool(processes=4)
            for (row, column) in tree.game_state.available_moves:
                temp_othello = OthelloGame(len(new_othello.get_board()), True)
                temp_board = OthelloGame.copy_board(new_othello.get_board())
                temp_othello.set_board(temp_board)
                temp_othello.set_turn_number(turn_number)
                temp_othello.set_stone((row, column), True)

                tree.add_node(turn_number, row, column, len(temp_board),
                              OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(),
                                                                            turn_number))
                tread_number += 1

                p_pool.append(pool.apply_async(PlayerAiForecastTurns.find_next_moves,
                                               (tree, turn_number, limit, new_othello, tread_number)))
                # a1.append((tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello, tread_number))

                # p = Process(target=PlayerAiForecastTurns.find_next_moves,
                #            args=(tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello, tread_number))
                # p.start()
                # p_pool.append(p)
                # index += 1
            #    if self.tread_number < MAX_THREADS:
            #        self.tread_number += 1
            #        t1 = ThreadWithReturnValue(target=self.find_next_moves, args=(tree.nodes[len(tree.nodes) - 1],
            #                                                                      turn_number, limit, temp_othello))
            #        threads_list.append(t1)
            #    else:
                #
                # PlayerAiForecastTurns.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number,
            #           limit, temp_othello, tread_number)
            # print(a1)

            print("start pool")

            pool.close()
            print("start pool2")
            pool.join()
            print("start pool3")
            # for p1 in p_pool:
            #    p1.join()

            # print(res.get(timeout=3))  # prints "400"
            # pool.map(self.multi_process, a1)
            print("after pool")
            # for t in threads_list:
            #    t.join()
        return tree

    @staticmethod
    def multi_process(object1):
        (tree, turn_number, limit, new_othello, tread_number) = object1
        # temp_othello = OthelloGame(len(new_othello.get_board()), True)
        # temp_board = OthelloGame.copy_board(new_othello.get_board())
        # temp_othello.set_board(temp_board)
        # temp_othello.set_turn_number(turn_number)
        # temp_othello.set_stone((row, column), True)

        # tree.add_node(turn_number, row, column, len(temp_board),
        #              OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))
        return PlayerAiForecastTurns.find_next_moves(tree, turn_number, limit, new_othello, tread_number)

    @staticmethod
    def find_next_moves(tree, turn_number, limit, new_othello, tread_number):
        print("Treads used13")
        if tree.turn_number == limit:
            # print("limit reached-----------------")
            tree.paths = 1
            return
            # return tree.get_root_node()

        print("Treads used7")
        if limit - turn_number > 2 and tread_number < MAX_THREADS:
            print("use new process +++++++++")
            return PlayerAiForecastTurns.use_threads(tree, turn_number, limit, new_othello, tread_number)

        turn_number += 1
        new_othello.set_turn_number(turn_number)
        if len(tree.nodes) == 0:
            print("Treads used8")
            tree.game_state = OthelloGame._compute_moves_and_stones_to_turn(new_othello.get_board(), turn_number)

        if len(tree.game_state.available_moves) == 0 and new_othello.game_ends():
            # print("turn end reached--------------")
            print("Treads used9")
            winner = OthelloGame.get_winner(new_othello.get_board())
            if turn_number % 2 == winner:
                tree.wins = 1
            else:
                tree.loss = 1
            return
        elif len(tree.game_state.available_moves) == 0:
            print("Treads used10")
            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)
            temp_othello.set_stone(INVALID_CELL, True)

            tree.add_node(turn_number, INVALID_CELL[0], INVALID_CELL[1], len(temp_board),
                          OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

            PlayerAiForecastTurns.find_next_moves(tree.nodes[0], turn_number, limit, temp_othello, tread_number)
        elif len(tree.nodes) == len(tree.game_state.available_moves):
            print("Treads used11")
            for node in tree.nodes:
                temp_othello = OthelloGame(len(new_othello.get_board()), True)
                temp_board = OthelloGame.copy_board(node.game_state.board)
                temp_othello.set_board(temp_board)
                temp_othello.set_turn_number(turn_number)
                PlayerAiForecastTurns.find_next_moves(node, turn_number, limit, temp_othello, tread_number)
        else:
            print("Treads used12")
            for (row, column) in tree.game_state.available_moves:
                temp_othello = OthelloGame(len(new_othello.get_board()), True)
                temp_board = OthelloGame.copy_board(new_othello.get_board())
                temp_othello.set_board(temp_board)
                temp_othello.set_turn_number(turn_number)
                temp_othello.set_stone((row, column), True)

                # OthelloGame.print_board(temp_othello._board, temp_othello._player_print_symbol)

                tree.add_node(turn_number, row, column, len(temp_board),
                              OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

                PlayerAiForecastTurns.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit,
                                                      temp_othello, tread_number)
        return tree

    @staticmethod
    def get_best_move(tree):
        if len(tree.nodes) != 0:

            best_row = tree.nodes[0].row
            best_column = tree.nodes[0].column

            best_row2 = best_row
            best_column2 = best_column

            max_win = 0
            min_loss = 2000
            max_points = 0
            paths = None
            # paths2 = None
            for node in tree.nodes:
                if node.wins >= max_win and (paths is None or node.paths < paths):
                    max_win = node.wins
                    best_row = node.row
                    best_column = node.column
                    paths = node.paths

                if node.loss <= min_loss and node.max_points >= max_points:
                        # (paths2 is None or node.paths * 3 < paths2 * 2):
                    max_points = node.max_points
                    min_loss = node.loss
                    best_row2 = node.row
                    best_column2 = node.column
                    # paths2 = node.paths

            if max_win > 0:
                return best_row, best_column
            if min_loss == 0:
                return best_row2, best_column2

            best_row = tree.nodes[0].row
            best_column = tree.nodes[0].column
            loss_vs_path = tree.nodes[0].loss / tree.nodes[0].paths
            max_points = 0
            for node in tree.nodes:

                value = node.loss / node.paths

                if value < loss_vs_path or (value <= loss_vs_path and node.max_points >= max_points):
                    if node.max_points >= max_points:
                        max_points = node.max_points
                    loss_vs_path = value
                    best_row = node.row
                    best_column = node.column
            return best_row, best_column

# class ThreadWithReturnValue(object):
#    def __init__(self, target=None, args=(), **kwargs):
#        self._que = Queue()
#        self._t = Thread(target=lambda q, arg1, kwargs1: q.put(target(*arg1, **kwargs1)),
#                         args=(self._que, args, kwargs),)
#        self._t.start()#
#
#    def join(self):
#        self._t.join()
#        return self._que.get()
