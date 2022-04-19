from LedPanel import LedPanel
from pixel_manager import PixelManager

class DrawingCanvas(LedPanel):

    def __init__(self) -> None:
        super().__init__()

    def setPixel(self, pixel):
        #super().__init__()
        x = pixel.get("X")
        y = pixel.get("Y")
        color = pixel.get("color")
        self.pixelArray[int(x)][int(y)] = color
        
        pixel = int(self.getPixelNumber(x, y))
        PixelManager.Show_Pixel(pixel, (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)), True)