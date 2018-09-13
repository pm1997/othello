def print_grid(grid):
    import constants
    import sys
    for c1 in range(0, constants.GRID_SIZE):
        sys.stdout.write(" | " + str(c1))
    sys.stdout.write("\n")
    for row in range(0, constants.GRID_SIZE):
        for c1 in range(0, constants.GRID_SIZE * 4 + 1):
            sys.stdout.write("-")
        sys.stdout.write("\n")
        sys.stdout.write(str(row))
        for column in range(0, constants.GRID_SIZE):
            field = "| " + " " + " "
            if grid[row][column] == constants.PLAYER_ONE:  # Player 1
                field = "| " + "W" + " "
            elif grid[row][column] == constants.PLAYER_TWO:  # Player 2
                field = "| " + "S" + " "
            sys.stdout.write(field)
        sys.stdout.write("|\n")
