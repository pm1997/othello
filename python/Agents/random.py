from othello import Othello
import random as rnd


class Random:
    """
    The PlayerRandom plays a random move taken from the set of legal moves
    The static method is kept in an enclosing class to support the generic use of Agents as done in main-game.py
    """

    @staticmethod
    def get_move(game_state: Othello):
        """
        interface function of all players
        :param game_state: actual game state
        :return: random move in available moves
        """
        # Get the legal moves
        possible_moves = game_state.get_available_moves()
        # Return a Random move
        return rnd.choice(possible_moves)
