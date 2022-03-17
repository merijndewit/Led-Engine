import random
import time

from LedPanel import LedPanel

class GameOfLife(LedPanel):
    grid = []
    cols = LedPanel.ledPanelsPixelWidth
    rows = LedPanel.ledPanelsPixelHeight

    @classmethod
    def Start(cls):
        GameOfLife.cols = LedPanel.ledPanelsPixelWidth
        GameOfLife.rows = LedPanel.ledPanelsPixelHeight
        listRow = [0] * GameOfLife.rows
        listCol = []
        for i in range(GameOfLife.cols): 
            for j in range(GameOfLife.rows):
                listRow[j] = int(random.randint(0, 1))
            listCol.append(listRow)
            listRow = [0] * GameOfLife.cols
        GameOfLife.grid = listCol
        while True:
            GameOfLife.draw()

    def draw():
        for i in range(GameOfLife.cols):
            for j in range(GameOfLife.rows):
                pixel = LedPanel.getPixelNumber(j, i)
                if (GameOfLife.grid[i][j] == 1):
                    LedPanel.pixels[pixel] = (0.5, 1, 0.5)
                else:
                    LedPanel.pixels[pixel] = (0, 0, 0)
        LedPanel.pixels.show()
        time.sleep(0.1)
        listCol = []
        listRow = [0] * GameOfLife.rows
        for i in range(GameOfLife.cols):
            for j in range(GameOfLife.rows):
                state = GameOfLife.grid[i][j]
                neighbors = GameOfLife.countNeighbors(GameOfLife.grid, i, j)
                if (state == 0 and neighbors == 3):
                    listRow[j] = 1
                elif (state == 1 and (neighbors < 2 or neighbors > 3)):
                    listRow[j] = 0
                else:
                    listRow[j] = state
            listCol.append(listRow)
            listRow = [0] * GameOfLife.cols
        GameOfLife.grid = listCol

    def countNeighbors(grid, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + GameOfLife.cols) % GameOfLife.cols
                row = (y + j + GameOfLife.rows) % GameOfLife.rows
                sum += grid[col][row]
        sum -= grid[x][y];
        return sum;
