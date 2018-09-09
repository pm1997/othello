class OthelloGameState:

    def __init__(self, turn_number=-1, board=list(), available_moves=set(), stones_to_turn=dict()):
        self.turn_number = turn_number
        self.board = board
        self.available_moves = available_moves
        self.stones_to_turn = stones_to_turn

    def copy(self):
        return OthelloGameState(int(self.turn_number), self.board.copy(), self.available_moves.copy(), self.stones_to_turn.copy())