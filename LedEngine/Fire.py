import random

from LedStrip import LedStrip

class Fire(LedStrip):
    def Start(self):
        global oneColorModeHex
        pixelList = []
        for i in range(self.pixelCount):
            pixelList.append(int(random.randint(0, 255)))
        while True:
            for pixel in range(self.pixelCount):
                self.pixels[pixel] = ((self.oneColorModeHex[0]*(pixelList[pixel] / 255) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (pixelList[pixel] / 255) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (pixelList[pixel] / 255) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                if pixelList[pixel] <= 0:
                    pixelList[pixel] = 255
                else:
                    pixelList[pixel] -= 1 
            self.pixels.show()