import board
import neopixel
import time
import colorsys

pixelCount = 120
pixels = neopixel.NeoPixel(board.D21, pixelCount, auto_write=False)
ledBrightness = 100
#rainbow variables
waveLength = 10
rainbowSpeed = 10

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
    print("updated wavelengthvalue to: " + str(waveLength))
def SetSpeedValue(speedValue):
    global rainbowSpeed
    rainbowSpeed = speedValue
    print("updated wavelengthvalue to: " + str(speedValue))

def rainbow_cycle():
    global ledBrightness
    global waveLength
    global rainbowSpeed
    h = 0
    s = 1
    v = ledBrightness / 5000
    while True:
        for i in range(pixelCount):
            hh = (i / waveLength) + h
            if hh >= 1:
                hh -= 1
            rgb = colorsys.hsv_to_rgb(hh, s, v)
            pixels[i] = ((rgb[0] * 255, rgb[1] * 255, rgb[2] * 255))
            h += 0.0001
            time.sleep(0.001 / (rainbowSpeed / 100))
        pixels.show()
        if h == 1:
            h == 0

def setPixel(x, y, color):
    print(x, y, color)
    pixel = int(getPixelNumber(x, y))
    pixels[pixel] = (int(color[:2], 16) / 70, int(color[2:4], 16) / 70, int(color[4:6], 16) / 70)  
    pixels.show()

# converts coordinates to the pixel number on the led panel
# this function is for an led panel with a zigzag pattern
# LedStrip:  
#   _________
#   _________|
#  |_________
#   _________|
#  |_________

def getPixelNumber(corX, corY):
    rowX = []
    x = 11 #width
    y = 11 #height
    for i in range(x):
        rowY = []
        for ii in range(y):
            if (i % 2) == 0: #check if number is even
                rowY.append((i * y) + ii)
            else:
                rowY.insert(0, ((i * y) + ii))
        rowX.append(rowY)
    return rowX[int(corY)][int(corX)]


