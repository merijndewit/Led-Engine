import board
import neopixel
import time

pixelCount = 13
pixels = neopixel.NeoPixel(board.D21, pixelCount)

def Clear():
    pixels.fill((0, 0, 0))

def SetBrightness(brightnessValue):
    pixels.brightness = brightnessValue

def setColor(R, G, B):
    pixels.fill((R, G, B))

def rainbow_cycle():
    R = 255
    G = 0
    B = 0
    while True:
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

#def wave():
#    while True:
#        for j in range(256*5):
#            for i in range(pixelCount):
#                pixels.setPixelColor(i, wheel(((i * 256 // pixels.numPixels()) + j) & 255))
#        pixels.show()
#        time.sleep(0.3)
#

