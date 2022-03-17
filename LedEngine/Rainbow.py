import colorsys
import time

from LedStrip import LedStrip

class Rainbow(LedStrip):
    waveLength = 100
    rainbowSpeed = 100

    def SetwaveLength(waveLengthValue):
        Rainbow.waveLength = waveLengthValue
    
    def SetSpeedValue(speedValue):
        Rainbow.rainbowSpeed = speedValue
    @classmethod
    def Start(self):
        h = 0
        s = 1
        while True:
            for i in range(self.pixelCount):
                hh = (i / self.waveLength) + h
                if hh >= 1:
                    hh -= 1
                rgb = colorsys.hsv_to_rgb(hh, s, 1)
                self.pixels[i] = (((rgb[0] * 255) * (self.Rpercentage / 100)*(self.ledBrightness / 100), (rgb[1] * 255) * (self.Gpercentage / 100)*(self.ledBrightness / 100), (rgb[2] * 255) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
                h += 0.0001
                time.sleep(0.001 / (self.rainbowSpeed / 100))
            self.pixels.show()
            if h == 1:
                h == 0