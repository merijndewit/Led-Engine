import board
import neopixel
import time
import colorsys

pixelCount = 13
pixels = neopixel.NeoPixel(board.D21, pixelCount, auto_write=False)

def Clear():
    pixels.fill((0, 0, 0))

def SetBrightness(brightnessValue):
    pixels.brightness = brightnessValue

def setColor(R, G, B):
    pixels.fill((R, G, B))

def rainbow_cycle():
    h = 0
    s = 1
    v = 0.2
    while True:
        for i in range(pixelCount):
            hh = (i * 10 / 256) + h
            if hh >= 1:
                hh -= 1
            rgb = colorsys.hsv_to_rgb(hh, s, v)
            pixels[i] = ((rgb[0] * 255, rgb[1] * 255, rgb[2] * 255))
            h += 0.001
            time.sleep(0.01)
        pixels.show()
        if h == 1:
            h == 0
