from othello import Othello
from util import UtilMethods
from players import PlayerMonteCarlo, PlayerMonteCarlo2, PlayerMonteCarlo3, PlayerHuman, PlayerRandom, PlayerAlphaBetaPruning
import time

print("Welcome to Othello")

while True:

    available_players = list()
    available_players.append(("Human Player", PlayerHuman))
    available_players.append(("AI Player - Random", PlayerRandom))
    available_players.append(("AI Player - Monte Carlo (simple)", PlayerMonteCarlo))
    available_players.append(("AI Player - Monte Carlo (improved)", PlayerMonteCarlo2))
    available_players.append(("AI Player - Monte Carlo (machine learning)", PlayerMonteCarlo3))
    available_players.append(("AI Player - Alpha-Beta Pruning", PlayerAlphaBetaPruning))

    selection_player_one = UtilMethods.select_one(available_players, f"Select Mode for Player {Othello.PRINT_SYMBOLS[Othello.PLAYER_ONE]}")
    player_one = selection_player_one()
    selection_player_two = UtilMethods.select_one(available_players,
                                                  f"Select Mode for Player {Othello.PRINT_SYMBOLS[Othello.PLAYER_TWO]}")
    player_two = selection_player_two()

    players = {Othello.PLAYER_ONE: player_one, Othello.PLAYER_TWO: player_two}

    game = Othello()
    game.init_game()

    game.print_board()

    start = time.time()
    while not game.game_is_over():
        current_player = game.get_current_player()
        player_object = players[current_player]
        move = player_object.get_move(game)
        game.play_position(move)
        game.print_board()
    duration = time.time() - start
    print("Game is over")
    print(f"Total duration: {duration} seconds")
    print(f"Winner is {Othello.PRINT_SYMBOLS[game.get_winner()]}")
    exit(0)
