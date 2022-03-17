import random
import time

from LedPanel import LedPanel

class BriansBrain(LedPanel):
    grid = []
    cols = 0
    rows = 0
    
    @classmethod
    def Start(cls):
        BriansBrain.cols = LedPanel.ledPanelsPixelWidth
        BriansBrain.rows = LedPanel.ledPanelsPixelHeight

        listRow = [0] * BriansBrain.rows
        listCol = []
        for i in range(BriansBrain.cols): 
            for j in range(BriansBrain.rows):
                listRow[j] = int(random.randint(0, 2))
            listCol.append(listRow)
            listRow = [0] * BriansBrain.cols
        BriansBrain.grid = listCol
        while True:
            BriansBrain.drawBriansBrain()

    def drawBriansBrain():
        for i in range(BriansBrain.cols):
            for j in range(BriansBrain.rows):
                pixel = LedPanel.getPixelNumber(j, i)
                if (BriansBrain.grid[i][j] == 1):
                    LedPanel.pixels[pixel] = (0, 1, 0)
                elif(BriansBrain.grid[i][j] == 2):
                    LedPanel.pixels[pixel] = (1, 0, 0)
                else:
                    LedPanel.pixels[pixel] = (0, 0, 0)
        LedPanel.pixels.show()
        
        nextGrid = BriansBrain.grid
        for i in range(BriansBrain.cols):
            for j in range(BriansBrain.rows):
                if (BriansBrain.grid[i][j] == 2):
                    nextGrid[i][j] = 1 #set the cell to dying state
                elif (BriansBrain.grid[i][j] == 1):
                    nextGrid[i][j] = 0
                elif (BriansBrain.grid[i][j] == 0):
                    neighbors = BriansBrain.countNeighborsBriansBrain(BriansBrain.grid, i, j)
                    if (neighbors == 2):
                        nextGrid[i][j] = 2
        BriansBrain.grid = nextGrid
        time.sleep(0.5)

    def countNeighborsBriansBrain(grid, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + BriansBrain.cols) % BriansBrain.cols
                row = (y + j + BriansBrain.rows) % BriansBrain.rows
                if (grid[col][row] == 2):
                    sum += 1
        return sum;