from othello import Othello
from constants import COLUMN_NAMES
import util


class Human:
    """
    The Human Agent asks the user to select each move
    """

    @staticmethod
    def get_move(game_state: Othello):
        """
        interface function of all players
        Asks the user for a move and returns the selection
        :param game_state: actual game state
        :return: best move in available moves
        """
        # Create a data structure to use with util.select_one
        possibilities = []
        for move in game_state.get_available_moves():
            (row, col) = move
            description = f"({COLUMN_NAMES[col]}{row + 1})"
            possibilities.append((description, move))
        # Return the users selection
        return util.select_one(possibilities, "Select your move:")
