from LedStrip import LedStrip

class StaticColor(LedStrip):
    def __init__(self):
        pass

    @classmethod
    def setColor(cls, color):
        cls.pixels.fill((int(color[1:3], 16) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), int(color[3:5], 16) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), int(color[5:7], 16) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
        cls.pixels.show()
