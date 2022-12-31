from tkinter import *
from player import *
from engine import *

if __name__ == "__main__":
    root = createWindow()

    showMaze = True
    showWall = True
    showWallPerma = True

    gameEngine = Engine(root, numPlayers, getPlayerTurn, incPlayerTurn, showMaze, showWall, showWallPerma)

    players = [Player(gameEngine) for _ in range(numPlayers)]

    gameEngine.setPlayers(players)

    gameEngine.placeToken()

    root.mainloop()
