import board
import neopixel
import time
import colorsys

pixelCount = 13
pixels = neopixel.NeoPixel(board.D21, pixelCount, auto_write=False)
ledBrightness = 100
#rainbow variables
waveLength = 10

def Clear():
    pixels.fill((0, 0, 0))
    pixels.show()

def setColor(R, G, B):
    pixels.fill((R, G, B))
    pixels.show()

def SetBrightness(brightnessValue):
    global ledBrightness
    ledBrightness = brightnessValue

def SetwaveLength(waveLengthValue):
    global waveLength
    waveLength = waveLengthValue

def rainbow_cycle():
    h = 0
    s = 1
    v = ledBrightness / 100
    while True:
        for i in range(pixelCount):
            hh = (i / waveLength) + h
            if hh >= 1:
                hh -= 1
            rgb = colorsys.hsv_to_rgb(hh, s, v)
            pixels[i] = ((rgb[0] * 255, rgb[1] * 255, rgb[2] * 255))
            h += 0.001
            time.sleep(0.001)
        pixels.show()
        if h == 1:
            h == 0


