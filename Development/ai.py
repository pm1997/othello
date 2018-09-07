import gridClass
import constants
import validation


def get_max_changes(next_states):
    max_row = constants.GRID_SIZE / 2
    max_column = constants.GRID_SIZE / 2
    max_changes = 0
    for [[row, column], changes] in next_states:
        if changes > max_changes:
            max_changes = changes
            max_column = column
            max_row = row
    return [max_row, max_column]


def ai_next_states(grid):
    cells_to_change = 0
    next_states = []
    for row in range(0, constants.GRID_SIZE):
        for column in range(0, constants.GRID_SIZE):
            cells_to_change = 0
            results = validation.valid_turn(grid, row, column, False)
            print(results)
            if results[0]:
                next_states.append([[row, column], results[1]])

    print(next_states)
    [best_row, best_column] = get_max_changes(next_states)
    validation.valid_turn(grid, best_row, best_column, True)
    grid.board[best_row][best_column] = grid.actual_player
    print(cells_to_change)
