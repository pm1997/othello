class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class PlayerInvalidError(Error):
    def __init__(self, message):
        self.message = message


class InvalidTurnError(Error):
    def __init__(self, message):
        self.message = message


class OddBoardSizeError(Error):
    def __init__(self, message):
        self.message = message


class BoardToSmallError(Error):
    def __init__(self, message):
        self.message = message


class NonIntegerBoardSizeError(Error):
    def __init__(self, message):
        self.message = message


class ToManyPlayersError(Error):
    def __init__(self, message):
        self.message = message