import time

from LedPanel import LedPanel

class WireWorld(LedPanel):
    wireWorldGrid = []
    wireWorldPixels = []
    cols = 0
    rows = 0

    class wireWorldPixel:
        x = 0
        y = 0
        more = 0

    def setWireWorldPixel(x, y, mode):
        wireWorldPixel = WireWorld.wireWorldPixel()
        wireWorldPixel.x = x
        wireWorldPixel.y = y
        wireWorldPixel.mode = mode
        WireWorld.wireWorldPixels.append(wireWorldPixel)

    @classmethod
    def Start(cls):
        WireWorld.wireWorldGrid = LedPanel.make2DArray(LedPanel.ledPanelsPixelWidth, LedPanel.ledPanelsPixelHeight)
        for i in range(len(WireWorld.wireWorldPixels)):
            WireWorld.wireWorldGrid[WireWorld.wireWorldPixels[i].x][WireWorld.wireWorldPixels[i].y] = WireWorld.wireWorldPixels[i].mode

        WireWorld.cols = LedPanel.ledPanelsPixelWidth
        WireWorld.rows = LedPanel.ledPanelsPixelHeight

        while True:
            WireWorld.RunWireWorld()

    def RunWireWorld():
        for j in range(WireWorld.cols):
            for i in range(WireWorld.rows):
                pixel = LedPanel.getPixelNumber(j, i)
                if (WireWorld.wireWorldGrid[j][i] == 0):
                    LedPanel.pixels[pixel] = (0, 0, 0)
                elif (WireWorld.wireWorldGrid[j][i] == 1):
                    LedPanel.pixels[pixel] = (1, 1, 0)
                elif (WireWorld.wireWorldGrid[j][i] == 2):
                    LedPanel.pixels[pixel] = (0, 0, 1)
                elif (WireWorld.wireWorldGrid[j][i] == 3):
                    LedPanel.pixels[pixel] = (1, 0, 0)
        nextgrid = LedPanel.make2DArray(WireWorld.cols, WireWorld.rows)
        LedPanel.pixels.show()
        time.sleep(0.5)
        
        for i in range(WireWorld.cols):
            for j in range(WireWorld.rows):
                if (WireWorld.wireWorldGrid[i][j] == 1):
                    neighbors = WireWorld.countNeighborsWireWorld(WireWorld.wireWorldGrid, i, j)
                    if (neighbors == 1 or neighbors == 2):
                        nextgrid[i][j] = 2
                    else:
                        nextgrid[i][j] = 1
                elif (WireWorld.wireWorldGrid[i][j] == 2):
                    nextgrid[i][j] = 3
                elif (WireWorld.wireWorldGrid[i][j] == 3):
                    nextgrid[i][j] = 1
        WireWorld.wireWorldGrid = nextgrid

    def countNeighborsWireWorld(wireWorldGrid, x, y):
        sum = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + WireWorld.cols) % WireWorld.cols
                row = (y + j + WireWorld.rows) % WireWorld.rows
                if (wireWorldGrid[col][row] == 2):
                    sum += 1
        return sum;