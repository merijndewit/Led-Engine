import random

from LedStrip import LedStrip
from pixel_manager import PixelManager

class Fire(LedStrip):

    def __init__(self) -> None:
        super().__init__()

    def Start(self):
        super().__init__()
        pixelList = []
        for i in range(self.pixelCount):
            pixelList.append(int(random.randint(0, 255)))
        while True:
            for pixel in range(self.pixelCount):
                r = self.oneColorModeHex[0]*(pixelList[pixel] / 255)
                g = self.oneColorModeHex[1]*(pixelList[pixel] / 255)
                b = self.oneColorModeHex[2]*(pixelList[pixel] / 255)
                PixelManager.Set_Pixel(pixel, (r, g, b), False)
                #self.neopixels[pixel] = ((self.oneColorModeHex[0]*(pixelList[pixel] / 255) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (pixelList[pixel] / 255) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (pixelList[pixel] / 255) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                if pixelList[pixel] <= 0:
                    pixelList[pixel] = 255
                else:
                    pixelList[pixel] -= 1
            PixelManager.Show_All()
            