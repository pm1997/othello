from Player import Player
from OthelloGame import OthelloGame
from StateForecastTree import StateForecastTree
from Constants import MAX_FORECAST


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        self.new_othello = None
        self.state_root_tree = StateForecastTree(game_reference.get_turn_number(),
                                                 len(game_reference.get_board()), None)

        print("Created new Forecast Turns AI Player")

    def play(self):

        turn_number = self._game_reference.get_turn_number()
        old_board = self._game_reference.get_board()

        turn_number -= 1
        limit = turn_number + MAX_FORECAST

        self.new_othello = OthelloGame(len(old_board), True)
        new_board = OthelloGame.copy_board(old_board)
        self.new_othello.set_board(new_board)
        self.new_othello.set_turn_number(self._game_reference.get_turn_number())

        # self.new_othello.print_board()
        # available_moves = OthelloGame._compute_moves_and_stones_to_turn(new_board, turn_number + 1).available_moves
        # self.state_root_tree = self.state_root_tree.search_node(turn_number, available_moves)
        self.state_root_tree = None
        if self.state_root_tree is None:
            # print("none+++++++++++++++++++++++++")
            self.state_root_tree = StateForecastTree(turn_number, len(old_board), None)
        self.state_root_tree.parent = None

        self.state_root_tree = self.find_next_moves(self.state_root_tree, turn_number, limit, self.new_othello)
        StateForecastTree.update_stats(self.state_root_tree, (turn_number + 1) % 2)

        # StateForecastTree.print_tree(tree)

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

    def find_next_moves(self, tree, turn_number, limit, new_othello):
        if tree.turn_number == limit:
            # print("limit reached-----------------")
            tree.paths = 1
            return
            # return tree.get_root_node()
        turn_number += 1
        new_othello.set_turn_number(turn_number)
        if len(tree.nodes) == 0:
            tree.game_state = OthelloGame._compute_moves_and_stones_to_turn(new_othello.get_board(), turn_number)

        if len(tree.game_state.available_moves) == 0 and new_othello.game_ends():
            # print("turn end reached--------------")
            winner = OthelloGame.get_winner(new_othello.get_board())
            if turn_number % 2 == winner:
                tree.wins = 1
            else:
                tree.loss = 1
            return
        elif len(tree.game_state.available_moves) == 0:
            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)

            tree.add_node(turn_number, -1, -1, len(temp_board),
                          OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

            self.find_next_moves(tree.nodes[0], turn_number, limit, temp_othello)
        if len(tree.nodes) == len(tree.game_state.available_moves):
            for node in tree.nodes:
                temp_othello = OthelloGame(len(new_othello.get_board()), True)
                temp_board = OthelloGame.copy_board(node.game_state.board)
                temp_othello.set_board(temp_board)
                temp_othello.set_turn_number(turn_number)
                self.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello)
        for (row, column) in tree.game_state.available_moves:

            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)
            temp_othello.set_stone((row, column), True)

            # temp_othello.print_board()

            tree.add_node(turn_number, row, column, len(temp_board),
                          OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

            self.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello)
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
