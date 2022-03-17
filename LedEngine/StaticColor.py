from LedStrip import LedStrip

class StaticColor(LedStrip):
    def __init__(self):
        pass

    @classmethod
    def setColor(cls, R, G, B):
        cls.pixels.fill((R * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), G * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), B * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
        cls.pixels.show()
