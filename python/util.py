class UtilMethods:
    @staticmethod
    def select_one(possibilities, description):
        print(description)
        for i in range(len(possibilities)):
            (object_description, _) = possibilities[i]
            print(f"{i}: {object_description}")
        valid_selection = False
        selection = -1  # invalid value
        while not valid_selection:
            try:
                selection = int(input("Please enter the number for your selection\n"))
            except ValueError:
                print("Invalid selection! Please enter an Integer")
                continue

            if 0 <= selection < len(possibilities):
                valid_selection = True
            else:
                print("Invalid selection! Please enter one of the listed options")
        (_, object1) = possibilities[selection]
        return object1

    @staticmethod
    def get_integer_selection(description, min_value, max_value):
        print(description)
        valid_selection = False
        selection = min_value - 1  # invalid selection
        while not valid_selection:
            try:
                selection = int(input(f"Please enter a number between {min_value} and {max_value}\n"))
            except ValueError:
                print("Invalid selection! Please enter an Integer")
                continue
            if min_value <= selection <= max_value:
                valid_selection = True
            else:
                print("Invalid selection! Number not between the specified bounds")
        return selection

    @staticmethod
    def translate_move_to_pair(move):
        column_numbers = {"a": 0, "b": 1, "c": 2,  "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        result = (int(move[1]) - 1), column_numbers[move[0]]
        return result
