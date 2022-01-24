import board
import neopixel
import time
import colorsys
from PIL import Image
import os
import requests
from io import BytesIO
import urllib.request
import json


pixelCount = 320
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

imageName = ""

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

def setPixel(x, y, color):
    global pixelArray
    pixelArray[int(x)][int(y)] = color
    pixel = int(getPixelNumber(x, y))
    pixels[pixel] = (int(color[:2], 16) * (Rpercentage / 100)*(ledBrightness / 100), int(color[2:4], 16) * (Gpercentage / 100)*(ledBrightness / 100), int(color[4:6], 16) * (Bpercentage / 100)*(ledBrightness / 100))  
    print("R:" + str(int(color[:2], 16) * (Rpercentage / 100)*(ledBrightness / 100)))
    print("G:" + str(int(color[2:4], 16) * (Gpercentage / 100)*(ledBrightness / 100)))
    print("B:" + str(int(color[4:6], 16) * (Bpercentage / 100)*(ledBrightness / 100)))
    
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


def NewPixelArray():
    global pixelArray
    global ledPanelWidth
    global ledPanelHeight
    for i in range(ledPanelWidth):
        rowY = []
        for ii in range(ledPanelHeight):
            rowY.append('#000000')
        pixelArray.append(rowY)


def CreateImage():
    global pixelArray
    global imageName
    global ledPanelWidth
    global ledPanelHeight
    img = Image.new('RGB', [ledPanelWidth,ledPanelHeight], 255)
    data = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
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


def DisplayImageFile(imageName):
    global ledPanelWidth
    global ledPanelHeight
    global Rpercentage
    global Gpercentage
    global Bpercentage
    print(Rpercentage, Gpercentage, Bpercentage)
    pixelList = []
    image = Image.open("savedImages/"+imageName)
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
    resized_image.save('savedImages/'+newName)

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
        path = "tmpImages/" + imageName
        urllib.request.urlretrieve(url, path)
        DownscaleImage(path, "tmp.png")
        return DisplayImageFile(imageName)

    print("no url entered")

def sendToClient(message):
    import Controller
    Controller.sendToClient(message)

def DisplayGIF():
    global gifUrl
    if gifUrl != "":
        imageName = "tmp.gif"
        path = "tmpImages/" + imageName
        urllib.request.urlretrieve(gifUrl, path)
        resize_gif(path, None, (16, 16))
        return path

def PlayGif():
    global Rpercentage
    global Gpercentage
    global Bpercentage
    gif = Image.open("tmpImages/tmp.gif")
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
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


def analyseImage(path):
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames

def LoadJsonValues():
    jsonFile = "config.json"
    global Rpercentage
    global Gpercentage
    global Bpercentage
    global ledBrightness
    global ledPanelWidth
    global ledPanelHeight
    with open(jsonFile) as json_file:
        json_decoded = json.load(json_file)

    if(json_decoded["redCalibration"]):
        Rpercentage = int(json_decoded["redCalibration"])
    else:
        Rpercentage = 100
    if(json_decoded["greenCalibration"]):
        Gpercentage = int(json_decoded["greenCalibration"])
    else:
        Gpercentage = 100
    if(json_decoded["blueCalibration"]):
        Bpercentage = int(json_decoded["blueCalibration"])
    else:
        Bpercentage = 100
    if(json_decoded["brightnessValue"]):
        ledBrightness = int(json_decoded["brightnessValue"])
    else:
        ledBrightness = 100
    if(json_decoded["LEDPanelWidth"]):
        ledPanelWidth = int(json_decoded["LEDPanelWidth"])
    if(json_decoded["LEDPanelHeight"]):
        ledPanelHeight = int(json_decoded["LEDPanelHeight"])

    NewPixelArray()
    print("json values loaded")