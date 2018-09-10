from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, game_reference):
        self._game_reference = game_reference

    @abstractmethod
    def play(self):
        pass
