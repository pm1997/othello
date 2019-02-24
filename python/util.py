class UtilMethods:
    @staticmethod
    def select_one(possibilities, description):
        print(description)
        for i in range(len(possibilities)):
            (object_description, _) = possibilities[i]
            print(f"{i}: {object_description}")
        valid_selection = False
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
        (_, object) = possibilities[selection]
        return object

    @staticmethod
    def get_integer_selection(description, min_value, max_value):
        print(description)
        valid_selection = False
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
        return  selection