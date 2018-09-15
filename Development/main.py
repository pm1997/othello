from othelloGame import OthelloGame
from constants import BOARD_SIZE


def main():
    print("new game++++++++++++++++++++++++")
    OthelloGame(BOARD_SIZE, False)
    input("Press any key to exit")


if __name__ == "__main__":
    main()
