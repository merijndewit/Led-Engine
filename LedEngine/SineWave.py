import time
import math

from LedStrip import LedStrip

class SineWave(LedStrip):
    sineWaveFrequency = 1
    sineWaveLength = 1

    def setSineWaveFrequency(value):
        SineWave.sineWaveFrequency = value

    def setSineWaveLength(value):
        SineWave.sineWaveLength = value / 100

    def Start(self):
        startTime = time.time()
        while True:
            for i in range(self.pixelCount):
                result = math.sin(SineWave.sineWaveFrequency*(time.time() - startTime)+(SineWave.sineWaveLength * i))
                self.pixels[i] = (((((result + 1)/2) * self.oneColorModeHex[0]) * (self.Rpercentage / 100)*(self.ledBrightness / 100), (((result + 1)/2) * self.oneColorModeHex[1]) * (self.Gpercentage / 100)*(self.ledBrightness / 100), (((result + 1)/2) * self.oneColorModeHex[2]) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
            self.pixels.show()
            #time.sleep(0.01)