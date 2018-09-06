import sys

cellsToChange = 0


def get_max_changes(next_states):
    max_row = 4
    max_column = 4
    max_changes = 0
    for [[row, column], changes] in next_states:
        if changes > max_changes:
            max_changes = changes
            max_column = column
            max_row = row
    return [max_row, max_column]


def ai_next_states():
    global grid
    global cellsToChange
    next_states = []
    for row in range(0, rowNumber):
        for column in range(0, rowNumber):
            cellsToChange = 0
            if valid_turn(row, column, False):
                next_states.append([[row, column], cellsToChange])

    print(next_states)
    [best_row, best_column] = get_max_changes(next_states)
    valid_turn(best_row, best_column, True)
    grid[best_row][best_column] = actualPlayer + 1
    print(cellsToChange)


def print_grid():
    for c1 in range(0, rowNumber):
        sys.stdout.write(" | " + str(c1))
    sys.stdout.write("\n")
    for row in range(0, rowNumber):
        for c1 in range(0, rowNumber * 4 + 1):
            sys.stdout.write("-")
        sys.stdout.write("\n")
        sys.stdout.write(str(row))
        for column in range(0, rowNumber):
            field = "| " + " " + " "
            if grid[row][column] == 1:  # Player 1
                field = "| " + "W" + " "
            elif grid[row][column] == 2:  # Player 2
                field = "| " + "S" + " "
            sys.stdout.write(field)
        sys.stdout.write("|\n")


def grid_full():
    for row in range(0, rowNumber):
        for column in range(0, rowNumber):
            if grid[row][column] == 0:
                return False
    return True


def reverse_cell(row, column):
    sys.stdout.write("changed cell " + str(row) + " , " + str(column) + "\n")
    # if ( grid[ row ][ column ] == 1 ) :
    grid[row][column] = actualPlayer + 1


def other_player_grid():
    if actualPlayer == 0:
        return 2
    return 1


def valid_horizontal_1(row_nr, column_nr, change):
    global cellsToChange
    cell_found = False
    found_column = - 1
    for column in range(column_nr - 2, - 1, -1):
        if grid[row_nr][column] == actualPlayer + 1:
            cell_found = True
            found_column = column
            break
        elif grid[row_nr][column] == 0:
            cell_found = False
            break

    if cell_found:
        for r in range(column_nr - 1, found_column, - 1):
            cellsToChange += 1
        if change:
            for r in range(column_nr - 1, found_column, - 1):
                reverse_cell(row_nr, r)
        # sys.stdout.write( "valid horizontal \n" )
        return True
    return False


def valid_horizontal_2(row_nr, column_nr, change):
    global cellsToChange
    cell_found = False
    found_column = - 1
    for column in range(column_nr + 2, rowNumber):
        if grid[row_nr][column] == actualPlayer + 1:
            cell_found = True
            found_column = column
            break
        elif grid[row_nr][column] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(column_nr + 1, found_column, 1):
            cellsToChange += 1
        if change:
            # sys.stdout.write( "valid horizontal2 " + str(column) + " \n" )
            for r in range(column_nr + 1, found_column, 1):
                reverse_cell(row_nr, r)
        return True
    return False


# valid vertical
def valid_vertical_1(row_nr, column_nr, change):
    global cellsToChange
    cell_found = False
    found_row = - 1
    for row in range(row_nr - 2, - 1, - 1):
        if grid[row][column_nr] == actualPlayer + 1:
            cell_found = True
            found_row = row
            break
        elif grid[row][column_nr] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(row_nr - 1, found_row, - 1):
            cellsToChange += 1
        if change:
            sys.stdout.write("valid vertical \n")
            for r in range(row_nr - 1, found_row, - 1):
                reverse_cell(r, column_nr)
        return True
    return False


def valid_vertical_2(row_nr, column_nr, change):
    global cellsToChange
    cell_found = False
    row_found = - 1
    for row in range(row_nr + 1, rowNumber, + 1):
        if grid[row][column_nr] == actualPlayer + 1:
            cell_found = True
            row_found = row
            break
        elif grid[row][column_nr] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(row_nr + 1, row_found, 1):
            cellsToChange += 1
        if change:
            for r in range(row_nr + 1, row_found, 1):
                reverse_cell(r, column_nr)
        return True
    return False


def valid_diagonal_1(row_nr, column_nr, change):
    global cellsToChange
    for offset in range(2, rowNumber):
        if (row_nr - offset >= 0) and (column_nr - offset >= 0):
            if grid[row_nr - offset][column_nr - offset] == actualPlayer + 1:
                for offset2 in range(1, offset):
                    cellsToChange += 1
                if change:
                    for offset2 in range(1, offset):
                        reverse_cell(row_nr - offset2, column_nr - offset2)
                return True
            elif grid[row_nr - offset][column_nr - offset] == 0:
                break
    return False


def valid_diagonal_2(row_nr, column_nr, change):
    global cellsToChange
    for offset in range(2, rowNumber):
        if (row_nr - offset >= 0) and (column_nr + offset < rowNumber):
            if grid[row_nr - offset][column_nr + offset] == actualPlayer + 1:
                for offset2 in range(1, offset):
                    cellsToChange += 1
                if change:
                    for offset2 in range(1, offset):
                        reverse_cell(row_nr - offset2, column_nr + offset2)
                return True
            elif grid[row_nr - offset][column_nr + offset] == 0:
                break
    return False


