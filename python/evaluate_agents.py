import argparse
import os

"""
This file add console arguments to the main game.
"""

from othello import Othello
import heuristics

from Agents.random import Random
from Agents.monteCarlo import MonteCarlo
from Agents.human import Human
from Agents.alphaBetaPruning import AlphaBetaPruning
import time
from constants import PLAYER_ONE, PLAYER_TWO, PRINT_SYMBOLS, COLUMN_NAMES

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("games_nr", help="number of played games", type=int)

    parser.add_argument("agent1", help="number of first player", type=int, choices=[0, 1, 2, 3])
    parser.add_argument("agent2", help="number of second player", type=int, choices=[0, 1, 2, 3])

    parser.add_argument("--big_number1", help="number of random games", type=int)
    parser.add_argument("--big_number2", help="number of random games", type=int)

    parser.add_argument("--start_libs1", help="use start libs in agent 1", type=bool)
    parser.add_argument("--start_libs2", help="use start libs in agent 2", type=bool)

    parser.add_argument("--preprocessor_n1", help="number of preprocessor_n", type=int)
    parser.add_argument("--preprocessor_n2", help="number of preprocessor_n", type=int)

    parser.add_argument("--heuristic1", help="number of heuristic", type=int)
    parser.add_argument("--heuristic2", help="number of heuristic", type=int)

    parser.add_argument("--search_depth1", help="search depth of alpha beta", type=int)
    parser.add_argument("--search_depth2", help="search depth of alpha beta", type=int)

    parser.add_argument("--use_mp1", help="use multiprocessing", type=bool)
    parser.add_argument("--use_mp2", help="use multiprocessing", type=bool)

    parser.add_argument("--use_mc1", help="use monte carlo", type=bool)
    parser.add_argument("--use_mc2", help="use monte carlo", type=bool)

    parser.add_argument("--use_wmc1", help="use weighted monte carlo", type=bool)
    parser.add_argument("--use_wmc2", help="use weighted monte carlo", type=bool)

    args = parser.parse_args()

    big_number = 2000
    if args.big_number1:
        big_number = args.big_number1

    use_start_libs = True
    if args.start_libs1:
        use_start_libs = args.start_libs1

    preprocessor_n = -1
    if args.preprocessor_n1:
        preprocessor_n = args.preprocessor_n1

    heuristic1 = heuristics.StoredMonteCarloHeuristic.heuristic
    if args.heuristic1:
        print(f"heuristic1: {args.heuristic1}")
        # Create a list of all Heuristics
        available_heuristics = list()
        # Use pairs of the form (description: String, class: Player) to store a player type
        available_heuristics.append(("Nijssen 07 Heuristic", heuristics.Nijssen07Heuristic.heuristic))
        available_heuristics.append(("Field Heuristic", heuristics.StoredMonteCarloHeuristic.heuristic))
        available_heuristics.append(("Cowthello Heuristic", heuristics.CowthelloHeuristic.heuristic))
        heuristic1 = available_heuristics[args.heuristic1][1]

    use_multiprocessing = True
    if args.use_mp1:
        use_multiprocessing = args.use_mp1

    use_monte_carlo = False
    if args.use_mc1:
        print(f"mc1: {args.use_mc1}")
        use_monte_carlo = args.use_mc1

    use_weighted_monte_carlo = False
    if args.use_wmc1:
        print(f"mc1: {args.use_wmc1}")
        use_weighted_monte_carlo = args.use_wmc1

    search_depth = 5
    if args.search_depth1:
        search_depth = args.search_depth1

    if args.agent1 == 1:
        player_one = Random()
    elif args.agent1 == 2:
        player_one = MonteCarlo(big_number=big_number, use_start_libs=use_start_libs, preprocessor_n=preprocessor_n,
                                heuristic=heuristic1, use_multiprocessing=use_multiprocessing, use_weighted_random=use_weighted_monte_carlo)
    elif args.agent1 == 3:
        player_one = AlphaBetaPruning(heuristic=heuristic1, search_depth=search_depth, mc_count=big_number, use_monte_carlo=use_monte_carlo,
                                      use_start_lib=use_start_libs)
    else:
        player_one = Human()

    # --------------------------------------------------------------------------------------------------
    # Player 2

    big_number2 = 2000
    if args.big_number2:
        big_number2 = args.big_number2

    use_start_libs2 = True
    if args.start_libs2:
        use_start_libs2 = args.start_libs2

    preprocessor_n2 = -1
    if args.preprocessor_n2:
        preprocessor_n2 = args.preprocessor_n2

    heuristic2 = heuristics.StoredMonteCarloHeuristic.heuristic
    if args.heuristic2:
        print(f"heuristic2: {args.heuristic2}")
        # Create a list of all Heuristics
        available_heuristics2 = list()
        # Use pairs of the form (description: String, class: Player) to store a player type
        available_heuristics2.append(("Nijssen 07 Heuristic", heuristics.Nijssen07Heuristic.heuristic))
        available_heuristics2.append(("Field Heuristic", heuristics.StoredMonteCarloHeuristic.heuristic))
        available_heuristics2.append(("Cowthello Heuristic", heuristics.CowthelloHeuristic.heuristic))
        heuristic2 = available_heuristics2[args.heuristic2][1]

    use_multiprocessing2 = True
    if args.use_mp2:
        use_multiprocessing2 = args.use_mp2

    use_monte_carlo2 = False
    if args.use_mc2:
        print(f"mc2: {args.use_mc2}")
        use_monte_carlo2 = args.use_mc2

    use_weighted_monte_carlo2 = False
    if args.use_wmc2:
        print(f"mc1: {args.use_wmc2}")
        use_weighted_monte_carlo2 = args.use_wmc2

    search_depth2 = 5
    if args.search_depth2:
        search_depth2 = args.search_depth2

    if args.agent2 == 1:
        player_two = Random()
    elif args.agent2 == 2:
        player_two = MonteCarlo(big_number=big_number2, use_start_libs=use_start_libs2, preprocessor_n=preprocessor_n2,
                                heuristic=heuristic2, use_multiprocessing=use_multiprocessing2, use_weighted_random=use_weighted_monte_carlo2)
    elif args.agent2 == 3:
        player_two = AlphaBetaPruning(heuristic=heuristic2, search_depth=search_depth2,
                                      use_monte_carlo=use_monte_carlo2, mc_count=big_number2, use_start_lib=use_start_libs2)
    else:
        player_two = Human()

    games_nr = args.games_nr
    winning_stats = {PLAYER_ONE: 0, PLAYER_TWO: 0}
    durations = 0
    total_times = {PLAYER_ONE: 0, PLAYER_TWO: 0}

    outfile_info_string = f"p-{player_one}_h-{heuristic1}_bn-{big_number}_sl-{use_start_libs}_pp-{preprocessor_n}_mc-{use_monte_carlo}_mp-{use_multiprocessing}\nvs\np-{player_two}_h-{heuristic2}_bn-{big_number2}_sl-{use_start_libs2}_pp-{preprocessor_n2}_mc-{use_monte_carlo2}_mp-{use_multiprocessing2}"
    outfile_name = None
    i = 0
    while outfile_name is None:
        if not os.path.isfile(f"result-{i}.txt"):
            outfile_name = f"result-{i}.txt"
        print(i)
        i = i + 1

    with open(outfile_name, 'w') as outfile:
        outfile.write(outfile_info_string + "\n")

    for game_counter in range(games_nr):
        print(f"game: {game_counter}")
        # Store the players in a dict with the internal player codes as key to allow easy access and maintaining the correct order
        players = {PLAYER_ONE: player_one, PLAYER_TWO: player_two}
        times = {PLAYER_ONE: 0, PLAYER_TWO: 0}

        # Create a new game state
        game = Othello()
        # Initialize it to start a new game
        game.init_game()

        # store the start time
        start = time.time()
        # While the game is still running continue to make turns
        while not game.game_is_over():
            # Get the symbol for the current player
            current_player = game.get_current_player()
            # Get the Player object assigned to that player
            player_object = players[current_player]
            # Ask the Player to calculate it's move based on the current state
            calculation_start = time.time()
            move = player_object.get_move(game)
            calculation_time = time.time() - calculation_start
            times[current_player] += calculation_time
            # Play the move calculated by the player
            game.play_position(move)
            # Print the new state of the board
            # game.print_board()

            print(f"Played position: ({COLUMN_NAMES[move[1]]}{move[0] + 1})")
        # calculate the playing time
        duration = time.time() - start

        # Inform the User on the fact that the game is over
        print("Game is over")
        # Print the playing time
        print(f"Total duration: {duration} seconds")
        # Print the winner of the game
        winner = game.get_winner()
        if winner is not None:
            winning_stats[winner] += 1
        print(f"Winner is {PRINT_SYMBOLS[winner]}")
        durations += duration
        total_times[PLAYER_ONE] += times[PLAYER_ONE]
        total_times[PLAYER_TWO] += times[PLAYER_TWO]

        with open(outfile_name, 'a+') as outfile:
            outfile.write("------------------------------------------------------------------------------------------\n")
            outfile.write(f"Total games: {(game_counter + 1)}\n")
            outfile.write(f"Player 1 won {winning_stats[PLAYER_ONE]} games\n")
            outfile.write(f"Player 2 won {winning_stats[PLAYER_TWO]} games\n")
            outfile.write(f"Player 1 won in {winning_stats[PLAYER_ONE] * 100 / (game_counter + 1)} %\n")
            outfile.write(f"Player 2 won in {winning_stats[PLAYER_TWO] * 100 / (game_counter + 1)} %\n")
            outfile.write(f"Total Computation Time Player 1: {total_times[PLAYER_ONE]}\n")
            outfile.write(f"Total Computation Time Player 2: {total_times[PLAYER_TWO]}\n")
            outfile.write(f"Average Computation Time Player 1: {total_times[PLAYER_ONE] / (game_counter + 1)}\n")
            outfile.write(f"Average Computation Time Player 2: {total_times[PLAYER_TWO] / (game_counter + 1)}\n")
            outfile.write(f"Total Duration: {durations}\n")
            outfile.write(f"Average Duration: {durations / (game_counter + 1)}\n")
    print(f"Player 1 won {winning_stats[PLAYER_ONE]} games")
    print(f"Player 2 won {winning_stats[PLAYER_TWO]} games")
    print(f"Player 1 won in {winning_stats[PLAYER_ONE] * 100 / games_nr} %\n")
    print(f"Player 2 won in {winning_stats[PLAYER_TWO] * 100 / games_nr} %\n")
    print(f"total duration: {durations}")
    print(f"average duration: {durations / games_nr}")

    with open("results", 'w') as outfile:
        outfile.write(f"Total games: {games_nr}\n")
        outfile.write(f"Player 1 won {winning_stats[PLAYER_ONE]} games\n")
        outfile.write(f"Player 2 won {winning_stats[PLAYER_TWO]} games\n")
        outfile.write(f"Player 1 won in {winning_stats[PLAYER_ONE] * 100 / games_nr} %\n")
        outfile.write(f"Player 2 won in {winning_stats[PLAYER_TWO] * 100 / games_nr} %\n")
        outfile.write(f"Total Computation Time Player 1: {total_times[PLAYER_ONE]}\n")
        outfile.write(f"Total Computation Time Player 2: {total_times[PLAYER_TWO]}\n")
        outfile.write(f"Average Computation Time Player 1: {total_times[PLAYER_ONE] / games_nr}\n")
        outfile.write(f"Average Computation Time Player 2: {total_times[PLAYER_TWO] / games_nr}\n")
        outfile.write(f"Total Duration: {durations}\n")
        outfile.write(f"Average Duration: {durations / games_nr}\n")
