import colorsys
import time

from LedStrip import LedStrip
from pixel_manager import PixelManager
from color import Color

class Rainbow(LedStrip):
    def __init__(self):
        super().__init__()
        self.waveLength = 100
        self.rainbowSpeed = 100
        #self.Start()

    def SetwaveLength(self, waveLengthValue):
        self.waveLength = int(waveLengthValue)
    
    def SetSpeedValue(self, speedValue):
        self.rainbowSpeed = int(speedValue)
        
    def Start(self):
        super().__init__()
        h = 0
        s = 1
        while True:
            for i in range(self.pixelCount):
                hh = (i / self.waveLength) + h
                if hh >= 1:
                    hh -= 1
                rgb = colorsys.hsv_to_rgb(hh, s, 1)
                col = Color(rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)
                PixelManager.set_color(col, i, False)
                h += 0.0001
                time.sleep(0.001 / (self.rainbowSpeed / 100))

            PixelManager.show_all()
            if h == 1:
                h == 0