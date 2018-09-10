import constants
import validation
from time import time
import gridClass


def get_max_changes(next_states):
    max_row = constants.GRID_SIZE + 1
    max_column = constants.GRID_SIZE + 1
    max_changes = 0
    for [[row, column], changes] in next_states:
        if changes > max_changes:
            max_changes = changes
            max_column = column
            max_row = row
    return [max_row, max_column]


def solve(grid, method=0):
    if method == constants.BEST_SEARCH:  # greedy best search
        ai_best_search(grid)
    elif method == constants.FORECAST_SEARCH:  # forecasting search
        ai_forecast(grid, constants.MAX_FORECAST)
    else:
        ai_best_search(grid)


def ai_best_search(grid):
    t = time()
    next_states = validation.get_valid_cells(grid)
    diff_time = (time() * 1000 - t * 1000)
    print("duration in milli seconds: " + str(diff_time))
    print(next_states)
    [best_row, best_column] = get_max_changes(next_states)
    if best_row == constants.GRID_SIZE + 1 or best_column == constants.GRID_SIZE + 1:
        print("Error")
        return
    validation.valid_turn(grid, best_row, best_column, True)
    grid.board[best_row][best_column] = grid.actual_player


def ai_forecast(grid, limit):
    if limit == 0:
        return False
    best = 0
    worse = constants.GRID_SIZE * constants.GRID_SIZE
    grid2 = gridClass.Grid()
    grid2.board = grid.board
    grid2.actual_player = grid.actual_player
    print(deepening_states(grid2, [[]], [0, 0, 0], best, worse, constants.MAX_FORECAST, []))


def deepening_states(grid, path, exit_codes, best_case, worse_case, limit, states):
    if limit == 0:  # limit
        exit_codes[0] += 1
        return path, exit_codes, best_case, worse_case
    limit -= 1
    next_states = validation.get_valid_cells(grid)
    if len(next_states) == 0:  # game finished
        [w, p1, p2] = grid.get_winner()
        if constants.PLAYER_ONE == w:
            exit_codes[1] += 1
        else:
            exit_codes[2] += 1

        if grid.actual_player == w:
            best_case = max(p1, best_case)
        else:
            worse_case = min(worse_case, p2)
        return path, exit_codes, best_case, worse_case
    for [[row, column], _] in next_states:
        print("!")
        print(str(row) + " --- " + str(column))
        grid.board[row][column] = grid.actual_player
        grid.actual_player = grid.other_player()  # change player
        path.append([row, column])
        best_case = max(best_case, grid.cells_of_player(grid.actual_player))
        worse_case = min(worse_case, grid.cells_of_player(grid.actual_player))
        states.append(deepening_states(grid, path, exit_codes, best_case, worse_case, limit, states))
    return states
