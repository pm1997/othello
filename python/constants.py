# Define constants used to mark a field on the board as empty or taken by a certain player
EMPTY_CELL = 0
PLAYER_ONE = 1
PLAYER_TWO = 2
# Define the string used in print statements to represent a certain player or an empty field.
PRINT_SYMBOLS = {EMPTY_CELL: " ", PLAYER_ONE: "B", PLAYER_TWO: "W", None: "None"}

# Used to print the names of fields not like (1,1) but as (b,1) instead.
COLUMN_NAMES = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

# The move directions used to calculate the stones turned by a certain move
# and the legality of that move respectively
DIRECTIONS = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

# Reverse of COLUMN_NAMES to match column name to a number
COLUMN_NUMBERS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
