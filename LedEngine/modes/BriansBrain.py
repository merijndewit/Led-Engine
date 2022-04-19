import random
import time

from LedPanel import LedPanel
from pixel_manager import PixelManager

class BriansBrain(LedPanel):
    
    def __init__(self):
        super().__init__()
        self.grid = []
        self.cols = 0
        self.rows = 0

    def Start(self):
        super().__init__()
        self.cols = self.ledPanelsPixelWidth
        self.rows = self.ledPanelsPixelHeight
        print(self.cols, self.rows)

        listRow = [0] * self.rows
        listCol = []
        for i in range(self.cols): 
            for j in range(self.rows):
                listRow[j] = int(random.randint(0, 2))
            listCol.append(listRow)
            listRow = [0] * self.cols
        self.grid = listCol
        while True:
            self.drawBriansBrain()

    def drawBriansBrain(self):
        for i in range(self.cols):
            for j in range(self.rows):
                pixel = self.getPixelNumber(j, i)
                if (self.grid[i][j] == 1):
                    PixelManager.Set_Pixel(pixel, (0, 100, 0), True)
                elif(self.grid[i][j] == 2):
                    PixelManager.Set_Pixel(pixel, (100, 0, 0), True)
                else:
                    PixelManager.Set_Pixel(pixel, (0, 0, 0), True)
        PixelManager.Show_All()
        
        nextGrid = self.grid
        for i in range(self.cols):
            for j in range(self.rows):
                if (self.grid[i][j] == 2):
                    nextGrid[i][j] = 1 #set the cell to dying state
                elif (self.grid[i][j] == 1):
                    nextGrid[i][j] = 0
                elif (self.grid[i][j] == 0):
                    neighbors = self.countNeighborsBriansBrain(i, j)
                    if (neighbors == 2):
                        nextGrid[i][j] = 2
        self.grid = nextGrid
        time.sleep(0.5)

    def countNeighborsBriansBrain(self, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                if (self.grid[col][row] == 2):
                    sum += 1
        return sum;