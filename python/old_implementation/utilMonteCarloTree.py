from othelloGame import OthelloGame

from constants import BOARD_SIZE
from constants import EMPTY_CELL
from constants import INVALID_CELL

#from secrets import choice
from random import sample


class UtilMonteCarloTree:
    def __init__(self, turn_number, size=BOARD_SIZE, row=INVALID_CELL[0], column=INVALID_CELL[1], game_state=None, parent=None):
        self.turn_number = turn_number
        self.row = row
        self.column = column
        self.paths = 0
        self.wins = 0
        self.loss = 0
        self.max_points = 0
        self.min_points = int(size * size)
        self.nodes = []
        self.parent = parent
        self.game_state = game_state

    def add_node(self, turn_number, row, column, size, game_state=None):
        self.nodes.append(UtilMonteCarloTree(turn_number, size, row, column, game_state, self))

    def add_tree(self, tree):
        self.nodes.append(tree)
        self.nodes[len(self.nodes) - 1].parent = self

    def get_root_node(self):
        if self.parent is not None:
            return self.parent.get_root_node()
        return self

    def search_node(self, board, turn_number):
        for node in self.nodes:
            if node.game_state is not None:
                if board == node.game_state.board and node.turn_number == turn_number:
                    return node
                if UtilMonteCarloTree.check_boards(board, node.game_state.board):
                    return node.search_node(board, turn_number)
        return None

    def set_nodes(self, nodes):
        self.nodes = nodes
        for node in self.nodes:
            node.parent = self

    def monte_carlo(self, limit):
        available_moves = self.game_state.available_moves
        for possible_move in self.game_state.available_moves:
            if limit > 0:
                new_board = OthelloGame.copy_board(self.game_state.board)
                OthelloGame.set_stone_static(new_board, self.game_state.turn_number, possible_move)
                new_game_state = OthelloGame.compute_moves_and_stones_to_turn(new_board,
                                                                              self.game_state.turn_number
                                                                              + 1,
                                                                              0)
                self.add_node(self.game_state.turn_number + 1, possible_move[0], possible_move[1], BOARD_SIZE,
                              new_game_state)
                self.nodes[len(self.nodes) - 1].monte_carlo(1)
                limit -= 1

        if 2 * len(available_moves) < limit:
            limit -= 2 * len(available_moves)
            for node in self.nodes:
            #for possible_move in self.game_state.available_moves:
                # new_board = OthelloGame.copy_board(self.game_state.board)
                # OthelloGame.set_stone_static(new_board, self.game_state.turn_number, possible_move)
                # new_game_state = OthelloGame.compute_moves_and_stones_to_turn(new_board,
                #                                                               self.game_state.turn_number
                #                                                               + 1,
                #                                                               0)
                # self.add_node(self.game_state.turn_number + 1, possible_move[0], possible_move[1], BOARD_SIZE,
                #               new_game_state)
                #self.nodes[len(self.nodes) - 1].monte_carlo(2)
                node.monte_carlo(2)
        if len(available_moves) > 0:
            while limit > 0:
                if len(self.nodes) > 0:
                    for node in self.nodes:
                        (node.wins, node.loss, node.paths, node.min_points, node.max_points) = self.update_stats(node,
                                                                                                                 0)
                    (min_path, min_path_node, max_path, max_path_node) = self.get_min_max_path()
                    if (max_path - min_path) > 5:
                        if limit > 2:
                            limit -= 2
                            min_path_node.monte_carlo(2)
                    (min_win, min_win_node, max_win, max_win_node) = self.get_min_max_win()
                    (min_loss, min_loss_node, max_loss, max_loss_node) = self.get_min_max_loss()
                    if 2 * max_win >= max_win_node.paths:
                        max_win_node.monte_carlo(1)
                        limit -= 1
                    if limit > 0 and min_loss * 2 < min_loss_node.paths:
                        limit -= 1
                        min_loss_node.monte_carlo(1)
                    if limit > 0:
                        limit -= 1
                        sample(self.nodes, 1)[0].monte_carlo(1)
                else:

                    limit -= 1
                    possible_move = sample(available_moves, 1)[0]
                    new_board = OthelloGame.copy_board(self.game_state.board)
                    OthelloGame.set_stone_static(new_board, self.game_state.turn_number, possible_move)
                    new_game_state = OthelloGame.compute_moves_and_stones_to_turn(new_board,
                                                                                  self.game_state.turn_number
                                                                                  + 1,
                                                                                  0)
                    self.add_node(self.game_state.turn_number + 1, possible_move[0], possible_move[1], BOARD_SIZE,
                                  new_game_state)
                    self.nodes[len(self.nodes) - 1].monte_carlo(1)

        elif self.game_state.number_of_passes < 2:
            new_game_state = OthelloGame.compute_moves_and_stones_to_turn(self.game_state.board,
                                                                          self.game_state.turn_number + 1,
                                                                          self.game_state.number_of_passes + 1)
            self.add_node(self.game_state.turn_number + 1, -1, -1, BOARD_SIZE, new_game_state)
            self.nodes[len(self.nodes) - 1].monte_carlo(limit)
        for node in self.nodes:
            (node.wins, node.loss, node.paths, node.min_points, node.max_points) = self.update_stats(node, 0)

    def get_min_max_path(self):
        min_path = -1
        max_node = self
        min_node = self
        max_path = -1
        for node in self.nodes:
            if node.paths >= max_path:
                max_path = node.paths
                max_node = node
            if node.paths <= min_path or min_path == -1:
                min_path = node.paths
                min_node = node
        return min_path, min_node, max_path, max_node

    def get_min_max_loss(self):
        min_loss = -1
        max_node = self
        min_node = self
        max_loss = -1
        for node in self.nodes:
            if node.loss >= max_loss:
                max_loss = node.loss
                max_node = node
            if node.loss <= min_loss or min_loss == -1:
                min_loss = node.loss
                min_node = node
        return min_loss, min_node, max_loss, max_node

    def get_min_max_win(self):
        min_win = -1
        max_node = self
        min_node = self
        max_win = -1
        for node in self.nodes:
            if node.wins >= max_win:
                max_win = node.wins
                max_node = node
            if node.wins <= min_win or min_win == -1:
                min_win = node.wins
                min_node = node
        return min_win, min_node, max_win, max_node

    def get_best_move(self, player):
        (_, _, max_win, max_node) = self.get_min_max_win()
        (_, _, max_loss, max_loss_node) = self.get_min_max_win()
        if player == 0:
            return max_node.row, max_node.column
        return max_loss_node.row, max_loss_node.column

    # static methods ------------------------------------------------------------------------------------------

    @staticmethod
    def check_boards(search_board, actual_board):
        board_size = len(search_board)
        for row in range(board_size):
            for column in range(board_size):
                if search_board[row][column] == EMPTY_CELL and actual_board[row][column] != EMPTY_CELL:
                    return False
        return True

    @staticmethod
    def print_tree(root):
        for node in root.nodes:
            print("----------------")
            print(node.turn_number)
            print("row:" + str(node.row + 1) + " column:" + str(node.column + 1))
            print("min: " + str(node.min_points) + " max: " + str(node.max_points))
            print("paths: " + str(node.paths))
            print("win: " + str(node.wins) + " lose: " + str(node.loss))
            print("----------------")
            print(" + ")
            UtilMonteCarloTree.print_tree(node)

    @staticmethod
    def update_stats(tree, player):
        tree.paths = 0
        tree.min_points = BOARD_SIZE * BOARD_SIZE
        tree.max_points = 0
        if len(tree.nodes) == 0:  # and tree.game_state is not None and tree.game_state.board is not None:
            stats = OthelloGame.get_stats(tree.game_state.board)
            tree.max_points = stats[tree.turn_number % 2]
            tree.min_points = stats[tree.turn_number % 2]
            if stats[0] != stats[1]:
                if stats[player] > stats[(player + 1) % 2]:
                    tree.wins = 1
                else:
                    tree.loss = 1

            tree.paths = 1
        for node in tree.nodes:
            data = UtilMonteCarloTree.update_stats(node, player)
            tree.wins += data[0]
            tree.loss += data[1]
            tree.paths += data[2]
            tree.min_points = min(tree.min_points, data[3])
            tree.max_points = max(tree.max_points, data[4])
        return tree.wins, tree.loss, tree.paths, tree.min_points, tree.max_points
