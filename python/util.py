"""
This file contains various utility methods.
E.g. to ask the user for a certain selection
"""


class UtilMethods:
    """
    Class contains static Utility Methods
    """

    @staticmethod
    def select_one(possibilities, description):
        """
        Asks the user to select one of the possibilities after displaying description as prompt
        """
        # Print the description as prompt
        print(description)
        # Display all possibilities
        # Iterate over the possibilities
        for i in range(len(possibilities)):
            # Access the description to each possibility
            (object_description, _) = possibilities[i]
            # Print it with the number it will be represented by
            print(f"{i}: {object_description}")
        # Store whether there is already a valid selection
        valid_selection = False
        # Store the selection value
        selection = -1  # invalid value
        # Continue to ask for a selection as long as there is no valid one
        while not valid_selection:
            try:
                # Prompt the user to enter a number representing her selection
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
        # Return the Object
        return object1

    @staticmethod
    def get_integer_selection(description, min_value, max_value):
        """
        Asks the user to select an integer between min_value and max_value
        """
        # Print the description as prompt
        print(description)
        # Initially there is no valid selection
        valid_selection = False
        # Init the selection
        selection = min_value - 1  # invalid selection
        # Continue to prompt user while there is no valid selection
        while not valid_selection:
            try:
                # Ask the user for an Integer input
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

    @staticmethod
    def translate_move_to_pair(move):
        column_numbers = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        result = (int(move[1]) - 1), column_numbers[move[0]]
        return result
