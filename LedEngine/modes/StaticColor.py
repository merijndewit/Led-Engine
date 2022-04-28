from LedStrip import LedStrip
from pixel_manager import PixelManager
from color import Color

class StaticColor(LedStrip):
    def __init__(self) -> None:
        super().__init__()

    def super_init(self):
        super().__init__()

    def setColor(self, hex_color):
        #super().__init__()
        #self.neopixels.fill((int(color[1:3], 16) * (self.Rpercentage / 100)*(self.ledBrightness / 100), int(color[3:5], 16) * (self.Gpercentage / 100)*(self.ledBrightness / 100), int(color[5:7], 16) * (self.Bpercentage / 100)*(self.ledBrightness / 100)))
        col = Color()
        col.set_color_hex(hex_color)
        PixelManager.fill_colors(col)
        PixelManager.show_all()
        print("showpixels")
