import board
import neopixel
import time
import colorsys
from PIL import Image, ImageFont, ImageDraw
import os
import urllib.request
import json
import random
import math

pixelCount = 256

pixels = neopixel.NeoPixel(board.D21, pixelCount, auto_write=False)
ledBrightness = 100
#rainbow variables
waveLength = 100
rainbowSpeed = 100

Rpercentage = 100
Gpercentage = 100
Bpercentage = 100

ledPanelWidth = 0
ledPanelHeight = 0

pixelArray = []
wireWorldGrid = [] # 0 = off/nothing, 1 = conductor, 2 = Electron Head, 3 = ElectronTail 

imageName = ""

def NewPixelArray():
    global pixelArray
    global ledPanelWidth
    global ledPanelHeight
    pixelArray = []
    for i in range(ledPanelWidth):
        rowY = []
        for ii in range(ledPanelHeight):
            rowY.append('#000000')
        pixelArray.append(rowY)

def make2DArray(cols, rows):
    listRow = [0] * cols
    listCol = []
    for i in range(cols): 
        listCol.append(listRow.copy())
    return listCol

def CreateWireWorld2dArray():
    global wireWorldGrid
    wireWorldGrid = make2DArray(ledPanelWidth, ledPanelHeight)

def LoadJsonValues():
    jsonFile = os.path.dirname(os.path.realpath(__file__))+"/config.json"
    global Rpercentage
    global Gpercentage
    global Bpercentage
    global pixelCount
    global ledBrightness
    global ledPanelWidth
    global ledPanelHeight

    with open(jsonFile) as json_file:
        json_decoded = json.load(json_file)

    if not (json_decoded.get('redCalibration') is None):
        Rpercentage = int(json_decoded["redCalibration"])
    else:
        Rpercentage = 100
    if not (json_decoded.get('greenCalibration') is None):
        Gpercentage = int(json_decoded["greenCalibration"])
    else:
        Gpercentage = 100
    if not (json_decoded.get('blueCalibration') is None):
        Bpercentage = int(json_decoded["blueCalibration"])
    else:
        Bpercentage = 100
    if not (json_decoded.get('LedCount') is None):
        pixelCount = int(json_decoded.get('LedCount'))
    if not (json_decoded.get('brightnessValue') is None):
        ledBrightness = int(json_decoded["brightnessValue"])
    else:
        ledBrightness = 100
    if not (json_decoded.get('LEDPanelWidth') is None):
        ledPanelWidth = int(json_decoded["LEDPanelWidth"])
    if not (json_decoded.get('LEDPanelHeight') is None):
        ledPanelHeight = int(json_decoded["LEDPanelHeight"])

def start():
    if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/config.json') == 1):
        LoadJsonValues()
    NewPixelArray()
    CreateWireWorld2dArray()

start()

def Clear():
    pixels.fill((0, 0, 0))
    pixels.show()

def setColor(R, G, B):
    pixels.fill((R * (Rpercentage / 100)*(ledBrightness / 100), G * (Gpercentage / 100)*(ledBrightness / 100), B * (Bpercentage / 100)*(ledBrightness / 100)))
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
    print("updated speed to: " + str(speedValue))



def setPixel(x, y, color):
    global pixelArray
    pixelArray[int(x)][int(y)] = color
    pixel = int(getPixelNumber(x, y))
    pixels[pixel] = (int(color[1:3], 16) * (Rpercentage / 100)*(ledBrightness / 100), int(color[3:5], 16) * (Gpercentage / 100)*(ledBrightness / 100), int(color[5:7], 16) * (Bpercentage / 100)*(ledBrightness / 100))
    
    pixels.show()

# get pixel number with lookup table methode
# converts coordinates to the pixel number on the led panel
# this function is for an led panel with a zigzag pattern
# LedStrip:  
#   _________
#   _________|
#  |_________
#   _________|
#  |_________

#def getPixelNumber(corX, corY):
#    rowX = []
#    x = 16 #width
#    y = 16 #height
#    for i in range(x):
#        rowY = []
#        for ii in range(y):
#            if (i % 2) == 0: #check if number is even
#                rowY.append((i * y) + ii)
#            else:
#                rowY.insert(0, ((i * y) + ii))
#        rowX.append(rowY)
#    return rowX[int(corY)][int(corX)]¨

