import neopixel
import board

class LedLib():
    @classmethod
    def __init__(cls, pixels) -> None:
        cls.neopixels = neopixel.NeoPixel(board.D21, pixels, auto_write=False)
        
    @classmethod
    def show_pixels(cls):
        cls.neopixels.show()
        
    @classmethod
    def set_neopixel(cls, pixel_number, color_tup):
        cls.neopixels[pixel_number] = color_tup