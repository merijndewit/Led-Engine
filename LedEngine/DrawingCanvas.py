from LedPanel import LedPanel

class DrawingCanvas(LedPanel):

    def setPixel(self, x, y, color):
        print("set hex:", color)
        LedPanel.pixelArray[int(x)][int(y)] = color
        pixel = int(LedPanel.getPixelNumber(x, y))
        LedPanel.pixels[pixel] = (int(color[1:3], 16) * (self.Rpercentage / 100)*(self.ledBrightness / 100), int(color[3:5], 16) * (self.Gpercentage / 100)*(self.ledBrightness / 100), int(color[5:7], 16) * (self.Bpercentage / 100)*(self.ledBrightness / 100))
        
        LedPanel.pixels.show()