def getPixelNumber(corX, corY):
    global ledPanelWidth
    index = 0
    if (int(corY) % 2) == 0: #you can easely mirror the image by changing == to !=
        index = (int(corY) * ledPanelWidth) + (ledPanelWidth - int(corX)) - 1
    else:
        index = (int(corY) * ledPanelWidth) + int(corX)
    return index


def RedCalibration(percentage):
    global Rpercentage
    Rpercentage = percentage
def GreenCalibration(percentage):
    global Gpercentage
    Gpercentage = percentage
def BlueCalibration(percentage):
    global Bpercentage
    Bpercentage = percentage

def setLedCount(ledCount):
    global pixelCount
    pixelCount = ledCount

def setConfigPanelWidth(value):
    global ledPanelWidth
    ledPanelWidth = value
    NewPixelArray()

def setConfigPanelHeight(value):
    global ledPanelHeight
    ledPanelHeight = value
    NewPixelArray()

def CreateImage():
    global pixelArray
    global imageName
    global ledPanelWidth
    global ledPanelHeight
    if imageName != "":
        img = Image.new('RGB', [ledPanelWidth,ledPanelHeight], 255)
        data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                string = str(pixelArray[x][y])
                data[x,y] = (int(string[1:3], 16), int(string[3:5], 16), int(string[5:7], 16))

        img.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+imageName + '.png')

def SetImageName(value):
    global imageName
    imageName = value

def GetImageNames():
    imageNames = []
    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/savedImages"):
        if file.endswith(".png"):
            imageNames.append(file)
    print(imageNames)
    return(imageNames)


def DisplayImageFile(imageName):
    global ledPanelWidth
    global ledPanelHeight
    global Rpercentage
    global Gpercentage
    global Bpercentage
    pixelList = []
    image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/savedImages/"+imageName)
    if (image.width == ledPanelWidth and image.height == ledPanelHeight):
        rgb_im = image.convert('RGB')
        Clear()
        for y in range(ledPanelHeight):
            for x in range(ledPanelWidth):
                pixel = int(getPixelNumber(x, y))
                r, g, b = rgb_im.getpixel((x, y))  
                pixels[pixel] = (r * ((Rpercentage / 100)*(ledBrightness / 100)), g * (Gpercentage / 100)*(ledBrightness / 100), b * (Bpercentage / 100)*(ledBrightness / 100))
                data_set = {"X": x, "Y": y, "R": r, "G": g, "B": b}
                pixelList.append(json.dumps(data_set))
            pixels.show()
    return pixelList

def DownscaleImage(imagePath, newName):
    global ledPanelWidth
    global ledPanelHeight
    image = Image.open(imagePath)
    resized_image = image.resize((ledPanelWidth,ledPanelHeight))
    #resized_image.save('savedImages/'+'new'+ '.png')
    resized_image.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+newName)

url = ""

def UpdateUrl(value):
    global url
    url = str(value)

gifUrl = ""

def UpdategifUrl(value):
    global gifUrl
    gifUrl = str(value)

def DisplayUrl():
    global url
    if url != "":
        imageName = "tmp.png"
        path = os.path.dirname(os.path.realpath(__file__))+"/tmpImages/" + imageName
        try:
            urllib.request.urlretrieve(url, path)
        except:
            return []
        DownscaleImage(path, "tmp.png")
        return DisplayImageFile(imageName)

    print("no url entered")

def LoadUploadedFile():
    path = os.path.dirname(os.path.realpath(__file__))+"/uploads"
    imageName = "tmp.png"
    files = os.listdir(path)

    if (files == ""):
        return
    for f in files:
        if (f != ""):
            filePath = path+"/"+str(f)
            DownscaleImage(filePath, "tmp.png")
            os.remove(filePath)
    return DisplayImageFile(imageName)

def sendToClient(message):
    import Controller
    Controller.sendToClient(message)

