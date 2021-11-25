import board
import neopixel
pixels = neopixel.NeoPixel(board.D21, 30)

def setColor(R, G, B):
    pixels.fill((R, G, B))
