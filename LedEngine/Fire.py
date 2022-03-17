import random

from LedStrip import LedStrip


class Fire(LedStrip):
    @classmethod
    def Start(cls):
        pixelList = []
        for i in range(cls.pixelCount):
            pixelList.append(int(random.randint(0, 255)))
        while True:
            for pixel in range(cls.pixelCount):
                cls.pixels[pixel] = ((cls.oneColorModeHex[0]*(pixelList[pixel] / 255) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), cls.oneColorModeHex[1] * (pixelList[pixel] / 255) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), cls.oneColorModeHex[2] * (pixelList[pixel] / 255) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
                if pixelList[pixel] <= 0:
                    pixelList[pixel] = 255
                else:
                    pixelList[pixel] -= 1
            cls.pixels.show()
            