def DisplayGIF():
    global ledPanelHeight
    global ledPanelWidth
    global gifUrl
    if gifUrl != "":
        imageName = "tmp.gif"
        path = os.path.dirname(os.path.realpath(__file__))+"/tmpImages/" + imageName
        try:
            urllib.request.urlretrieve(gifUrl, path)
        except:
            return ""
        resize_gif(path, None, (ledPanelWidth, ledPanelHeight))
        return path

def PlayGif():
    global ledPanelHeight
    global ledPanelWidth
    global Rpercentage
    global Gpercentage
    global Bpercentage
    gif = Image.open(os.path.dirname(os.path.realpath(__file__))+"/tmpImages/tmp.gif")
    
    while True:
        for i in range(gif.n_frames):
            gif.seek(i)
            rgb_im = gif.convert('RGB')
            for y in range(ledPanelHeight):
                for x in range(ledPanelWidth):
                    pixel = int(getPixelNumber(x, y))
                    r, g, b = rgb_im.getpixel((x, y))  
                    pixels[pixel] = (r * ((Rpercentage / 100)*(ledBrightness / 100)), g * (Gpercentage / 100)*(ledBrightness / 100), b * (Bpercentage / 100)*(ledBrightness / 100))
            pixels.show()
            time.sleep(0.2)

def resize_gif(path, save_as=None, resize_to=None):
    all_frames = extract_and_resize_frames(path, resize_to)

    if not save_as:
        save_as = path

    if len(all_frames) == 1:
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)

def extract_and_resize_frames(path, resize_to=None):
    global ledPanelHeight
    global ledPanelWidth
    im = Image.open(path)
    all_frames = []
    try:
        while True:
            im.convert('RGB')
            new_frame = im.resize((ledPanelWidth,ledPanelHeight))
            all_frames.append(new_frame)
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames

grid = []
cols = ledPanelWidth
rows = ledPanelHeight

def startGameOfLife():
    global grid
    global cols
    global rows

    listRow = [0] * rows
    listCol = []
    for i in range(cols): 
        for j in range(rows):
            listRow[j] = int(random.randint(0, 1))
        listCol.append(listRow)
        listRow = [0] * cols
    grid = listCol
    while True:
        draw()

def draw():
    global grid
    global cols
    global rows
    for i in range(cols):
        for j in range(rows):
            pixel = getPixelNumber(j, i)
            if (grid[i][j] == 1):
                pixels[pixel] = (0.5, 1, 0.5)
            else:
                pixels[pixel] = (0, 0, 0)
    pixels.show()
    time.sleep(0.1)
    listCol = []
    listRow = [0] * rows
    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            neighbors = countNeighbors(grid, i, j)
            if (state == 0 and neighbors == 3):
                listRow[j] = 1
            elif (state == 1 and (neighbors < 2 or neighbors > 3)):
                listRow[j] = 0
            else:
                listRow[j] = state
        listCol.append(listRow)
        listRow = [0] * cols
    grid = listCol

def countNeighbors(grid, x, y):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            sum += grid[col][row]
    sum -= grid[x][y];
    return sum;

antGrid = [];
x = 0;
y = 0;
dir = 0;
color = (0, 0, 0)

ANTUP = 0;
ANTRIGHT = 1;
ANTDOWN = 2;
ANTLEFT = 3;

def StartAnt():
    global antGrid, x, y, dir
    antGrid = make2DArray(ledPanelWidth, ledPanelHeight)
    x = int(ledPanelWidth / 2)
    y = int(ledPanelHeight / 2)
    dir = ANTUP
    while True:
        drawAnt()

def turnRight():
    global dir
    dir += 1
    if (dir > ANTLEFT):
        dir = ANTUP
  
def turnLeft():
    global dir
    dir -= 1
    if (dir < ANTUP):
        dir = ANTLEFT

