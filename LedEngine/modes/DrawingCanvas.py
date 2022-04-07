from LedPanel import LedPanel

class DrawingCanvas(LedPanel):

    def __init__(self) -> None:
        super().__init__()

    def setPixel(self, aDict):
        x = aDict.get("X")
        y = aDict.get("Y")
        color = aDict.get("color")
        self.pixelArray[int(x)][int(y)] = color
        pixel = int(self.getPixelNumber(x, y))
        self.pixels[pixel] = (int(color[1:3], 16) * (self.Rpercentage / 100)*(self.ledBrightness / 100), int(color[3:5], 16) * (self.Gpercentage / 100)*(self.ledBrightness / 100), int(color[5:7], 16) * (self.Bpercentage / 100)*(self.ledBrightness / 100))
        
        self.pixels.show()