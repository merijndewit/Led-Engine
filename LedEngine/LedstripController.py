import board
import neopixel
import time
import colorsys
from PIL import Image
import os

pixelCount = 320
pixels = neopixel.NeoPixel(board.D21, pixelCount, auto_write=False)
ledBrightness = 100
#rainbow variables
waveLength = 100
rainbowSpeed = 100

Roffset = 1
Goffset = 1
Boffset = 1

Rpercentage = 100
Gpercentage = 100
Bpercentage = 100

pixelArray = []

imageName = ""

def Clear():
    pixels.fill((0, 0, 0))
    pixels.show()

def setColor(R, G, B):
    pixels.fill((R * Roffset, G * Goffset, B * Boffset))
    pixels.show()

def SetBrightness(brightnessValue):
    global ledBrightness
    global Roffset
    global Goffset
    global Boffset
    ledBrightness = brightnessValue
    Roffset = (Rpercentage / 100)*(ledBrightness / 100)
    Goffset = (Gpercentage / 100)*(ledBrightness / 100)
    Boffset = (Bpercentage / 100)*(ledBrightness / 100)


def SetwaveLength(waveLengthValue):
    global waveLength
    waveLength = waveLengthValue
    print("updated wavelengthvalue to: " + str(waveLength))
def SetSpeedValue(speedValue):
    global rainbowSpeed
    rainbowSpeed = speedValue
    print("updated speed to: " + str(speedValue))

def rainbow_cycle():
    print("StartRainbow")
    global ledBrightness
    global waveLength
    global rainbowSpeed
    h = 0
    s = 1
    while True:
        for i in range(pixelCount):
            hh = (i / waveLength) + h
            if hh >= 1:
                hh -= 1
            rgb = colorsys.hsv_to_rgb(hh, s, 1)
            pixels[i] = (((rgb[0] * 255) * Roffset, (rgb[1] * 255) * Goffset, (rgb[2] * 255) * Boffset))
            h += 0.0001
            time.sleep(0.001 / (rainbowSpeed / 100))
        pixels.show()
        if h == 1:
            h == 0

def setPixel(x, y, color):
    global pixelArray
    pixelArray[int(x)][int(y)] = color
    pixel = int(getPixelNumber(x, y))
    pixels[pixel] = (int(color[:2], 16) * Roffset, int(color[2:4], 16) * Goffset, int(color[4:6], 16) * Boffset)  
    pixels.show()
    print(pixel)

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

def RedCalibration(percentage):
    global Roffset
    global Rpercentage
    Rpercentage = percentage
    Roffset = (percentage / 100)*(ledBrightness / 100)
def GreenCalibration(percentage):
    global Goffset
    global Gpercentage
    Gpercentage = percentage
    Goffset = (percentage / 100)*(ledBrightness / 100)
def BlueCalibration(percentage):
    global Boffset
    global Bpercentage
    Bpercentage = percentage
    Boffset = (percentage / 100)*(ledBrightness / 100)

def NewPixelArray():
    global pixelArray
    x = 11 #width
    y = 11 #height
    for i in range(x):
        rowY = []
        for ii in range(y):
            rowY.append('#000000')
        pixelArray.append(rowY)
NewPixelArray()

def CreateImage():
    global pixelArray
    global imageName
    img = Image.new('RGB', [11,11], 255)
    data = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            string = str(pixelArray[x][y])
            data[x,y] = (int(string[1:3], 16), int(string[3:5], 16), int(string[5:7], 16))

    img.save('savedImages/'+imageName + '.png')

def SetImageName(value):
    global imageName
    imageName = value

def GetImageNames():
    imageNames = []
    for file in os.listdir("savedImages"):
        if file.endswith(".png"):
            imageNames.append(file)
    print(imageNames)
    return(imageNames)

GetImageNames()

