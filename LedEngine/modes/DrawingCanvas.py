from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class DrawingCanvas(LedPanel):

    def __init__(self) -> None:
        super().__init__()

    def super_init(self):
        super().__init__()

    def setPixel(self, pixel):
        x = pixel.get("X")
        y = pixel.get("Y")
        color = pixel.get("color")
        col = Color(int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
        
        pixel = int(self.getPixelNumber(x, y))
        PixelManager.set_color(col, pixel, True)