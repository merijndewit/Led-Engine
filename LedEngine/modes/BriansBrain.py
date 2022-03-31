import random
import time

from LedPanel import LedPanel

class BriansBrain(LedPanel):
    
    def __init__(self):
        self.grid = []
        self.cols = 0
        self.rows = 0

    @classmethod
    def Start(self):
        self.cols = self.ledPanelsPixelWidth
        self.rows = self.ledPanelsPixelHeight

        listRow = [0] * self.rows
        listCol = []
        for i in range(self.cols): 
            for j in range(self.rows):
                listRow[j] = int(random.randint(0, 2))
            listCol.append(listRow)
            listRow = [0] * self.cols
        self.grid = listCol
        while True:
            self.drawBriansBrain(self)

    def drawBriansBrain(self):
        for i in range(self.cols):
            for j in range(self.rows):
                pixel = self.getPixelNumber(j, i)
                if (self.grid[i][j] == 1):
                    self.pixels[pixel] = (0, 1, 0)
                elif(self.grid[i][j] == 2):
                    self.pixels[pixel] = (1, 0, 0)
                else:
                    self.pixels[pixel] = (0, 0, 0)
        self.pixels.show()
        
        nextGrid = self.grid
        for i in range(self.cols):
            for j in range(self.rows):
                if (self.grid[i][j] == 2):
                    nextGrid[i][j] = 1 #set the cell to dying state
                elif (self.grid[i][j] == 1):
                    nextGrid[i][j] = 0
                elif (self.grid[i][j] == 0):
                    neighbors = self.countNeighborsBriansBrain(self, self.grid, i, j)
                    if (neighbors == 2):
                        nextGrid[i][j] = 2
        self.grid = nextGrid
        time.sleep(0.5)

    def countNeighborsBriansBrain(self, grid, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                if (grid[col][row] == 2):
                    sum += 1
        return sum;