from othello import Othello
import random


class PlayerRandom:
    """
    The PlayerRandom plays a random move taken from the set of legal moves
    """

    @staticmethod
    def get_move(game_state: Othello):
        """
        Return the selected move for the current state
        """
        # Get the legal moves
        possible_moves = game_state.get_available_moves()
        # Return a Random move
        return possible_moves[random.randrange(len(possible_moves))]
