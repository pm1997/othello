import print_output
import gridClass
import constants
import sys
import validation
import ai


def game_finished(board):
    player1 = 0
    player2 = 0
    for row in range(0, constants.GRID_SIZE):
        for column in range(0, constants.GRID_SIZE):
            if board[row][column] == 1:
                player1 += 1
            elif board[row][column] == 2:
                player2 += 1
    if player1 > player2:
        print("Player 1 wins: " + str(player1))
    else:
        print("Player 2 wins: " + str(player2))


def insert_value(grid):
    correct = False
    print("Player " + str(grid.actual_player) + ":")
    row = constants.GRID_SIZE / 2
    column = constants.GRID_SIZE / 2
    while not correct:
        correct = True
        row = 0
        try:
            r1 = input("Insert row number: ")
            if len(r1) == 0:
                print("row incorrect")
                correct = False
                continue
            row = int(r1)
        except ValueError:
            print("row incorrect")
            correct = False
            continue
        if row < 0 or row > constants.GRID_SIZE - 1:
            print("row not a number")
            correct = False
            continue

        column = 0
        try:
            c1 = input("Insert column number: ")
            if len(c1) == 0:
                sys.stdout.write("column incorrect\n")
                correct = False
                continue
            column = int(c1)
        except ValueError:
            print("column not a number")
            correct = False
            continue

        if column < 0 or column > constants.GRID_SIZE - 1:
            sys.stdout.write("column incorrect\n")
            correct = False
            continue
        if grid.board[row][column] != 0:
            correct = False
            sys.stdout.write("cell is not empty\n")
            continue
        if not validation.valid_turn(grid, row, column, True):
            correct = False
            sys.stdout.write("no valid turn\n")

    if grid.actual_player == constants.PLAYER_ONE:
        grid.board[row][column] = constants.PLAYER_ONE
    else:
        grid.board[row][column] = constants.PLAYER_TWO


def main():
    print("Welcome to Othello game\n")

    grid = gridClass.Grid()
    grid.actual_player = constants.PLAYER_ONE

    start = int(constants.GRID_SIZE / 2)

    grid.board[start][start] = constants.PLAYER_ONE
    grid.board[start][start - 1] = constants.PLAYER_TWO
    grid.board[start - 1][start] = constants.PLAYER_TWO
    grid.board[start - 1][start - 1] = constants.PLAYER_ONE

    print_output.print_grid(grid.board)
    while not grid.grid_full() and validation.valid_cell_left(grid):
        if grid.actual_player == constants.PLAYER_ONE:
            # insert_value(grid)
            ai.ai_next_states(grid)
        else:
            ai.ai_next_states(grid)
        grid.actual_player = grid.other_player()
        print_output.print_grid(grid.board)
    print("Finish")
    game_finished(grid.board)


if __name__ == "__main__":
    main()
