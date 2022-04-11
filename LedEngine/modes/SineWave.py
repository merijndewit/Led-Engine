import time
import math

from LedStrip import LedStrip

class SineWave(LedStrip):
    
    def __init__(self) -> None:
        super().__init__()
    
        self.sineWaveFrequency = 1
        self.sineWaveLength = 1

    def setSineWaveFrequency(self, value):
        self.sineWaveFrequency = int(value)

    def setSineWaveLength(self, value):
        self.sineWaveLength = int(value) / 100

    def Start(self):
        super().__init__()
        startTime = time.time()
        while True:
            for i in range(self.pixelCount):
                result = math.sin(self.sineWaveFrequency*(time.time() - startTime)+(self.sineWaveLength * i))
                self.pixels[i] = (((((result + 1)/2) * self.oneColorModeHex[0]) * (self.Rpercentage / 100)*(self.ledBrightness / 100), (((result + 1)/2) * self.oneColorModeHex[1]) * (self.Gpercentage / 100)*(self.ledBrightness / 100), (((result + 1)/2) * self.oneColorModeHex[2]) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
            self.pixels.show()
            #time.sleep(0.01)