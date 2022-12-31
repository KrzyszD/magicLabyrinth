from tkinter import *
from player import *
from engine import *

if __name__ == "__main__":
    root = createWindow()
    gameEngine = Engine(root, numPlayers, getPlayerTurn, incPlayerTurn)

    players = [Player(gameEngine) for _ in range(numPlayers)]

    gameEngine.setPlayers(players)

    gameEngine.placeToken()

    root.mainloop()
