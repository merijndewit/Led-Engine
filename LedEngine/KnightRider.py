import time

from LedStrip import LedStrip

class KnightRider(LedStrip):

    knightRiderFade = 100
    knightRiderSpeed = 1

    def setKnightRiderFade(value):
        KnightRider.knightRiderFade = value

    def setKnightRiderSpeed(value):
        KnightRider.knightRiderSpeed = value

    def Start(self):
        oneColorModeHex = self.oneColorModeHex
        pixels = self.pixels
        Rpercentage = self.Rpercentage
        Bpercentage = self.Bpercentage
        Gpercentage = self.Gpercentage
        ledBrightness = self.ledBrightness
        pixelCount = LedStrip.pixelCount

        neighbors = []
        pixelStrength = 100
        while pixelStrength >= 15:
            strength = pixelStrength / (1 + (KnightRider.knightRiderFade * 0.001))
            if pixelStrength >= 15:
                neighbors.append(strength)
                pixelStrength = pixelStrength / (1 + (KnightRider.knightRiderFade * 0.001))
            else:
                break
        if len(neighbors) * 2 >= pixelCount:
            print("Please increse fade")
            return

        while True:
            for position in range(pixelCount):
                pixels[position] = ((oneColorModeHex[0] * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1] * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (Bpercentage / 100)*(ledBrightness / 100)))
                for neighborPixel in range(len(neighbors)):
                    neighborFront = position + neighborPixel + 1
                    if neighborFront <= 255:
                        pixels[neighborFront] = ((oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1]  * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                    neighborRear = position - neighborPixel - 1
                    if neighborRear >= 0:

                        pixels[neighborRear] = ((oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1]  * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                    pixels[neighborRear - len(neighbors)] = ((0, 0, 0))
                time.sleep(KnightRider.knightRiderSpeed * 0.001)
                pixels.show()

            for pixel in range(pixelCount - 1, 0, -1):
                pixels[pixel] = ((oneColorModeHex[0] * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1] * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (Bpercentage / 100)*(ledBrightness / 100)))
                #show neighbors
                for neighborPixel in range(len(neighbors)):
                    neighborFront = pixel + neighborPixel + 1
                    if neighborFront <= 255:
                        pixels[neighborFront] = ((oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1] * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                    neighborRear = pixel - neighborPixel - 1
                    if neighborRear >= 0:

                        pixels[neighborRear] = ((oneColorModeHex[0] * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), oneColorModeHex[1] * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), oneColorModeHex[2] * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                    if (neighborFront + len(neighbors) <= pixelCount):
                        pixels[neighborFront + len(neighbors) - 1] = ((0, 0, 0))
                time.sleep(KnightRider.knightRiderSpeed * 0.001)     
                pixels.show()

