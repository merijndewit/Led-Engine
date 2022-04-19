import time

from LedStrip import LedStrip
from pixel_manager import PixelManager

class KnightRider(LedStrip):

    def __init__(self) -> None:
        super().__init__()

        self.knightRiderFade = 100
        self.knightRiderSpeed = 1

    def setKnightRiderFade(self, value):
        self.knightRiderFade = int(value)

    def setKnightRiderSpeed(self, value):
        self.knightRiderSpeed = int(value)

    def Start(self):
        super().__init__()
        neighbors = []
        pixelStrength = 100
        while pixelStrength >= 15:
            strength = pixelStrength / (1 + (self.knightRiderFade * 0.001))
            if pixelStrength >= 15:
                neighbors.append(strength)
                pixelStrength = pixelStrength / (1 + (self.knightRiderFade * 0.001))
            else:
                break
        if len(neighbors) * 2 >= self.pixelCount:
            print("Please increse fade")
            return

        while True:
            for position in range(self.pixelCount):
                self.neopixels[position] = ((self.oneColorModeHex[0] * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                for neighborPixel in range(len(neighbors)):
                    neighborFront = position + neighborPixel + 1
                    if neighborFront <= 255:
                        self.neopixels[neighborFront] = ((self.oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1]  * (neighbors[neighborPixel] / 100) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                    neighborRear = position - neighborPixel - 1
                    if neighborRear >= 0:

                        self.neopixels[neighborRear] = ((self.oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1]  * (neighbors[neighborPixel] / 100) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                    self.neopixels[neighborRear - len(neighbors)] = ((0, 0, 0))
                time.sleep(self.knightRiderSpeed * 0.001)
                self.neopixels.show()

            for pixel in range(self.pixelCount - 1, 0, -1):
                self.neopixels[pixel] = ((self.oneColorModeHex[0] * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                #show neighbors
                for neighborPixel in range(len(neighbors)):
                    neighborFront = pixel + neighborPixel + 1
                    if neighborFront <= 255:
                        self.neopixels[neighborFront] = ((self.oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (neighbors[neighborPixel] / 100) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                    neighborRear = pixel - neighborPixel - 1
                    if neighborRear >= 0:

                        self.neopixels[neighborRear] = ((self.oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (self.Rpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[1] * (neighbors[neighborPixel] / 100) * (self.Gpercentage / 100)*(self.ledBrightness / 100), self.oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                    if (neighborFront + len(neighbors) <= self.pixelCount):
                        self.neopixels[neighborFront + len(neighbors) - 1] = ((0, 0, 0))
                time.sleep(self.knightRiderSpeed * 0.001)
                self.neopixels.show()

