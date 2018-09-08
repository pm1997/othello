from abc import ABC, abstractmethod
class Player(ABC):
    @abstractmethod
    def __init__(self, game_reference):
        pass

    @abstractmethod
    def play(self):
        pass