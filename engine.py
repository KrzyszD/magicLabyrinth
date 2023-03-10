from tkinter import *
from config import *
from random import randint, shuffle
import os
import math
import itertools
from canvas_btn import CanvasButton

def createWindow():
    root = Tk()

    root.title("Magic Labyrinth")

    root.geometry(f"{int(rowSize*gridCellSize * 1.0)}x{colSize*gridCellSize+135}")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    return root

class Engine:
    def __init__(self, root, numPlayers, getPlayerTurn, incPlayerTurn, showPath=False, showWall=False, showWallPerma=False):
        self.root = root
        self.numPlayers = numPlayers
        self.getPlayerTurn = getPlayerTurn
        self.incPlayerTurn = incPlayerTurn
        self.numMoves = 0

        self.showPath = showPath
        self.showWall = showWall
        self.showWallPerma = showWallPerma
        
        # grid btns
        self.grid = [[] for _ in range(rowSize)]
        self.possWalls = []

        # Colors
        self.colors = colors
        self.clearColor = "SystemButtonFace"

        # Grid and controls
        self.gridFrame = Canvas(root)
        self.controlFrame = Frame(root)

        self.setGridBtns()
        self.setControlBtns()

        # Bottom label
        self.label = Label(root, text=f"It is {colors[0]}'s turn")
        self.label.grid(row=2, column=0, sticky="n")

        # Make maze
        self.makeMaze()

        # Shows path
        if self.showPath:
            self.showPaths()

        # print("Available Tokens: ", len(self.avaibleTokens))
    
    
    def setGridBtns(self):
        # Sets up the grid
        gridFrame = self.gridFrame

        # Empty image to enable size by pixel
        self.pixel = PhotoImage(width=60, height=60)
        self.avaibleTokens = []

        # Gets coin image
        cwd = os.getcwd()
        self.coin = PhotoImage(file=cwd + '\\' + coinPNG)
        
        # Places grid in window
        gridFrame.grid(row=0, column=0, sticky="news")
        
        # Actual grid
        grid = Frame(gridFrame)
        grid.grid(sticky="n", column=0, row=rowSize, columnspan=2)

        # Initializes each btn
        for x in range(rowSize):
            for y in range(colSize):
                self.configureGridBtn(x, y)
                
        # Sets grid dimensions
        gridFrame.columnconfigure(tuple(range(rowSize)), weight=1)
        gridFrame.rowconfigure(tuple(range(colSize)), weight=1)

        # Shuffles tokens and possible walls for random selection later
        shuffle(self.avaibleTokens)
        shuffle(self.possWalls)

    def setControlBtns(self): 
        # Sets up roll die and end turn btns
        controlFrame = self.controlFrame

        controlFrame.grid(row=1, column=0, sticky="n")

        endBtn = Button(controlFrame, text="End turn", compound='c',
            height=gridCellSize, width=gridCellSize, 
            image=self.pixel, command=lambda: self.endTurnBtn())
        endBtn.pack(side="right", expand=True)
        endBtn["state"] = "disabled"

        rollDiceBtn = Button(controlFrame, text="Roll Die", compound='c',
            height=gridCellSize, width=gridCellSize, 
            image=self.pixel, command=lambda: self.rollDice())
        rollDiceBtn.pack(side="left", expand=True)

        self.endBtn = endBtn
        self.rollDiceBtn = rollDiceBtn

    def setPlayers(self, players):
        # Enables engine to access players
        self.players = players
    

    def configureGridBtn(self, x, y):
        # Configures a grid btn
        gridFrame = self.gridFrame

        btn = CanvasButton(gridFrame, x, y, self.clearColor, self.coin)

        # Assigns coordinates and function to btn
        btn.x = x 
        btn.y = y
        btn.setCmd(lambda: self.gridBtnFunc(btn) )

        # Checks if cell is far enough way from corner
        btn.tokenStatus = 0
        btn.tokenAvailable = 1
        for coord in itertools.product([0, rowSize - 1], [0, colSize - 1]):
            if math.dist(coord, (x, y)) < cornerTokenBuffer:
                btn.tokenAvailable = 0
                break

        if btn.tokenAvailable:
            self.avaibleTokens.append( (x, y) )
        
        # Finds all neighbors for btn to calc walls
        btn.neigh = []

        for move in [ [1, 0], [-1, 0], [0, 1], [0, -1] ]:
            if x + move[0] < 0 or x + move[0] == rowSize:
                continue
            if y + move[1] < 0 or y + move[1] == colSize:
                continue
            btn.neigh.append( (x + move[0], y + move[1]) )

            # Look at only right or down moves for walls
            if move[0] + move[1] == -1:
                continue

            self.possWalls.append( (x, y, x + move[0], y + move[1]) )
            
        # Add btn to grid array
        self.grid[x].append(btn)

    def gridBtnFunc(self, btn):
        # Function for when a grid btn is pressed
        # Checks if a move is valid, crosses a wall and 
        # if a player has captured a token

        # Check if move is valid
        if not self.checkValidMove(btn):
            return

        playerTurn = self.getPlayerTurn()
        player = self.players[playerTurn]

        # Clear previous position
        self.grid[player.x][player.y].changeColor(self.clearColor)
        
        if self.checkCrossWall(btn):
            
            self.showWallFunc(btn, player)

            # Update current position
            # Players starting position
            player.x = player.originX
            player.y = player.originY
            self.grid[player.x][player.y].changeColor(self.colors[playerTurn])

            # Update number of moves
            self.numMoves = 0
            self.rollDiceBtn["text"] = f"Remaining\nMoves:\n{self.numMoves}"

        else:
            # Update current position
            player.x = btn.x
            player.y = btn.y
            self.grid[player.x][player.y].changeColor(self.colors[playerTurn])

            # Update number of moves
            self.numMoves -= 1
            self.rollDiceBtn["text"] = f"Remaining\nMoves:\n{self.numMoves}"

            # Capture token if there
            if btn.tokenStatus == 1:
                self.captureToken(btn, player)
        
        if self.numMoves == 0:
            self.rollDiceBtn.configure(bg="#f00")

    def showWallFunc(self, btn, player):
        # Shows wall if encounter and enabled
        if not self.showWall:
            return
        
        bx, by = btn.x, btn.y
        px, py = player.x, player.y

        offset = gridCellSize // 2

        if bx == px:
            # Show Horizontal wall
            wx1 = bx * gridCellSize
            wy1 = ((by + py) / 2) * gridCellSize + offset

            wx2 = wx1 + gridCellSize
            wy2 = wy1
        else: 
            # Show vertical Wall
            wx1 = ((bx + px) / 2) * gridCellSize + offset
            wy1 = by * gridCellSize

            wx2 = wx1
            wy2 = wy1 + gridCellSize

        # Wall
        wallID = self.gridFrame.create_line(wx1, wy1, wx2, wy2, fill="red", width=5)
        
        if not self.showWallPerma:
            # Hide wall after delay
            self.gridFrame.after(1000, self.gridFrame.delete, wallID)

    def checkValidMove(self, btn):
        # Checks if a move is valid
        playerTurn = self.getPlayerTurn()

        # Check if cell is adjancent
        diffX = abs(btn.x - self.players[playerTurn].x)
        diffY = abs(btn.y - self.players[playerTurn].y)

        if diffX + diffY != 1:
           return False

        # Check if cell is empty
        for i in range(self.numPlayers):
            if playerTurn == i:
                continue

            if btn.x == self.players[i].x and btn.y == self.players[i].y:
                return False   

        # Check if has remaining Moves
        if self.numMoves == 0:
            return False

        return True

    def checkCrossWall(self, btn):
        # Check if cell is neighbor of current cell
        playerTurn = self.getPlayerTurn()

        px = self.players[playerTurn].x
        py = self.players[playerTurn].y

        bx = btn.x
        by = btn.y

        return (px, py) not in self.grid[bx][by].neigh


    def placeToken(self):
        # Place a token on the grid
        if len(self.avaibleTokens) == 0:
            self.endGame()
            return

        coord = self.avaibleTokens.pop()
        
        self.grid[coord[0]][coord[1]].tokenStatus = 1
        self.grid[coord[0]][coord[1]].configure(True)

        # In on a player, capture token
        # Delay by 500ms to let players see
        for player in self.players:
            if coord == (player.x, player.y):
                self.root.after(500, lambda: self.captureToken(self.grid[coord[0]][coord[1]], player))

    def captureToken(self, btn, player):
        # Enables a player to capture a token
        # Updates image and score
        playerTurn = self.getPlayerTurn()

        btn.tokenStatus = 0
        btn.tokenAvailable = 0
        btn.configure(False)
        self.players[playerTurn].points += 1

        self.placeToken()


    def endGame(self):
        # If there are no more tokens, find highest scoring player
        playerID = 0
        topScore = 0

        for player in self.players:
            if player.points > topScore:
                topScore = player.points
                playerID = player.id

        self.label["text"] = f"Winner is player {colors[playerID]}"


    def endTurnBtn(self):
        # Ends current turn
        self.incPlayerTurn()
        self.rollDiceBtn["state"] = "normal"
        self.rollDiceBtn["text"] = f"Roll Die"
        self.rollDiceBtn.configure(bg="#fff")

        self.endBtn["state"] = "disabled"

        playerTurn = self.getPlayerTurn()
        self.label["text"] = f"It is {colors[playerTurn]}'s turn"
        
    def rollDice(self):
        # Rolls the die and enable end/skip turn
        self.numMoves = randint(1, maxDiceNum)
        self.rollDiceBtn["state"] = "disabled"
        self.rollDiceBtn["text"] = f"Remaining\nMoves:\n{self.numMoves}"

        self.endBtn["state"] = "normal"


    def allVisitable(self):
        # Use BFS to check if all cells are visitable
        # Return True if yes, False otherwise
        count = 0

        visited = [(0, 0)]
        queue = [(0, 0)]
        
        while queue:
            x, y = queue.pop()
            count += 1
            for neigh in self.grid[x][y].neigh:
                if neigh not in visited:
                    queue.append(neigh)
                    visited.append(neigh)
        
        return count == rowSize * colSize
    
    def makeMaze(self):
        # Generate a maze on the current map
        count = 0

        while count < numWalls and len(self.possWalls) > 0:
            # Add a wall and test if valid
            x1, y1, x2, y2 = self.possWalls.pop()
            self.grid[x1][y1].neigh.remove( (x2, y2) )
            self.grid[x2][y2].neigh.remove( (x1, y1) )

            if not self.allVisitable():
                # Not all cells visitable, remove walls
                self.grid[x1][y1].neigh.append( (x2, y2) )
                self.grid[x2][y2].neigh.append( (x1, y1) )
            else:
                count += 1

    def showPaths(self):
        # Shows all routes
        gridFrame = self.gridFrame

        offset = gridCellSize // 2

        for x in range(rowSize):
            for y in range(colSize):
                for neigh in self.grid[x][y].neigh:
                    x1 = x * gridCellSize + offset
                    y1 = y * gridCellSize + offset
                    x2 = neigh[0] * gridCellSize + offset
                    y2 = neigh[1] * gridCellSize + offset

                    gridFrame.create_line(x1, y1, x2, y2, fill="black", width=5)
