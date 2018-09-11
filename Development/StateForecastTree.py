from Constants import BOARD_SIZE


class StateForecastTree:
    def __init__(self, turn_number, game_state, parent=None):
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

    def add_node(self, turn_number, game_state):
        self.nodes.append(StateForecastTree(turn_number, game_state, self))

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
            print("--")
            StateForecastTree.print_tree(node)

    @staticmethod
    def delete_nodes(node, stop_node_value):
        return node.delete(stop_node_value)