def moveForward():
    global x, y, dir, color

    if (dir == ANTUP):
        color = (2, 0, 1.5)
        y -= 1 
    elif (dir == ANTRIGHT):
        color = (2, 1.5, 0)
        x += 1
    elif (dir == ANTDOWN):
        color = (2, 1.5, 1.5)
        y += 1
    elif (dir == ANTLEFT):
        color = (2, 0, 0)
        x -= 1

    if (x > ledPanelWidth - 1):
        x = 0
    elif (x < 0):
        x = ledPanelWidth - 1
    if (y > ledPanelHeight - 1):
        y = 0
    elif (y < 0) :
        y = ledPanelHeight - 1

def drawAnt():
    global x, y, dir, color

    for n in range(100):
        state = antGrid[x][y]
        if (state == 0):
            turnRight()
            antGrid[x][y] = 1
        elif (state == 1):
            turnLeft()
            antGrid[x][y] = 0
        if (antGrid[x][y] == 1):
            color = (0, 0, 0)

        pixel = getPixelNumber(x, y)
        pixels[pixel] = (color)

        moveForward()
        #time.sleep(0.05)
        pixels.show()

def startBriansBrain():
    global grid
    global cols
    global rows

    listRow = [0] * rows
    listCol = []
    for i in range(cols): 
        for j in range(rows):
            listRow[j] = int(random.randint(0, 2))
        listCol.append(listRow)
        listRow = [0] * cols
    grid = listCol
    while True:
        drawBriansBrain()

def drawBriansBrain():
    global grid
    global cols
    global rows
    for i in range(cols):
        for j in range(rows):
            pixel = getPixelNumber(j, i)
            if (grid[i][j] == 1):
                pixels[pixel] = (0, 1, 0)
            elif(grid[i][j] == 2):
                pixels[pixel] = (1, 0, 0)
            else:
                pixels[pixel] = (0, 0, 0)
    pixels.show()
    
    nextGrid = grid
    for i in range(cols):
        for j in range(rows):
            if (grid[i][j] == 2):
                nextGrid[i][j] = 1 #set the cell to dying state
            elif (grid[i][j] == 1):
                nextGrid[i][j] = 0
            elif (grid[i][j] == 0):
                neighbors = countNeighborsBriansBrain(grid, i, j)
                if (neighbors == 2):
                    nextGrid[i][j] = 2
    grid = nextGrid
    time.sleep(0.5)

def countNeighborsBriansBrain(grid, x, y):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            if (grid[col][row] == 2):
                sum += 1
    return sum;

def setWireWorldPixel(x, y, mode):
    global wireWorldGrid
    wireWorldGrid[x][y] = mode

def StartWireWorld():
    while True:
        RunWireWorld()

def RunWireWorld():
    global wireWorldGrid
    for j in range(cols):
        for i in range(rows):
            pixel = getPixelNumber(j, i)
            if (wireWorldGrid[j][i] == 0):
                pixels[pixel] = (0, 0, 0)
            elif (wireWorldGrid[j][i] == 1):
                pixels[pixel] = (1, 1, 0)
            elif (wireWorldGrid[j][i] == 2):
                pixels[pixel] = (0, 0, 1)
            elif (wireWorldGrid[j][i] == 3):
                pixels[pixel] = (1, 0, 0)
    nextgrid = make2DArray(cols, rows)
    pixels.show()
    time.sleep(0.5)
    
    for i in range(cols):
        for j in range(rows):
            if (wireWorldGrid[i][j] == 1):
                neighbors = countNeighborsWireWorld(wireWorldGrid, i, j)
                if (neighbors == 1 or neighbors == 2):
                    nextgrid[i][j] = 2
                else:
                    nextgrid[i][j] = 1
            elif (wireWorldGrid[i][j] == 2):
                nextgrid[i][j] = 3
            elif (wireWorldGrid[i][j] == 3):
                nextgrid[i][j] = 1
    wireWorldGrid = nextgrid

def countNeighborsWireWorld(wireWorldGrid, x, y):
    sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            if (wireWorldGrid[col][row] == 2):
                sum += 1
    return sum;

#all modes for LED-Panel and LED-Strip

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
            pixels[i] = (((rgb[0] * 255) * (Rpercentage / 100)*(ledBrightness / 100), (rgb[1] * 255) * (Gpercentage / 100)*(ledBrightness / 100), (rgb[2] * 255) * (Bpercentage / 100)*(ledBrightness / 100)))
            h += 0.0001
            time.sleep(0.001 / (rainbowSpeed / 100))
        pixels.show()
        if h == 1:
            h == 0

