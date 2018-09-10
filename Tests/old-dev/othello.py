import print_output
import gridClass
import constants
import validation
import ai


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
        if row < 0 or row >= constants.GRID_SIZE:
            print("row not a number")
            correct = False
            continue

        column = 0
        try:
            c1 = input("Insert column number: ")
            if len(c1) == 0:
                print("column incorrect")
                correct = False
                continue
            column = int(c1)
        except ValueError:
            print("column not a number")
            correct = False
            continue

        if column < 0 or column >= constants.GRID_SIZE:
            print("column incorrect")
            correct = False
            continue
        if grid.board[row][column] != 0:
            correct = False
            print("cell is not empty")
            continue
        if not validation.valid_turn(grid, row, column, True)[0]:
            correct = False
            print("no valid turn")

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
            insert_value(grid)
            # ai.solve(grid, constants.FORECAST_SEARCH)
        else:
            # insert_value(grid)
            ai.solve(grid, constants.FORECAST_SEARCH)
            # ai.solve(grid, constants.BEST_SEARCH)
        grid.actual_player = grid.other_player()
        print_output.print_grid(grid.board)
    print("Finish")
    grid.game_finished()


if __name__ == "__main__":
    main()
