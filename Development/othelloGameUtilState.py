from constants import EMPTY_CELL


class OthelloGameState:

    def __init__(self, turn_number=-1, number_of_passes=0, board=None, available_moves=None, stones_to_turn=None):
        self.turn_number = turn_number
        self.number_of_passes = number_of_passes
        if board is None:
            board = list()
        self.board = board
        if available_moves is None:
            available_moves = set()
        self.available_moves = available_moves
        if stones_to_turn is None:
            stones_to_turn = dict()
        self.stones_to_turn = stones_to_turn

    def copy_state(self):
        return OthelloGameState(int(self.turn_number), int(self.number_of_passes),
                                OthelloGameState.copy_board(self.board),
                                self.available_moves.copy(),
                                self.stones_to_turn.copy())

    @staticmethod
    def copy_board(old_board):
        board_size = len(old_board)
        new_board = [[EMPTY_CELL for _ in range(board_size)] for _ in range(board_size)]
        for row in range(board_size):
            for column in range(board_size):
                new_board[row][column] = old_board[row][column]
        return new_board