def valid_diagonal_3(row_nr, column_nr, change):
    global cellsToChange
    for offset in range(2, rowNumber):
        if (row_nr + offset < rowNumber) and (column_nr + offset < rowNumber):
            if grid[row_nr + offset][column_nr + offset] == actualPlayer + 1:
                for offset2 in range(1, offset):
                    cellsToChange += 1
                if change:
                    for offset2 in range(1, offset):
                        reverse_cell(row_nr + offset2, column_nr + offset2)
                return True
            elif grid[row_nr + offset][column_nr + offset] == 0:
                break
    return False


def valid_diagonal_4(row_nr, column_nr, change):
    global cellsToChange
    for offset in range(2, rowNumber):
        if (row_nr + offset < rowNumber) and (column_nr - offset >= 0):
            if grid[row_nr + offset][column_nr - offset] == actualPlayer + 1:
                for offset2 in range(1, offset):
                    cellsToChange += 1
                if change:
                    for offset2 in range(1, offset):
                        reverse_cell(row_nr + offset2, column_nr - offset2)
                return True
            elif grid[row_nr + offset][column_nr - offset] == 0:
                break
    return False


def valid_turn(row_nr, column_nr, change):
    global grid
    valid = False

    if grid[row_nr][column_nr] != 0:
        return False

    if row_nr - 1 >= 0:
        if grid[row_nr - 1][column_nr] == other_player_grid():
            if valid_vertical_1(row_nr, column_nr, change):
                valid = True

    if row_nr + 1 < rowNumber:
        if grid[row_nr + 1][column_nr] == other_player_grid():
            if valid_vertical_2(row_nr, column_nr, change):
                valid = True

        if column_nr + 1 < rowNumber:
            if grid[row_nr + 1][column_nr + 1] == other_player_grid():
                if valid_diagonal_3(row_nr, column_nr, change):
                    valid = True

        if column_nr - 1 >= 0:
            if grid[row_nr + 1][column_nr - 1] == other_player_grid():
                if valid_diagonal_4(row_nr, column_nr, change):
                    valid = True

    if column_nr + 1 < rowNumber:
        if grid[row_nr][column_nr + 1] == other_player_grid():
            if valid_horizontal_2(row_nr, column_nr, change):
                valid = True

        if row_nr - 1 >= 0:
            if grid[row_nr - 1][column_nr + 1] == other_player_grid():
                if valid_diagonal_2(row_nr, column_nr, change):
                    valid = True

    if column_nr - 1 >= 0:
        if grid[row_nr][column_nr - 1] == other_player_grid():
            if valid_horizontal_1(row_nr, column_nr, change):
                valid = True

        if row_nr - 1 >= 0:
            if grid[row_nr - 1][column_nr - 1] == other_player_grid():
                if valid_diagonal_1(row_nr, column_nr, change):
                    valid = True
    return valid


def valid_cell_left():
    for row in range(0, rowNumber):
        for column in range(0, rowNumber):
            if valid_turn(row, column, False):
                return True
    sys.stdout.write("no valid turn left\n")
    return False


def insert_value():
    global actualPlayer
    global grid
    global rowNumber
    correct = False
    sys.stdout.write("Player " + str(actualPlayer + 1) + ":\n")
    row = rowNumber / 2
    column = rowNumber / 2
    while not correct:
        correct = True
        try:
            r1 = input("Insert row number: ")
            # if not r1:
            #    sys.stdout.write("row incorrect\n")
            #   correct = False
            #    continue
            row = int(r1)
            if row < 0 or row > rowNumber - 1:
                sys.stdout.write("row incorrect\n")
                correct = False
                continue

            c1 = input("Insert column number: ")
            # if not c1:
            #    sys.stdout.write("column incorrect\n")
            # correct = False
            # continue
            column = int(c1)
            if column < 0 or column > rowNumber - 1:
                sys.stdout.write("column incorrect\n")
                correct = False
                continue
            if grid[row][column] != 0:
                correct = False
                sys.stdout.write("cell is not empty\n")
                continue
            if not valid_turn(row, column, True):
                correct = False
                sys.stdout.write("no valid turn\n")
        except EOFError:
            print("incorrect input")

    if actualPlayer == 0:  # Player 1
        grid[row][column] = 1
    else:
        grid[row][column] = 2
    actualPlayer = (actualPlayer + 1) % 2


def game_finished():
    global grid
    player1 = 0
    player2 = 0
    for row in range(0, rowNumber):
        for column in range(0, rowNumber):
            if grid[row][column] == 1:
                player1 += 1
            elif grid[row][column] == 2:
                player2 += 1
    if player1 > player2:
        print("Player 1 wins: " + str(player1))
    else:
        print("Player 2 wins: " + str(player2))


rowNumber = 8
grid = [[0 for i1 in range(rowNumber)] for i2 in range(rowNumber)]
actualPlayer = 0  # Player 1 = 0


# Player 2 = 1


def main():
    global actualPlayer
    global grid
    global rowNumber

    print("Welcome to Othello game\n")

    start = int(rowNumber / 2)

    grid[start][start] = 1  # Player 1
    grid[start][start - 1] = 2  # Player 2
    grid[start - 1][start] = 2
    grid[start - 1][start - 1] = 1

    print_grid()
    while not grid_full() and valid_cell_left():
        if actualPlayer == 1:
            ai_next_states()
            actualPlayer = 0
        else:
            # ai_next_states()
            # actualPlayer = 1
            insert_value()
        print_grid()
    print("Finish")
    game_finished()


if __name__ == "__main__":
    main()