oneColorModeHex = "#ffffff"
oneColorModeName = ""

def sethexOneColorEffect(value):
    global oneColorModeHex
    oneColorModeHex = value

def selectOneColorMode(modeName):
    global oneColorModeName
    oneColorModeName = modeName

def startOneColorMode():
    if oneColorModeName == "SineWave":
        sinewave()
    elif oneColorModeName == "FireEffect":
        FireEffect()
    elif oneColorModeName == "StarsEffect":
        StarEffect()
    elif oneColorModeName == "KnightRider":
        knightRider()
    elif oneColorModeName == "DisplayText":
        DisplayText()
        

sineWaveFrequency = 1
sineWaveLength = 1

def setSineWaveFrequency(value):
    global sineWaveFrequency
    sineWaveFrequency = value

def setSineWaveLength(value):
    global sineWaveLength
    sineWaveLength = value / 100

def sinewave():
    global sineWaveLength
    global sineWaveFrequency

    startTime = time.time()
    while True:
        for i in range(pixelCount):
            result = math.sin(sineWaveFrequency*(time.time() - startTime)+(sineWaveLength * i))
            pixels[i] = (((((result + 1)/2) * int(oneColorModeHex[1:3], 16)) * (Rpercentage / 100)*(ledBrightness / 100), (((result + 1)/2) * int(oneColorModeHex[3:5], 16)) * (Gpercentage / 100)*(ledBrightness / 100), (((result + 1)/2) * int(oneColorModeHex[5:7], 16)) * (Bpercentage / 100)*(ledBrightness / 100)))
        pixels.show()
        #time.sleep(0.01)

def FireEffect():
    global oneColorModeHex
    pixelList = []
    for i in range(pixelCount):
        pixelList.append(int(random.randint(0, 255)))
    while True:
        for pixel in range(pixelCount):
            pixels[pixel] = ((int(oneColorModeHex[1:3], 16)*(pixelList[pixel] / 255) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (pixelList[pixel] / 255) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (pixelList[pixel] / 255) * (Bpercentage / 100)*(ledBrightness / 100)))
            if pixelList[pixel] <= 0:
                pixelList[pixel] = 255
            else:
                pixelList[pixel] -= 1 
        pixels.show()

class Star:
    value = 0
    declining = False
    position = 0

starsPerSecond = 1

def setStarsPerSecond(value):
    global starsPerSecond
    starsPerSecond = value

def StarEffect():
    global oneColorModeHex
    starList = []
    starsToRemove = []
    startTime = time.time()
    while True:
        if time.time() - startTime >= starsPerSecond / 100:
            newStar = Star()
            newStar.position = int(random.randint(0, pixelCount - 1))
            starList.append(newStar)
            startTime = time.time()

        for star in range(len(starList)):
            pixels[starList[star].position] = ((int(oneColorModeHex[1:3], 16)*(starList[star].value / 255) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (starList[star].value / 255) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (starList[star].value / 255) * (Bpercentage / 100)*(ledBrightness / 100)))
            
            if starList[star].declining == True:
                if starList[star].value == 0:
                    if star not in starsToRemove:
                        starsToRemove.append(star)
                else:
                    starList[star].value -= 1
            else:
                if starList[star].value == 255:
                    starList[star].declining = True
                else:
                    starList[star].value += 1

        for i in range(len(starsToRemove)):
            starList.pop(starsToRemove[i])
        starsToRemove = []

        pixels.show()

knightRiderFade = 100
knightRiderSpeed = 1

def setKnightRiderFade(value):
    global knightRiderFade
    knightRiderFade = value

def setKnightRiderSpeed(value):
    global knightRiderSpeed
    knightRiderSpeed = value

