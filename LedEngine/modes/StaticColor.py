from LedStrip import LedStrip

class StaticColor(LedStrip):
    def __init__(self) -> None:
        super().__init__()

    def setColor(self, color):
        super().__init__()
        self.pixels.fill((int(color[1:3], 16) * (self.Rpercentage / 100)*(self.ledBrightness / 100), int(color[3:5], 16) * (self.Gpercentage / 100)*(self.ledBrightness / 100), int(color[5:7], 16) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
        self.pixels.show()
