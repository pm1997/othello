import constants
import validation
from time import time


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


def ai_next_states(grid):
    next_states = []
    t = time()
    for row in range(0, constants.GRID_SIZE):
        for column in range(0, constants.GRID_SIZE):
            results = validation.valid_turn(grid, row, column, False)
            if results[0]:
                next_states.append([[row, column], results[1]])
    diff_time = (time() - t) * 1000
    print("duration in milli seconds: " + str(diff_time))
    print(next_states)
    [best_row, best_column] = get_max_changes(next_states)
    if best_row == constants.GRID_SIZE + 1 or best_column == constants.GRID_SIZE + 1:
        print("Error")
        return
    validation.valid_turn(grid, best_row, best_column, True)
    grid.board[best_row][best_column] = grid.actual_player
