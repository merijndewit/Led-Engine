import board
import neopixel
import time

pixelCount = 13
canRun = True

pixels = neopixel.NeoPixel(board.D21, pixelCount)

def Clear():
    pixels.fill((0, 0, 0))

def setColor(R, G, B):
    pixels.fill((R, G, B))

def rainbow_cycle():
    pixels.fill((0, 0, 0))
    R = 255
    G = 0
    B = 0
    while canRun:
        if R == 255 and G == 0:
            B += 1
            pixels.fill((R, G, B))
            time.sleep(0.005)
        if B == 255 and R != 0:
            R -= 1
            pixels.fill((R, G, B))
            time.sleep(0.005)
        if B == 255 and R == 0:
            G += 1
            pixels.fill((R, G, B))
            time.sleep(0.005)
        if G == 255 and B != 0:
            B -= 1
            pixels.fill((R, G, B))
            time.sleep(0.005)
        if G == 255 and B == 0:
            R += 1
            pixels.fill((R, G, B))
            time.sleep(0.005)
        if R == 255 and G != 0:
            G -= 1
            pixels.fill((R, G, B))
            time.sleep(0.005)