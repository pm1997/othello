from Constants import BOARD_SIZE
from OthelloGame import OthelloGame


class StateForecastTree:
    def __init__(self, turn_number, size, game_state=None, parent=None):
        self.turn_number = turn_number
        self.row = 0  # int(BOARD_SIZE / 2)
        self.column = 0  # int(BOARD_SIZE / 2)
        self.paths = 0
        self.wins = 0
        self.loss = 0
        self.max_points = 0
        self.min_points = int(size * size)
        self.nodes = []
        self.parent = parent
        self.game_state = game_state

    def delete(self, stop_node):
        self.parent = None
        if self.turn_number == stop_node:
            print("stop node reached" + str(self.turn_number))
            return self

        val = None
        for nodes in self.nodes:
            val2 = nodes.delete(stop_node)
            if val2 is not None:
                val = val2
        # del self
        return val

    def add_node(self, turn_number, row, column, size, game_state=None):
        self.nodes.append(StateForecastTree(turn_number, size, game_state, self))
        self.nodes[len(self.nodes) - 1].row = row
        self.nodes[len(self.nodes) - 1].column = column

    def get_depth(self):
        if self.parent is None:
            return 1
        return self.parent.get_depth() + 1

    def delete_parent(self, stop_node_value):
        if self.parent is not None:
            return self.parent.delete_parent(stop_node_value)

        # top level reached
        return StateForecastTree.delete_nodes(self, stop_node_value)

    def get_root_node(self):
        if self.parent is not None:
            return self.parent.get_root_node()
        return self

    def update_parent_node(self, data):
        pass

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
            StateForecastTree.print_tree(node)

    @staticmethod
    def delete_nodes(node, stop_node_value):
        return node.delete(stop_node_value)

    def search_node(self, turn_number, available_moves):
        if self.turn_number % 2 == turn_number % 2:
            if self.game_state is not None:
                print(available_moves)
                print(self.game_state.available_moves)
                print("+++++++++++++++")
                print(" ")
                if self.game_state.available_moves == available_moves:
                    return self
        if self.turn_number + 3 > turn_number:
            return None
        for node in self.nodes:
            result = node.search_node(turn_number, available_moves)
            if result is not None:
                return self

    @staticmethod
    def update_stats(tree, player):
        tree.paths = 0
        tree.min_points = BOARD_SIZE * BOARD_SIZE
        tree.max_points = 0
        if len(tree.nodes) == 0:  # and tree.game_state is not None and tree.game_state.board is not None:
            stats = OthelloGame.get_stats(tree.game_state.board)
            tree.max_points = stats[tree.turn_number % 2]
            tree.min_points = stats[tree.turn_number % 2]
            if stats[tree.turn_number % 2] > stats[(tree.turn_number + 1) % 2]:
                if tree.turn_number % 2 == player:
                    tree.wins = 1
                else:
                    tree.loss = 1

            tree.paths = 1
        for node in tree.nodes:
            data = StateForecastTree.update_stats(node, player)
            # if data[4] == 0:
            #    tree.max_points = OthelloGame.get_stats(tree.game_state.board)[tree.turn_number % 2]
            #    tree.min_points = OthelloGame.get_stats(tree.game_state.board)[tree.turn_number % 2]
            tree.wins += data[0]
            tree.loss += data[1]
            tree.paths += data[2]
            tree.min_points = min(tree.min_points, data[3])
            tree.max_points = max(tree.max_points, data[4])
        return tree.wins, tree.loss, tree.paths, tree.min_points, tree.max_points
