import constants


def valid_horizontal_1(grid, row_nr, column_nr, change):
    cells_to_change = 0
    cell_found = False
    found_column = - 1
    for column in range(column_nr - 2, - 1, -1):
        if grid.board[row_nr][column] == grid.actual_player:
            cell_found = True
            found_column = column
            break
        elif grid.board[row_nr][column] == 0:
            cell_found = False
            break

    if cell_found:
        for r in range(column_nr - 1, found_column, - 1):
            cells_to_change += 1
        if change:
            for r in range(column_nr - 1, found_column, - 1):
                grid.reverse_cell(row_nr, r)
        # sys.stdout.write( "valid horizontal \n" )
        return True, cells_to_change
    return False, cells_to_change


def valid_horizontal_2(grid, row_nr, column_nr, change):
    cells_to_change = 0
    cell_found = False
    found_column = - 1
    for column in range(column_nr + 2, constants.GRID_SIZE):
        if grid.board[row_nr][column] == grid.actual_player:
            cell_found = True
            found_column = column
            break
        elif grid.board[row_nr][column] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(column_nr + 1, found_column, 1):
            cells_to_change += 1
        if change:
            for r in range(column_nr + 1, found_column, 1):
                grid.reverse_cell(row_nr, r)
        return True, cells_to_change
    return False, cells_to_change


def valid_vertical_1(grid, row_nr, column_nr, change):
    cells_to_change = 0
    cell_found = False
    found_row = - 1
    for row in range(row_nr - 2, - 1, - 1):
        if grid.board[row][column_nr] == grid.actual_player:
            cell_found = True
            found_row = row
            break
        elif grid.board[row][column_nr] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(row_nr - 1, found_row, - 1):
            cells_to_change += 1
        if change:
            for r in range(row_nr - 1, found_row, - 1):
                grid.reverse_cell(r, column_nr)
        return True, cells_to_change
    return False, cells_to_change


def valid_vertical_2(grid, row_nr, column_nr, change):
    cells_to_change = 0
    cell_found = False
    row_found = - 1
    for row in range(row_nr + 1, constants.GRID_SIZE, + 1):
        if grid.board[row][column_nr] == grid.actual_player:
            cell_found = True
            row_found = row
            break
        elif grid.board[row][column_nr] == 0:
            cell_found = False
            break
    if cell_found:
        for r in range(row_nr + 1, row_found, 1):
            cells_to_change += 1
        if change:
            for r in range(row_nr + 1, row_found, 1):
                grid.reverse_cell(r, column_nr)
        return True, cells_to_change
    return False, cells_to_change


def valid_diagonal_1(grid, row_nr, column_nr, change):
    cells_to_change = 0
    for offset in range(2, constants.GRID_SIZE):
        if (row_nr - offset >= 0) and (column_nr - offset >= 0):
            if grid.board[row_nr - offset][column_nr - offset] == grid.actual_player:
                for offset2 in range(1, offset):
                    cells_to_change += 1
                if change:
                    for offset2 in range(1, offset):
                        grid.reverse_cell(row_nr - offset2, column_nr - offset2)
                return True, cells_to_change
            elif grid.board[row_nr - offset][column_nr - offset] == 0:
                break
    return False, cells_to_change


def valid_diagonal_2(grid, row_nr, column_nr, change):
    cells_to_change = 0
    for offset in range(2, constants.GRID_SIZE):
        if (row_nr - offset >= 0) and (column_nr + offset < constants.GRID_SIZE):
            if grid.board[row_nr - offset][column_nr + offset] == grid.actual_player:
                for offset2 in range(1, offset):
                    cells_to_change += 1
                if change:
                    for offset2 in range(1, offset):
                        grid.reverse_cell(row_nr - offset2, column_nr + offset2)
                return True, cells_to_change
            elif grid.board[row_nr - offset][column_nr + offset] == 0:
                break
    return False, cells_to_change


