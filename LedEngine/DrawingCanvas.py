from LedPanel import LedPanel

class DrawingCanvas(LedPanel):

    @classmethod
    def setPixel(cls, x, y, color):
        print("set hex:", color)
        LedPanel.pixelArray[int(x)][int(y)] = color
        pixel = int(LedPanel.getPixelNumber(x, y))
        print(cls.ledBrightness)
        LedPanel.pixels[pixel] = (int(color[1:3], 16) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), int(color[3:5], 16) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), int(color[5:7], 16) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
        
        LedPanel.pixels.show()