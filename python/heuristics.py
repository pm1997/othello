"""
This file contains heuristics used to evaluate a certain game state
"""

from othello import Othello
import  util
from constants import POSITION_TO_DATABASE
import database

# Generate sets of fields with similar value
ALL_FIELDS = {(a, b) for a in range(8) for b in range(8)}
CENTER = {(3, 3), (3, 4), (4, 3), (4, 4)}
CENTRAL_FIELDS = {(a, b) for a in range(2, 6) for b in range(2, 6)}
CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
C_FIELDS = {(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)}
X_FIELDS = {(1, 1), (1, 6), (6, 1), (6, 6)}
A_FIELDS = {(0, 2), (0, 5), (2, 0), (2, 7), (5, 0), (5, 7), (7, 2), (7, 5)}
B_FIELDS = {(0, 3), (0, 4), (3, 0), (3, 7), (4, 0), (4, 7), (7, 3), (7, 4)}
EDGES = C_FIELDS | A_FIELDS | B_FIELDS
OTHER_FIELDS = ALL_FIELDS - CENTRAL_FIELDS - CORNERS - EDGES - X_FIELDS


def get_sign(current_player, field_value):
    """
    Returns an indicator whether the field_value denotes a field as owned by current_player
      1: if the field_value indicates the field is owned by the current_player
      0: if the field_value indicates neither player owns the field
     -1: If the field_value indicates the field is owned by opponent of current_player
    Both current_player and field_value are coded as the constants EMPTY_CELL, PLAYER_ONE and PLAYER_TWO
      form constants.py. Therefore both parameters are integer values.
    """
    if field_value == current_player:
        return 1
    elif field_value == Othello.other_player(current_player):
        return -1
    else:
        return 0


def select_heuristic(player_string):
    """
    Asks the user to select one of the heuristics known to the function
    :param player_string: 'W' or 'B' to ask specific player to choose a heuristic
    :return: function reference of the selected heuristic
    """
    # Create a list of all Heuristics
    available_heuristics = list()
    # Use pairs of the form (description: String, class: Player) to store a player type
    available_heuristics.append(("Nijssen 07 Heuristic", NijssenHeuristic.heuristic))
    available_heuristics.append(("Field Heuristic", StoredMonteCarloHeuristic.heuristic))
    available_heuristics.append(("Cowthello Heuristic", CowthelloHeuristic.heuristic))

    if len(available_heuristics) > 1:
        return util.select_one(available_heuristics, f"[{player_string}] Please select a heuristic")
    else:
        return available_heuristics[0][1]


class NijssenHeuristic:
    """
    Is the heuristic proposed by Nijssen's paper from 2007
    """
    # Create a dictionary and assign each field it's value
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
        """
        Calculates the value of game_state for current_player according to the Nijssen Heuristic
        current_player is coded as the constants EMPTY_CELL, PLAYER_ONE and PLAYER_TWO
          form constants.py. Therefore the parameter is an integer values.
        """
        # Without any information the value is 0
        value = 0
        # Get the board
        board = game_state.get_board()
        # Get the values assigned to each field
        weight_dict = NijssenHeuristic.values
        # Iterate over the fields with an assigned value
        for (row, column) in NijssenHeuristic.values.keys():
            # Add the fields value to the heuristic value if it us owned by the current player. Subtract it otherwise
            value += get_sign(current_player, board[row][column]) * weight_dict[(row, column)]
        # Return the Calculated value 
        return value


class StoredMonteCarloHeuristic:

    @staticmethod
    def heuristic(current_player, game_state: Othello):
        """
        Calculates the value of game_state for current_player according to the Stored MonteCarlo Heuristic
        current_player is coded as the constants EMPTY_CELL, PLAYER_ONE and PLAYER_TWO
          form constants.py. Therefore the parameter is an integer values.
        """

        moves = game_state.get_available_moves()
        turn_nr = game_state.get_turn_nr()

        return max([database.db.get_likelihood(move, turn_nr, current_player) for move in moves])


class CowthelloHeuristic:
    """
    Is the heuristic proposed by http://www.aurochs.org/games/cowthello/cowthello.js

    corner,     nextCorner, helpCorner, edge,       edge,       helpCorner, nextCorner, corner,
    nextCorner, nextNext,   normal,     normal,     normal,     normal,     nextNext,   nextCorner,
    helpCorner, normal,     helpHelp,   helpEdge,   helpEdge,   helpHelp,   normal,     helpCorner,
    edge,       normal,     helpEdge,   normal,     normal,     helpEdge,   normal,     edge,
    edge,       normal,     helpEdge,   normal,     normal,     helpEdge,   normal,     edge,
    helpCorner, normal,     helpHelp,   helpEdge,   helpEdge,   helpHelp,   normal,     helpCorner,
    nextCorner, nextNext,   normal,     normal,     normal,     normal,     nextNext,   nextCorner,
    corner,     nextCorner, helpCorner, edge,       edge,       helpCorner, nextCorner, corner

    corner=100;
    edge=10;
    helpCorner=25;
    helpHelp=50
    nextCorner=-25;
    normal=1;
    helpEdge=5;
    nextNext=-50;


    """
    # Create a dictionary and assign each field it's value
    values = dict()
    for position in ALL_FIELDS:
        values[position] = POSITION_TO_DATABASE[position]

    weight_matcher = {0: 100, 1: -25, 2: 25, 3: 10, 4: -50, 5: 1, 6: 1, 7: 50, 8: 5, 'X': 1}
    for position in ALL_FIELDS:
        values[position] = weight_matcher[values[position]]

    @staticmethod
    def heuristic(current_player, game_state: Othello):
        """
        Calculates the value of game_state for current_player according to the Cowthello
        current_player is coded as the constants EMPTY_CELL, PLAYER_ONE and PLAYER_TWO
          form constants.py. Therefore the parameter is an integer values.
        """
        # Without any information the value is 0
        value = 0
        # Get the board
        board = game_state.get_board()
        # Get the values assigned to each field
        weight_dict = CowthelloHeuristic.values
        # Iterate over the fields with an assigned value
        for (x, y) in CowthelloHeuristic.values.keys():
            # Add the fields value to the heuristic value if it us owned by the current player. Subtract it otherwise
            value += get_sign(current_player, board[x][y]) * weight_dict[(x, y)]
        # Return the Calculated value
        return value