def valid_diagonal_3(grid, row_nr, column_nr, change):
    cells_to_change = 0
    for offset in range(2, constants.GRID_SIZE):
        if (row_nr + offset < constants.GRID_SIZE) and (column_nr + offset < constants.GRID_SIZE):
            if grid.board[row_nr + offset][column_nr + offset] == grid.actual_player:
                for offset2 in range(1, offset):
                    cells_to_change += 1
                if change:
                    for offset2 in range(1, offset):
                        grid.reverse_cell(row_nr + offset2, column_nr + offset2)
                return True, cells_to_change
            elif grid.board[row_nr + offset][column_nr + offset] == 0:
                break
    return False, cells_to_change


def valid_diagonal_4(grid, row_nr, column_nr, change):
    cells_to_change = 0
    for offset in range(2, constants.GRID_SIZE):
        if (row_nr + offset < constants.GRID_SIZE) and (column_nr - offset >= 0):
            if grid.board[row_nr + offset][column_nr - offset] == grid.actual_player:
                for offset2 in range(1, offset):
                    cells_to_change += 1
                if change:
                    for offset2 in range(1, offset):
                        grid.reverse_cell(row_nr + offset2, column_nr - offset2)
                return True, cells_to_change
            elif grid.board[row_nr + offset][column_nr - offset] == 0:
                break
    return False, cells_to_change


def valid_turn(grid, row_nr, column_nr, change):
    valid = False
    cells_to_change = 0

    if grid.board[row_nr][column_nr] != 0:
        return False, 0

    if row_nr - 1 >= 0:
        if grid.board[row_nr - 1][column_nr] == grid.other_player():
            results = valid_vertical_1(grid, row_nr, column_nr, change)
            if results[0]:
                cells_to_change += results[1]
                valid = True

    if row_nr + 1 < constants.GRID_SIZE:
        if grid.board[row_nr + 1][column_nr] == grid.other_player():
            results = valid_vertical_2(grid, row_nr, column_nr, change)
            if results[0]:
                valid = True
                cells_to_change += results[1]

        if column_nr + 1 < constants.GRID_SIZE:
            if grid.board[row_nr + 1][column_nr + 1] == grid.other_player():
                results = valid_diagonal_3(grid, row_nr, column_nr, change)
                if results[0]:
                    valid = True
                    cells_to_change += results[1]

        if column_nr - 1 >= 0:
            if grid.board[row_nr + 1][column_nr - 1] == grid.other_player():
                results = valid_diagonal_4(grid, row_nr, column_nr, change)
                if results[0]:
                    valid = True
                    cells_to_change += results[1]

    if column_nr + 1 < constants.GRID_SIZE:
        if grid.board[row_nr][column_nr + 1] == grid.other_player():
            results = valid_horizontal_2(grid, row_nr, column_nr, change)
            if results[0]:
                valid = True
                cells_to_change += results[1]

        if row_nr - 1 >= 0:
            if grid.board[row_nr - 1][column_nr + 1] == grid.other_player():
                results = valid_diagonal_2(grid, row_nr, column_nr, change)
                if results[0]:
                    valid = True
                    cells_to_change += results[1]

    if column_nr - 1 >= 0:
        if grid.board[row_nr][column_nr - 1] == grid.other_player():
            results = valid_horizontal_1(grid, row_nr, column_nr, change)
            if results[0]:
                valid = True
                cells_to_change += results[1]

        if row_nr - 1 >= 0:
            if grid.board[row_nr - 1][column_nr - 1] == grid.other_player():
                results = valid_diagonal_1(grid, row_nr, column_nr, change)
                if results[0]:
                    valid = True
                    cells_to_change += results[1]
    return valid, cells_to_change


def get_valid_cells(grid):
    valid_cells = []
    for row in range(0, constants.GRID_SIZE):
        for column in range(0, constants.GRID_SIZE):
            results = valid_turn(grid, row, column, False)
            if results[0]:
                valid_cells.append([[row, column], results[1]])
    return valid_cells


def valid_cell_left(grid):
    for row in range(0, constants.GRID_SIZE):
        for column in range(0, constants.GRID_SIZE):
            if valid_turn(grid, row, column, False)[0]:
                return True
    print("no valid turn left")
    return False
