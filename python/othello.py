class Othello:
    """Is the Othello Game class"""
    EMPTY_CELL = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    PRINT_SYMBOLS = {PLAYER_ONE: "B", PLAYER_TWO: "W"}

    DIRECTIONS = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}

    board_ = [[0 for _ in range(8)] for _ in range(8)]
    currentPlayer = None

    last_turn_passed = False

    fringe = set()
    turning_stones = dict()

    def init_game(self):
        self.board_[3][3] = self.PLAYER_TWO
        self.board_[4][4] = self.PLAYER_TWO
        self.board_[3][4] = self.PLAYER_ONE
        self.board_[4][3] = self.PLAYER_ONE

        self.update_fringe((3, 3))
        self.update_fringe((4, 4))
        self.update_fringe((3, 4))
        self.update_fringe((4, 3))

        self.currentPlayer = 0

    def print_board(self):
        for row in range(8):
            for col in range(8):
                print(self.board_[row][col], end="")
            print("\n", end="")

    def get_current_symbol(self):
        if self.currentPlayer == 0:
            return self.PLAYER_ONE
        if self.currentPlayer == 1:
            return self.PLAYER_TWO
        return None

    def next_player(self):
        if self.currentPlayer == 0:
            self.currentPlayer == 1
        elif self.currentPlayer == 1:
            self.currentPlayer == 0

    def update_fringe(self, position):
        (x, y) = position
        for direction in self.DIRECTIONS:
            next_step = self.next_step(position, direction)
            if self.board_[x][y] == self.EMPTY_CELL:
                self.fringe.add(next_step)

    def prepare_next_turn(self):
        self.next_player()
        self.compute_available_moves()

    @staticmethod
    def next_step(position, direction):
        (x, y), (x_step, y_step) = position, direction
        new_position = (new_x, new_y) = (x + x_step, y + y_step)
        if 0 <= new_x <= 8 and 0 <= new_y <= 8:
            return new_position
        else:
            return None

    def get_available_moves(self):
        return self.turning_stones.keys()

    def play_position(self, position):
        if position in self.get_available_moves():
            (x, y) = position
            current_symbol = self.get_current_symbol()
            self.board_[x][y] = current_symbol
            for (x, y) in self.turning_stones[position]:
                self.board_[x][y] = current_symbol
            self.update_fringe(position)
            self.prepare_next_turn()
            return True
        else:
            return False

    def compute_available_moves(self):
        self.turning_stones = dict()
        own_symbol = self.get_current_symbol()
        for current_position in self.fringe:
            for direction in self.DIRECTIONS:
                next_step = next_step(current_position, direction)
                this_direction = set()
                while next_step is not None:
                    (current_x, current_y) = next_step
                    current_value = self.board_[current_x][current_y]
                    if current_value == self.EMPTY_CELL:
                        break
                    elif current_value != own_symbol:
                        this_direction.add(next_step)
                    elif current_value == own_symbol:
                        if len(this_direction) > 0:
                            self.turning_stones[current_position] = this_direction
                        break
                    next_step = next_step(next_step, direction)