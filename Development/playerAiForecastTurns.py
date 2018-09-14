from player import Player
from othelloGame import OthelloGame
from utilTreeForecastTurns import UtilTreeForecastTurns
from constants import MAX_FORECAST
from error import InvalidTurnError


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        self.new_othello = None
        self.state_root_tree = UtilTreeForecastTurns(game_reference.get_turn_number(), None)

        print("Created new AI Player - Forecast Turns")

    def play(self):

        turn_number = self._game_reference.get_turn_number()

        # self.state_root_tree = self.state_root_tree.search_node(turn_number)
        # if self.state_root_tree is None:
        self.state_root_tree = UtilTreeForecastTurns(turn_number, None)
        self.state_root_tree.parent = None

        turn_number -= 1
        limit = turn_number + MAX_FORECAST

        old_board = self._game_reference.get_board()
        self.new_othello = OthelloGame(len(old_board), True)
        new_board = OthelloGame.copy_board(old_board)
        self.new_othello.set_board(new_board)
        self.new_othello.set_turn_number(self._game_reference.get_turn_number())

        tree = self.find_next_moves(self.state_root_tree, turn_number, limit, self.new_othello)
        UtilTreeForecastTurns.update_stats(tree, (turn_number + 1) % 2)

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

        if len(tree.nodes) != 0:

            best_row = tree.nodes[0].row
            best_column = tree.nodes[0].column

            best_row2 = best_row
            best_column2 = best_column

            max_win = 0
            min_loss = 2000
            max_points = 0
            for node in tree.nodes:
                if node.wins > max_win:
                    max_win = node.wins
                    best_row = node.row
                    best_column = node.column

                if node.loss <= min_loss and node.max_points > max_points:
                    max_points = node.max_points
                    min_loss = node.loss
                    best_row2 = node.row
                    best_column2 = node.column

            if max_win > 0:
                self._game_reference.set_stone((best_row, best_column))
                return

            if min_loss < 10:
                self._game_reference.set_stone((best_row2, best_column2))
                return

            print("use almost old code -------------------------------------------")

            # positions_to_turn = self.new_othello.get_stones_to_turn()
            # number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

            # (best_row, best_column) = max(number_inversions, key=itemgetter(1))[0]

            best_row = tree.nodes[0].row
            best_column = tree.nodes[0].column
            max_points = tree.nodes[0].max_points
            for node in tree.nodes:
                if node.max_points > max_points:
                    best_row = node.row
                    best_column = node.column

            self._game_reference.set_stone((best_row, best_column))

    def find_next_moves(self, tree, turn_number, limit, new_othello):
        if tree.turn_number == limit:
            # print("limit reached-----------------")
            tree.paths = 1
            return
            # return tree.get_root_node()
        turn_number += 1
        new_othello.set_turn_number(turn_number)
        tree.game_state = OthelloGame._compute_moves_and_stones_to_turn(new_othello.get_board(), turn_number)

        if len(tree.game_state.available_moves) == 0:
            # print("turn end reached--------------")
            winner = OthelloGame.get_winner(new_othello.get_board())
            if turn_number % 2 == winner:
                tree.wins = 1
            else:
                tree.loss = 1
            return

        for (row, column) in tree.game_state.available_moves:

            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)
            temp_othello.set_stone((row, column), True)

            # temp_othello.print_board()

            tree.add_node(turn_number, row, column,
                          OthelloGame._compute_moves_and_stones_to_turn(temp_othello.get_board(), turn_number))

            self.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello)
        return tree
