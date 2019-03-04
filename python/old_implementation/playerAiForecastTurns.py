from player import Player

from othelloGame import OthelloGame

from utilTreeForecastTurns import UtilTreeForecastTurns

from constants import MAX_FORECAST
from constants import INVALID_CELL
from constants import MAX_THREADS

from multiprocessing import Pool


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        self.new_othello = None
        self.state_root_tree = UtilTreeForecastTurns(game_reference.get_turn_number(),
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

        new_board = OthelloGame.copy_board(old_board)

        self.state_root_tree = self.state_root_tree.search_node(new_board, turn_number)
        if self.state_root_tree is None:
            self.state_root_tree = UtilTreeForecastTurns(turn_number, len(old_board), None)
        self.state_root_tree.parent = None

        self.state_root_tree = PlayerAiForecastTurns.use_threads(self.state_root_tree, turn_number, limit, new_board, 0)
        if self.state_root_tree is None:
            print("Error: tree is none")
            # force cancel of game
            self._game_reference.set_stone(INVALID_CELL)

        UtilTreeForecastTurns.update_stats(self.state_root_tree, (turn_number + 1) % 2)

        (best_row, best_column) = PlayerAiForecastTurns.get_best_move(self.state_root_tree)
        self._game_reference.set_stone((best_row, best_column))

    # static methods ------------------------------------------------------------------------------------------

    @staticmethod
    def find_next_moves(tree, turn_number, limit, board, tread_number):
        if tree.turn_number == limit:
            tree.paths = 1
            return

        turn_number += 1
        if len(tree.nodes) == 0:
            tree.game_state = OthelloGame.compute_moves_and_stones_to_turn(board, turn_number)

        if len(tree.game_state.available_moves) == 0:
            if OthelloGame.game_ends(board, turn_number):
                winner = OthelloGame.get_winner(board)
                if turn_number % 2 == winner:
                    tree.wins = 1
                else:
                    tree.loss = 1
                return
            else:
                new_board = OthelloGame.copy_board(board)

                tree.add_node(turn_number, INVALID_CELL[0], INVALID_CELL[1], len(new_board),
                              OthelloGame.compute_moves_and_stones_to_turn(new_board, turn_number))

                PlayerAiForecastTurns.find_next_moves(tree.nodes[0], turn_number, limit, new_board, tread_number)
        elif len(tree.nodes) == len(tree.game_state.available_moves):
            for node in tree.nodes:
                new_board = OthelloGame.copy_board(node.game_state.board)
                PlayerAiForecastTurns.find_next_moves(node, turn_number, limit, new_board, tread_number)
        else:
            for (row, column) in tree.game_state.available_moves:
                new_board = OthelloGame.set_stone_static(OthelloGame.copy_board(board), turn_number, (row, column))

                tree.add_node(turn_number, row, column, len(new_board),
                              OthelloGame.compute_moves_and_stones_to_turn(new_board, turn_number))

                PlayerAiForecastTurns.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit,
                                                      new_board, tread_number)
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
            for node in tree.nodes:
                if node.wins >= max_win and (paths is None or node.paths < paths):
                    max_win = node.wins
                    best_row = node.row
                    best_column = node.column
                    paths = node.paths

                if node.loss <= min_loss and node.max_points >= max_points:
                    max_points = node.max_points
                    min_loss = node.loss
                    best_row2 = node.row
                    best_column2 = node.column

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

    @staticmethod
    def use_threads(tree, turn_number, limit, board, tread_number):
        if tree.turn_number == limit:
            tree.paths = 1
            print("Error: limit must be bigger than 0!")
            return None

        turn_number += 1
        tree.game_state = OthelloGame.compute_moves_and_stones_to_turn(board, turn_number)
        a1 = []
        if len(tree.game_state.available_moves) == 1:
            print("only one turn left!")
            for (row, column) in tree.game_state.available_moves:

                new_board = OthelloGame.set_stone_static(OthelloGame.copy_board(board), turn_number, (row, column))

                tree.add_node(turn_number, row, column, len(new_board),
                              OthelloGame.compute_moves_and_stones_to_turn(new_board, turn_number))
                PlayerAiForecastTurns.find_next_moves(tree.nodes[0], turn_number, limit, new_board, tread_number)
            return tree

        elif len(tree.game_state.available_moves) == 0:
            print("no valid turn left")
        for (row, column) in tree.game_state.available_moves:
            new_board = OthelloGame.set_stone_static(OthelloGame.copy_board(board), turn_number, (row, column))

            tree.add_node(turn_number, row, column, len(new_board),
                          OthelloGame.compute_moves_and_stones_to_turn(new_board, turn_number))
            tread_number += 1

            a1.append((tree.nodes[len(tree.nodes) - 1], turn_number, limit, new_board, tread_number))

        pool = Pool(processes=len(a1))
        # pool = Pool(processes=8)
        results = []
        for i in range(0, len(a1)):
            results.append(pool.apply_async(PlayerAiForecastTurns.find_next_moves, args=(a1[i][0], turn_number,
                                                                                         limit, a1[i][3],
                                                                                         tread_number)))

        results = [r.get() for r in results]
        pool.close()
        tree.set_nodes([])
        for subtree in results:
            if subtree is not None:
                    # UtilTreeForecastTurns.print_tree(subtree)
                tree.add_tree(subtree)
        return tree
