from tkinter import *
from player import *
from engine import *

if __name__ == "__main__":
    root = createWindow()

    showMaze = True

    gameEngine = Engine(root, numPlayers, getPlayerTurn, incPlayerTurn, showMaze)

    players = [Player(gameEngine) for _ in range(numPlayers)]

    gameEngine.setPlayers(players)

    gameEngine.placeToken()

    root.mainloop()
