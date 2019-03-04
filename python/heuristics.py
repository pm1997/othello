from othello import Othello

ALL_FIELDS = {(a, b) for a in range(8) for b in range(8)}
CENTRAL_FIELDS = {(a, b) for a in range(2, 6) for b in range(2, 6)}
CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
C_FIELDS = {(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)}
X_FIELDS = {(1, 1), (1, 6), (6, 1), (6, 6)}
A_FIELDS = {(0, 2), (0, 5), (2, 0), (2, 7), (5, 0), (5, 7), (7, 2), (7, 5)}
B_FIELDS = {(0, 3), (0, 4), (3, 0), (3, 7), (4, 0), (4, 7), (7, 3), (7, 4)}
EDGES = C_FIELDS | A_FIELDS | B_FIELDS
OTHER_FIELDS = ALL_FIELDS - CENTRAL_FIELDS - CORNERS - EDGES - X_FIELDS


def get_sign(current_player, field_value):
    if field_value == current_player:
        return 1
    elif field_value == Othello.other_player(current_player):
        return -1
    else:
        return 0


class Nijssen07Heuristic:
    values = dict()
    for position in CORNERS:
        values[position] = 5
    for position in X_FIELDS:
         values[position] = -2
    for position in C_FIELDS:
        values[position] = -1
    for position in CENTRAL_FIELDS:
        values[position] = 2
    for position in ALL_FIELDS - CORNERS - X_FIELDS - C_FIELDS - CENTRAL_FIELDS:
        values[position] = 1

    @staticmethod
    def heuristic(current_player, game_state: Othello):
        value = 0
        board = game_state.get_board()
        weight_dict = Nijssen07Heuristic.values
        for (x, y) in Nijssen07Heuristic.values.keys():
            value += get_sign(current_player, board[x][y]) * weight_dict[(x, y)]
        return value
