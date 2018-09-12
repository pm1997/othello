from Constants import BOARD_SIZE


class StateForecastTree:
    def __init__(self, turn_number, game_state=None, parent=None):
        self.turn_number = turn_number
        self.x = int(BOARD_SIZE / 2)
        self.y = int(BOARD_SIZE / 2)
        self.paths = 0
        self.wins = 0
        self.loss = 0
        self.max_points = 0
        self.min_points = BOARD_SIZE * BOARD_SIZE
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

    def add_node(self, turn_number, x, y, parent=None, game_state=None):
        self.nodes.append(StateForecastTree(turn_number, game_state, self))
        self.nodes[len(self.nodes) - 1].x = x
        self.nodes[len(self.nodes) - 1].y = y
        self.parent = parent

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
            print(node.turn_number)
            print("x:" + str(node.x) + " y:" + str(node.y))
            print("--")
            StateForecastTree.print_tree(node)

    @staticmethod
    def delete_nodes(node, stop_node_value):
        return node.delete(stop_node_value)

    def search_node(self, turn_number):
        if self.turn_number == turn_number:
            return self
        if self.turn_number > turn_number:
            if self.parent is not None:
                return self.parent.search_node(turn_number)
        else:
            node_count = len(self.nodes)
            i = 0
            if node_count > 0:
                result = self.nodes[i].search_node(turn_number)
                while result is None and i + 1 < node_count:
                    i += 1
                    result = self.nodes[i].search_node(turn_number)
                return result
            return None

    @staticmethod
    def update_stats(tree):
        tree.wins = 0
        tree.loss = 0
        tree.paths = 0
        for node in tree.nodes:
            tree.wins += node.wins
            tree.loss += node.loss
            tree.paths += node.paths
        if tree.parent is not None:
            StateForecastTree.update_stats(tree.parent)
