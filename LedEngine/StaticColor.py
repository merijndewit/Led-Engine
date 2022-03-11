from LedStrip import LedStrip

class StaticColor(LedStrip):
    def __init__(self):
        pass

    def setColor(self, R, G, B):
        self.pixels.fill((R * (self.Rpercentage / 100)*(self.ledBrightness / 100), G * (self.Gpercentage / 100)*(self.ledBrightness / 100), B * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
        self.pixels.show()
