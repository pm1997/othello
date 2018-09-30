class OthelloGameState:

    def __init__(self, turn_number=-1, board=None, available_moves=None, stones_to_turn=None):
        self.turn_number = turn_number
        if board is None:
            board = list()
        self.board = board
        if available_moves is None:
            available_moves = set()
        self.available_moves = available_moves
        if stones_to_turn is None:
            stones_to_turn = dict()
        self.stones_to_turn = stones_to_turn

    def copy(self):
        return OthelloGameState(int(self.turn_number), self.board.copy(), self.available_moves.copy(),
                                self.stones_to_turn.copy())
