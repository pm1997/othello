from Player import Player
from operator import itemgetter
from OthelloGame import OthelloGame
from StateForecastTree import StateForecastTree
from Constants import MAX_FORECAST


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self._game_reference = game_reference
        old_board = game_reference.get_board()
        self.new_othello = OthelloGame(len(old_board), True)
        new_board = OthelloGame.copy_board(old_board)
        self.new_othello.set_board(new_board)
        self.new_othello.set_turn_number(game_reference.get_turn_number())
        self.state_root_tree = StateForecastTree(self.new_othello.get_turn_number(), None)

        print("Created new Forecast Turns AI Player")

    def play(self):

        turn_number = self._game_reference.get_turn_number()

        self.state_root_tree = self.state_root_tree.search_node(turn_number)
        if self.state_root_tree is None:
            self.state_root_tree = StateForecastTree(turn_number, None)
        self.state_root_tree.parent = None
        limit = turn_number + MAX_FORECAST
        turn_number -= 1
        tree = self.find_next_moves(self.state_root_tree, turn_number, limit, self.new_othello)
        StateForecastTree.update_stats(tree)

        StateForecastTree.print_tree(tree)
        # old code

        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)

    def find_next_moves(self, tree, turn_number, limit, new_othello):
        if tree.turn_number == limit:
            print("limit reached-----------------")
            tree.paths = 1
            return
            # return tree.get_root_node()
        turn_number += 1
        new_othello.set_turn_number(turn_number)
        tree.game_state = OthelloGame._compute_moves_and_stones_to_turn(new_othello.get_board(), turn_number)

        if len(tree.game_state.available_moves) == 0:
            print("turn end reached--------------")
            winner = OthelloGame.get_winner(new_othello.get_board())
            if turn_number % 2 == winner:
                tree.wins = 1
            else:
                tree.loss = 1
            return

        for (x, y) in tree.game_state.available_moves:

            temp_othello = OthelloGame(len(new_othello.get_board()), True)
            temp_board = OthelloGame.copy_board(new_othello.get_board())
            temp_othello.set_board(temp_board)
            temp_othello.set_turn_number(turn_number)
            temp_othello.set_stone((x, y))
            tree.x = x
            tree.y = y
            # temp_othello.print_board()
            tree.add_node(turn_number, x, y, None, None)

            print(str(x + 1) + " " + str(y + 1))
            # new_othello.print_board()
            self.find_next_moves(tree.nodes[len(tree.nodes) - 1], turn_number, limit, temp_othello)
        return tree
