from Player import Player
from operator import itemgetter
from OthelloGame import OthelloGame
from Constants import BOARD_SIZE
from StateForecastTree import StateForecastTree


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self.state_storage = list()
        self._game_reference = game_reference
        print("Created new Forecast Turns AI Player")

    def play(self):

        old_board = self._game_reference.get_board()

        new_othello = OthelloGame(len(old_board), True)

        new_board = OthelloGame.copy_board(old_board)
        new_board[0][0] = 0
        new_othello.set_board(new_board)

        print("old board:")
        self._game_reference.print_board()

        print("new instance:")
        new_othello.print_board()

        tree = StateForecastTree(1, None, None)

        tree.add_node(2, None)
        print("Tree2")
        tree.add_node(3, None)

        tree.nodes[1].add_node(5, None)

        print(tree.turn_number)
        print("++")
        tree.print_tree(tree.get_root_node())

        tree = StateForecastTree.delete_parent(tree, tree.nodes[1].turn_number)

        print("Finished")

        print(tree.turn_number)
        print("++")
        tree.print_tree(tree.get_root_node())

        # old code

        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)

    def find_next_moves(self):
        pass
