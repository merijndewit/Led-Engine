import random
import time

from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class GameOfLife(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
        self.grid = []
        self.cols = self.ledPanelsPixelWidth
        self.rows = self.ledPanelsPixelHeight

    def Start(self):
        super().__init__()
        self.cols = self.ledPanelsPixelWidth
        self.rows = self.ledPanelsPixelHeight
        listRow = [0] * self.rows
        listCol = []
        for i in range(self.cols): 
            for j in range(self.rows):
                listRow[j] = int(random.randint(0, 1))
            listCol.append(listRow)
            listRow = [0] * self.cols
        self.grid = listCol
        while True:
            self.draw()

    def draw(self):
        for i in range(self.cols):
            for j in range(self.rows):
                pixel = self.getPixelNumber(j, i)
                if (self.grid[i][j] == 1):
                    PixelManager.set_color(Color(50, 100, 50), pixel)
                else:
                    PixelManager.set_color(Color(0, 0, 0), pixel)
        PixelManager.show_all()
        time.sleep(0.1)
        listCol = []
        listRow = [0] * self.rows
        for i in range(self.cols):
            for j in range(self.rows):
                state = self.grid[i][j]
                neighbors = self.countNeighbors(self.grid, i, j)
                if (state == 0 and neighbors == 3):
                    listRow[j] = 1
                elif (state == 1 and (neighbors < 2 or neighbors > 3)):
                    listRow[j] = 0
                else:
                    listRow[j] = state
            listCol.append(listRow)
            listRow = [0] * self.cols
        self.grid = listCol

    def countNeighbors(self, grid, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                sum += grid[col][row]
        sum -= grid[x][y];
        return sum;
