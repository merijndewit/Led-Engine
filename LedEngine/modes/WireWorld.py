import time

from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class WireWorld(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
        self.wireWorldGrid = []
        self.wireWorldPixels = []
        self.cols = 0
        self.rows = 0

    def super_init(self):
        super().__init__()

    class wireWorldPixel:
        x = 0
        y = 0
        mode = 0

    def setWireWorldPixel(self, aDict):
        x = aDict.get("X")
        y = aDict.get("Y")
        mode = aDict.get("mode")
        wireWorldPixel = self.wireWorldPixel()
        wireWorldPixel.x = x
        wireWorldPixel.y = y
        wireWorldPixel.mode = mode
        self.wireWorldPixels.append(wireWorldPixel)

    def Start(self):
        super().__init__()
        self.wireWorldGrid = self.make2DArray(self.ledPanelsPixelWidth, self.ledPanelsPixelHeight)
        for i in range(len(self.wireWorldPixels)):
            self.wireWorldGrid[self.wireWorldPixels[i].x][self.wireWorldPixels[i].y] = self.wireWorldPixels[i].mode

        self.cols = self.ledPanelsPixelWidth
        self.rows = self.ledPanelsPixelHeight

        while True:
            self.RunWireWorld()

    def RunWireWorld(self):
        for j in range(self.cols):
            for i in range(self.rows):
                pixel = self.getPixelNumber(j, i)
                if (self.wireWorldGrid[j][i] == 0):
                    col = Color(0, 0, 0)
                    PixelManager.set_color(col, pixel)
                elif (self.wireWorldGrid[j][i] == 1):
                    col = Color(200, 100, 0)
                    PixelManager.set_color(col, pixel)
                elif (self.wireWorldGrid[j][i] == 2):
                    col = Color(0, 0, 200)
                    PixelManager.set_color(col, pixel)
                elif (self.wireWorldGrid[j][i] == 3):
                    col = Color(200, 0, 0)
                    PixelManager.set_color(col, pixel)
        nextgrid = self.make2DArray(self.cols, self.rows)
        PixelManager.show_all()
        time.sleep(0.5)
        
        for i in range(self.cols):
            for j in range(self.rows):
                if (self.wireWorldGrid[i][j] == 1):
                    neighbors = self.countNeighborsWireWorld(self.wireWorldGrid, i, j)
                    if (neighbors == 1 or neighbors == 2):
                        nextgrid[i][j] = 2
                    else:
                        nextgrid[i][j] = 1
                elif (self.wireWorldGrid[i][j] == 2):
                    nextgrid[i][j] = 3
                elif (self.wireWorldGrid[i][j] == 3):
                    nextgrid[i][j] = 1
        self.wireWorldGrid = nextgrid

    def countNeighborsWireWorld(self, wireWorldGrid, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                if (wireWorldGrid[col][row] == 2):
                    count += 1
        return count