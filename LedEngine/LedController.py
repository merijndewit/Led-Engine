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

class LedController:
    Rpercentage = 100
    Gpercentage = 100
    Bpercentage = 100
    ledBrightness = 100

    oneColorModeHex = (50, 0, 0)

    def sethexOneColorEffect(value):
        LedController.oneColorModeHex = value

    pixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)
    
    def SetPixelAmount(amount):
        LedController.pixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)

    def Clear():
        LedController.pixels.fill((0, 0, 0))
        LedController.pixels.show()

    def SetBrightness(brightnessValue):
        LedController.ledBrightness
        LedController.ledBrightness = brightnessValue

    def RedCalibration(percentage):
        LedController.Rpercentage = percentage
    def GreenCalibration(percentage):
        LedController.Gpercentage = percentage
    def BlueCalibration(percentage):
        LedController.Bpercentage = percentage

    def sendToClient(message):
        import Controller
        Controller.sendToClient(message)




#rainbow variables




pixelArray = []
wireWorldGrid = [] # 0 = off/nothing, 1 = conductor, 2 = Electron Head, 3 = ElectronTail 


imageName = ""

def start():
    pass

    #this is a test grid
    #panels2DArray[0][0] = 0
    #panels2DArray[0][1] = 1
    #panels2DArray[1][0] = 2
    #panels2DArray[1][1] = 3

    #NewPixelArray()
    #CreateWireWorld2dArray()

#all modes for LED-Panel and LED-Strip



#oneColorModeHex = "#ffffff"
#oneColorModeName = ""
#
#def sethexOneColorEffect(value):
#    global oneColorModeHex
#    oneColorModeHex = value
#
#def selectOneColorMode(modeName):
#    global oneColorModeName
#    oneColorModeName = modeName
#
#def startOneColorMode():
#    if oneColorModeName == "SineWave":
#        sinewave()
#    elif oneColorModeName == "FireEffect":
#        FireEffect()
#    elif oneColorModeName == "StarsEffect":
#        StarEffect()
#    elif oneColorModeName == "KnightRider":
#        knightRider()
#    elif oneColorModeName == "DisplayText":
#        DisplayText()
        