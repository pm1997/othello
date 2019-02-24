from othello import Othello
from util import UtilMethods
from players import PlayerRandom
from players import PlayerHuman
from players import PlayerMonteCarlo

print("Welcome to Othello")

while True:

    available_players = []
    available_players.append(("Human Player", PlayerHuman))
    available_players.append(("AI Player - Random", PlayerRandom))
    available_players.append(("AI Player - Monte Carlo (simple)", PlayerMonteCarlo))

    selection_player_one = UtilMethods.select_one(available_players, f"Select Mode for Player {Othello.PRINT_SYMBOLS[Othello.PLAYER_ONE]}")
    selection_player_two = UtilMethods.select_one(available_players,
                                                  f"Select Mode for Player {Othello.PRINT_SYMBOLS[Othello.PLAYER_TWO]}")

    players = {Othello.PLAYER_ONE: selection_player_one(), Othello.PLAYER_TWO: selection_player_two()}

    game = Othello()
    game.init_game()

    game.print_board()

    while not game.game_is_over():
        current_player = game.get_current_player()
        player_object = players[current_player]
        move = player_object.get_move(game)
        game.play_position(move)
        game.print_board()
    print("Game is over")
    print(f"Winner is {Othello.PRINT_SYMBOLS[game.get_winner()]}")
    exit(0)