def knightRider():
    global knightRiderSpeed
    neighbors = []
    pixelStrength = 100
    while pixelStrength >= 15:
        strength = pixelStrength / (1 + (knightRiderFade * 0.001))
        if pixelStrength >= 15:
            neighbors.append(strength)
            pixelStrength = pixelStrength / (1 + (knightRiderFade * 0.001))
        else:
            break
    if len(neighbors) * 2 >= pixelCount:
        print("Please increse fade")
        return

    while True:
        for position in range(pixelCount):
            pixels[position] = ((int(oneColorModeHex[1:3], 16) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (Bpercentage / 100)*(ledBrightness / 100)))
            for neighborPixel in range(len(neighbors)):
                neighborFront = position + neighborPixel + 1
                if neighborFront <= 255:
                    pixels[neighborFront] = ((int(oneColorModeHex[1:3], 16) * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16)  * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                neighborRear = position - neighborPixel - 1
                if neighborRear >= 0:
                    
                    pixels[neighborRear] = ((int(oneColorModeHex[1:3], 16) * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16)  * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                pixels[neighborRear - len(neighbors)] = ((0, 0, 0))
            time.sleep(knightRiderSpeed * 0.001)
            pixels.show()

        for pixel in range(pixelCount - 1, 0, -1):
            pixels[pixel] = ((int(oneColorModeHex[1:3], 16) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (Bpercentage / 100)*(ledBrightness / 100)))
            #show neighbors
            for neighborPixel in range(len(neighbors)):
                neighborFront = pixel + neighborPixel + 1
                if neighborFront <= 255:
                    pixels[neighborFront] = ((int(oneColorModeHex[1:3], 16) * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                neighborRear = pixel - neighborPixel - 1
                if neighborRear >= 0:
                    
                    pixels[neighborRear] = ((int(oneColorModeHex[1:3], 16) * (neighbors[neighborPixel] / 100) * (Rpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[3:5], 16) * (neighbors[neighborPixel] / 100) * (Gpercentage / 100)*(ledBrightness / 100), int(oneColorModeHex[5:7], 16) * (neighbors[neighborPixel] / 100) * (Bpercentage / 100)*(ledBrightness / 100)))
                if (neighborFront + len(neighbors) <= pixelCount):
                    pixels[neighborFront + len(neighbors) - 1] = ((0, 0, 0))
            time.sleep(knightRiderSpeed * 0.001)     
            pixels.show()

textToDisplay = ""
textSpeed = 10

removeTopPixels = 0

def SetDisplayText(value):
    global textToDisplay
    textToDisplay = value

def DisplayText():
    global ledPanelWidth
    global ledPanelHeight
    global textToDisplay
    font = ImageFont.truetype('font/PixeloidSans.ttf', 9)
    print("length", font.getsize(textToDisplay))
    img = Image.new(mode="RGB", size=font.getsize(textToDisplay))
    
    draw = ImageDraw.Draw(im=img)

    draw.text(xy=(0, 0), text=textToDisplay, font=font, fill='#ffffff')
    while True:
        if img.width < ledPanelWidth:
            for width in range(min( img.width, ledPanelWidth)):
                for height in range(min(img.height - removeTopPixels, ledPanelHeight)):
                    r, g, b = img.getpixel((width, height + removeTopPixels))  
                    pixels[getPixelNumber(width, height)] = (r * ((Rpercentage / 100)*(ledBrightness / 100)), g * (Gpercentage / 100)*(ledBrightness / 100), b * (Bpercentage / 100)*(ledBrightness / 100))
            
            pixels.show()
            time.sleep(textSpeed / 100)
        else: #scroll function if thext doesnt fit in the led panel completely
            for widthPos in range(img.width - ledPanelWidth):
                for width in range(min( img.width, ledPanelWidth)):
                    for height in range(min(img.height - removeTopPixels, ledPanelHeight)):
                        r, g, b = img.getpixel((width + widthPos, height + removeTopPixels))  
                        pixels[getPixelNumber(width, height)] = (r * ((Rpercentage / 100)*(ledBrightness / 100)), g * (Gpercentage / 100)*(ledBrightness / 100), b * (Bpercentage / 100)*(ledBrightness / 100))
                
                pixels.show()
                time.sleep(textSpeed / 100)
        

#DisplayText()