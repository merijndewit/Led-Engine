import random
import time

from LedPanel import LedPanel

class GameOfLife(LedPanel):
    _grid = []
    _cols = LedPanel.ledPanelsPixelWidth
    _rows = LedPanel.ledPanelsPixelHeight

    def _Start(self):
        GameOfLife._cols = LedPanel.ledPanelsPixelWidth
        GameOfLife._rows = LedPanel.ledPanelsPixelHeight
        __listRow = [0] * GameOfLife._rows
        __listCol = []
        for i in range(GameOfLife._cols):
            for j in range(GameOfLife._rows):
                __listRow[j] = int(random.randint(0, 1))
            __listCol.append(__listRow)
            __listRow = [0] * GameOfLife._cols
        GameOfLife._grid = __listCol
        while True:
            GameOfLife.__draw()

    def __draw():
        for i in range(GameOfLife._cols):
            for j in range(GameOfLife._rows):
                pixel = LedPanel.getPixelNumber(j, i)
                if (GameOfLife._grid[i][j] == 1):
                    LedPanel.pixels[pixel] = (0.5, 1, 0.5)
                else:
                    LedPanel.pixels[pixel] = (0, 0, 0)
        LedPanel.pixels.show()
        time.sleep(0.1)
        __listCol = []
        __listRow = [0] * GameOfLife._rows
        for i in range(GameOfLife._cols):
            for j in range(GameOfLife._rows):
                __state = GameOfLife._grid[i][j]
                __neighbors = GameOfLife.__countNeighbors(GameOfLife._grid, i, j)
                if (__state == 0 and __neighbors == 3):
                    __listRow[j] = 1
                elif (__state == 1 and (__neighbors < 2 or __neighbors > 3)):
                    __listRow[j] = 0
                else:
                    __listRow[j] = __state
            __listCol.append(__listRow)
            __listRow = [0] * GameOfLife._cols
        GameOfLife._grid = __listCol

    def __countNeighbors(_grid, x, y):
        __sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                __col = (x + i + GameOfLife._cols) % GameOfLife._cols
                __row = (y + j + GameOfLife._rows) % GameOfLife._rows
                __sum += _grid[__col][__row]
        __sum -= _grid[x][y];
        return __sum;
