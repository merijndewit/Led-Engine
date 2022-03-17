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

    @classmethod
    def Start(cls):
        startTime = time.time()
        while True:
            for i in range(cls.pixelCount):
                result = math.sin(SineWave.sineWaveFrequency*(time.time() - startTime)+(SineWave.sineWaveLength * i))
                cls.pixels[i] = (((((result + 1)/2) * cls.oneColorModeHex[0]) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), (((result + 1)/2) * cls.oneColorModeHex[1]) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), (((result + 1)/2) * cls.oneColorModeHex[2]) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
            cls.pixels.show()
            #time.sleep(0.01)