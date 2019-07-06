"""
This file contains various utility methods.
E.g. to ask the user for a certain selection
"""
from constants import COLUMN_NUMBERS


def select_one(possibilities, description):
    """
    Asks the user to select one of the possibilities after displaying description as prompt
    """
    print(description)
    # Display all possibilities
    for i in range(len(possibilities)):
        (object_description, _) = possibilities[i]
        print(f"{i}: {object_description}")
    valid_selection = False
    selection = -1  # invalid value
    # Continue to ask for a selection as long as there is no valid one
    while not valid_selection:
        try:
            selection = int(input("Please enter the number for your selection\n"))
        except ValueError:
            # Inform the user to enter an integer
            print("Invalid selection! Please enter an Integer")
            continue

        # The selection is valid if it is between 0 and the number of available possibilities
        if 0 <= selection < len(possibilities):
            valid_selection = True
        else:
            # Inform the user on the fact, that his selection was invalid
            print("Invalid selection! Please enter one of the listed options")
    # Get the selected Object
    (_, object1) = possibilities[selection]
    return object1


def get_integer_selection(description, min_value, max_value):
    """
    Asks the user to select an integer between min_value and max_value
    """
    print(description)
    # Initially there is no valid selection
    valid_selection = False
    selection = min_value - 1  # invalid selection
    # Continue to prompt user while there is no valid selection
    while not valid_selection:
        try:
            selection = int(input(f"Please enter a number between {min_value} and {max_value}\n"))
        except ValueError:
            # Inform the user on the fact, that the entered value was not an Integer
            print("Invalid selection! Please enter an Integer")
            continue
        # Check whether the given value is in the range
        if min_value <= selection <= max_value:
            valid_selection = True
        else:
            print("Invalid selection! Number not between the specified bounds")
    # Return the Selection
    return selection


def get_float_selection(description, min_value, max_value):
    """
    Asks the user to select an float between min_value and max_value
    """
    print(description)
    # Initially there is no valid selection
    valid_selection = False
    selection = min_value - 1  # invalid selection
    # Continue to prompt user while there is no valid selection
    while not valid_selection:
        try:
            selection = float(input(f"Please enter a number between {min_value} and {max_value}\n"))
        except ValueError:
            # Inform the user on the fact, that the entered value was not an Integer
            print("Invalid selection! Please enter a float value")
            continue
        # Check whether the given value is in the range
        if min_value <= selection <= max_value:
            valid_selection = True
        else:
            print("Invalid selection! Number not between the specified bounds")
    return selection


def get_boolean_selection(description):
    """
    Asks the user to enter a yes/no value
    """
    print(description)
    # Continue to prompt user while there is no valid selection
    while True:
        entered_string = input(f"Please enter y/n\n")
        if entered_string.lower() in {"yes", "y", "j", "ja", "1"}:
            return True
        elif entered_string.lower() in {"no", "n", "nein", "0"}:
            return False
        else:
            print("Invalid selection! Enter yes / no")


def translate_move_to_pair(move):
    """
    :param move: given move like "a2"
    :return: pair of row, column like 1, 0
    """
    result = (int(move[1]) - 1), COLUMN_NUMBERS[move[0]]
    return result
