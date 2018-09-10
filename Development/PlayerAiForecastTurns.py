from Player import Player
from operator import itemgetter
from OthelloGame import OthelloGame
from Constants import BOARD_SIZE


class PlayerAiForecastTurns(Player):
    def __init__(self, game_reference):
        Player.__init__(self, game_reference)
        self.state_storage = list()
        self._game_reference = game_reference
        print("Created new Forecast Turns AI Player")

    def play(self):

        new_othello = OthelloGame(BOARD_SIZE, True)
        old_board = self._game_reference.get_board()
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

        print(tree.value)
        print("++")
        tree.print_tree(tree.get_root_node())

        tree = StateForecastTree.delete_parent(tree, tree.nodes[1])

        print("Finished")

        print(tree.value)
        print("++")
        tree.print_tree(tree.get_root_node())

        # old code

        positions_to_turn = self._game_reference.get_stones_to_turn()
        number_inversions = [(position, len(positions_to_turn[position])) for position in positions_to_turn]

        position_with_most_inversions = max(number_inversions, key=itemgetter(1))[0]
        self._game_reference.set_stone(position_with_most_inversions)

    def find_next_moves(self):
        pass


class StateForecastTree:
    def __init__(self, value, game_state, parent=None):
        self.value = value
        self.nodes = []
        self.parent = parent
        self.game_state = game_state

    def delete(self, stop_node):
        self.parent = None
        if self is stop_node:
            print("stop node reached" + str(self.value))
            return self

        val = None
        for nodes in self.nodes:
            val2 = nodes.delete(stop_node)
            if val2 is not None:
                val = val2
        del self
        return val

    def add_node(self, node, game_state):
        self.nodes.append(StateForecastTree(node, game_state, self))

    def get_depth(self):
        if self.parent is None:
            return 1
        return self.parent.get_depth() + 1

    def delete_parent(self, actual_node):
        if self.parent is not None:
            return self.parent.delete_parent(actual_node)

        # top level reached
        return StateForecastTree.delete_nodes(self, actual_node)

    def get_root_node(self):
        if self.parent is not None:
            return self.parent.get_root_node()
        return self

    @staticmethod
    def print_tree(root):
        for node in root.nodes:
            print(node.value)
            print("--")
            StateForecastTree.print_tree(node)

    @staticmethod
    def delete_nodes(node, stop_node):
        return node.delete(stop_node)
