from LedPanel import LedPanel

class DrawingCanvas(LedPanel):

    @classmethod
    def setPixel(cls, aDict):
        x = aDict.get("X")
        y = aDict.get("Y")
        color = aDict.get("color")
        LedPanel.pixelArray[int(x)][int(y)] = color
        pixel = int(LedPanel.getPixelNumber(x, y))
        LedPanel.pixels[pixel] = (int(color[1:3], 16) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), int(color[3:5], 16) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), int(color[5:7], 16) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
        
        LedPanel.pixels.show()