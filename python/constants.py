# Define constants used to mark a field on the board as empty or taken by a certain player
EMPTY_CELL = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
# Define the string used in print statements to represent a certain player or an empty field.
PRINT_SYMBOLS = {EMPTY_CELL: " ", PLAYER_ONE: "B", PLAYER_TWO: "W", None: "None"}

# Used to print the names of fields not like (1,1) but as (b,1) instead.
COLUMN_NAMES = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

# Reverse of COLUMN_NAMES to match column name to a number
COLUMN_NUMBERS = {name: number for number, name in COLUMN_NAMES.items()}

# The move directions used to calculate the stones turned by a certain move and the legality of that move respectively
L = (-1, 0, 1)
DIRECTIONS = {(a, b) for a in L for b in L if (a, b) != (0, 0)}

# name of database file
DATABASE_FILE_NAME = "database_moves.csv"

# map field to position number
#     0   1   2   3   4   5   6   7
#   +---+---+---+---+---+---+---+---+
# 0 | 0 | 1 | 2 | 3 | 3 | 2 | 1 | 0 |
#   +---+---+---+---+---+---+---+---+
# 1 | 1 | 4 | 5 | 6 | 6 | 5 | 4 | 1 |
#   +---+---+---+---+---+---+---+---+
# 2 | 2 | 5 | 7 | 8 | 8 | 7 | 5 | 2 |
#   +---+---+---+---+---+---+---+---+
# 3 | 3 | 6 | 8 | X | X | 8 | 6 | 3 |
#   +---+---+---+---+---+---+---+---+
# 4 | 3 | 6 | 8 | X | X | 8 | 6 | 3 |
#   +---+---+---+---+---+---+---+---+
# 5 | 2 | 5 | 7 | 8 | 8 | 7 | 5 | 2 |
#   +---+---+---+---+---+---+---+---+
# 6 | 1 | 4 | 5 | 6 | 6 | 5 | 4 | 1 |
#   +---+---+---+---+---+---+---+---+
# 7 | 0 | 1 | 2 | 3 | 3 | 2 | 1 | 0 |
#   +---+---+---+---+---+---+---+---+
DATABASE_TO_POSITIONS = {0: [(0, 0), (0, 7), (7, 0), (7, 7)],
                          1: [(0, 1), (0, 6), (1, 0), (1, 7), (6, 0), (6, 7), (7, 1), (7, 6)],
                          2: [(0, 2), (0, 5), (2, 0), (2, 7), (5, 0), (5, 7), (7, 2), (7, 5)],
                          3: [(0, 3), (0, 4), (3, 0), (3, 7), (4, 0), (4, 7), (7, 3), (7, 4)],
                          4: [(1, 1), (1, 6), (6, 1), (6, 6)],
                          5: [(1, 2), (1, 5), (2, 1), (2, 6), (5, 1), (5, 6), (6, 2), (6, 5)],
                          6: [(1, 3), (1, 4), (3, 1), (3, 6), (4, 1), (4, 6), (6, 3), (6, 4)],
                          7: [(2, 2), (2, 5), (5, 2), (5, 5)],
                          8: [(2, 3), (2, 4), (3, 2), (3, 5), (4, 2), (4, 5), (5, 3), (5, 4)],
                          'X': [(3, 3), (3, 4), (4, 3), (4, 4)]}

POSITION_TO_DATABASE = {}
for (field_type, fields) in DATABASE_TO_POSITIONS.items():
    for field in fields:
        POSITION_TO_DATABASE[field] = field_type
