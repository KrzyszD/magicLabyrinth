from config import *

class Player:
    idCounter = 0
    def __init__(self, gameEngine):
        self.id = Player.idCounter
        Player.idCounter += 1
        self.setCoord()
        self.show(gameEngine)
        self.points = 0
    
    def setCoord(self):
        global colSize, rowSize
        if self.id < 2:
            self.y = 0
        else:
            self.y = colSize - 1

        if self.id % 2 == 0:
            self.x = 0
        else:
            self.x = rowSize - 1
        
        # Starting point
        self.originY = self.y
        self.originX = self.x
    
    def show(self, gameEngine):
        # Show itself in the beginning of the game
        gameEngine.grid[self.x][self.y].changeColor(colors[self.id])

def getPlayerTurn():
    return playerTurn

def incPlayerTurn():
    global playerTurn, numPlayers
    playerTurn = (playerTurn + 1) % numPlayers
