import random
from time import sleep

from managers.game import Game
import entities.globals


def startGame():
    """
    Game Initialization
    """

    # Initializing Actual Game Interface
    newGame = Game(entities.globals.player1)

    # * Update this with proper exit condition
    while True:
        newGame.idle()


if __name__ == "__main__":
    startGame()
