"""
This file manges the main game.
"""

from othello import Othello
from util import UtilMethods

from Agents.playerRandom import PlayerRandom
from Agents.monteCarlo import PlayerMonteCarlo
from Agents.machineLearning import PlayerMachineLearning
from Agents.human import PlayerHuman
from Agents.alphaBetaPruning import PlayerAlphaBetaPruning

import time
from constants import PLAYER_ONE, PLAYER_TWO, PRINT_SYMBOLS, COLUMN_NAMES
from ml_database import ml_database

if __name__ == '__main__':
    # from machine_learning import Database
    # db = Database()
    # db._reset_database()
    print("Welcome to Othello")

    # Create a list of Player Types
    available_players = list()
    # Use pairs of the form (description: String, class: Player) to store a player type
    available_players.append(("Human Player", PlayerHuman))
    available_players.append(("AI Player - Random", PlayerRandom))
    available_players.append(("AI Player - Monte Carlo", PlayerMonteCarlo))
    available_players.append(("AI Player - Alpha-Beta Pruning", PlayerAlphaBetaPruning))
    available_players.append(("AI Player - Machine Learning", PlayerMachineLearning))

    # Ask the user to select a type of player as first player.
    selection_player_one = UtilMethods.select_one(available_players,
                                                  f"Select Mode for Player {PRINT_SYMBOLS[PLAYER_ONE]}")
    # Initialize a new player of the selected type and store it.
    player_one = selection_player_one()
    # Ask the user to select a type of player as second player.
    selection_player_two = UtilMethods.select_one(available_players,
                                                  f"Select Mode for Player {PRINT_SYMBOLS[PLAYER_TWO]}")
    # Initialize a new player of the selected type and store it.
    player_two = selection_player_two()

    # Store the players in a dict with the internal player codes as key to allow easy access and maintaining the correct order
    players = {PLAYER_ONE: player_one, PLAYER_TWO: player_two}

    # Create a new game state
    game = Othello()
    # Initialize it to start a new game
    game.init_game()

    # Print the board
    game.print_board()

    # store the start time
    start = time.time()
    # While the game is still running continue to make turns
    while not game.game_is_over():
        # Get the symbol for the current player
        current_player = game.get_current_player()
        # Get the Player object assigned to that player
        player_object = players[current_player]
        # Ask the Player to calculate it's move based on the current state
        move = player_object.get_move(game)
        # Play the move calculated by the player
        game.play_position(move)
        # Print the new state of the board
        game.print_board()

        print(f"Played position: ({COLUMN_NAMES[move[1]]}{move[0] + 1})")
    # calculate the playing time
    duration = time.time() - start

    ml_database._store_database()
    # Inform the User on the fact that the game is over
    print("Game is over")
    # Print the playing time
    print(f"Total duration: {duration} seconds")
    # Print the winner of the game
    print(f"Winner is {PRINT_SYMBOLS[game.get_winner()]}")
