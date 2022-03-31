from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import json
import multiprocessing
import os
import importlib
import sys
import re
import RPi.GPIO as GPIO
from jsonHelper import JsonHelper
from LedStrip import LedStrip

#LedEngine Scripts
from LedController import LedController
from LedPanel import LedPanel
from Rainbow import Rainbow
from Fire import Fire
from SineWave import SineWave
from Stars import Stars
from KnightRider import KnightRider
from DisplayText import DisplayText
from GameOfLife import GameOfLife
from LangtonsAnt import LangtonsAnt
from BriansBrain import BriansBrain
from WireWorld import WireWorld
from DrawingCanvas import DrawingCanvas
from SaveCanvas import SaveCanvas
from DisplayImage import DisplayImage
from DisplayGif import DisplayGif
from DisplayImageFile import DisplayImageFile


UDP_TX_IP = "127.0.0.1"
UDP_TX_PORT = 3000

UDP_RX_IP = "127.0.0.1"
UDP_RX_PORT = 3001

print("UDP target IP: %s" % UDP_TX_IP)
print("UDP target port: %s" % UDP_TX_PORT)

sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockRX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sockRX.bind((UDP_RX_IP, UDP_RX_PORT))

# set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT) 
GPIO.output(21,GPIO.HIGH)

modeProcs = []

def newclient():
    if GPIO.input(21):
        sockTX.sendto(bytes('{"LedStrip0":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          
def CheckInput():
    switcher = {
        "ExecuteFunction": ExecuteFunction,
        "SetValueFunction": SetValueFunction,
        "SetOneValueFunction": SetOneValueFunction,
        "StopProcesses": StopProcesses,
        "searchImages": searchImages,
        "DisplayImage": displayImage,
        "LoadUrl": LoadUrl,
        "RequestJSONdata": RequestJSONdata,
        "LoadUploadedFile": LoadUploadedFile
    }
    while True:
        data, addr = sockRX.recvfrom(2048) # buffer size is 2048 bytes
        JsonStr = data.decode('utf_8')
        if JsonStr:
            sockTX.sendto(bytes(JsonStr, "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
            aDict = json.loads(JsonStr)
        if (JsonStr.find('{"NewClient":1}') != -1):
            newclient()
        key = next(iter(aDict))
        print(JsonStr, key)
        func = switcher.get(key, doNothing)
        func(aDict, addr)
    
def doNothing(aDict, addr):
    print(next(iter(aDict)), "does not exist in switcher")

def ExecuteFunction(aDict, addr):
    string = aDict["ExecuteFunction"].split(".", 1)
    objectClass = getattr(sys.modules[string[0]], string[0])
    objectClass()
    method = getattr(objectClass, string[1])
    method()
    
def SetValueFunction(aDict, addr):
    string = aDict["SetValueFunction"].split(".", 1)
    method = getattr(getattr(sys.modules[string[0]], string[0]) , string[1])
    method(aDict["args"])
    
def SetOneValueFunction(aDict, addr):
    string = aDict["SetOneValueFunction"].split(".",1)
    method = getattr(getattr(sys.modules[string[0]], string[0]) , string[1])
    method(aDict["value"])
    
def StopProcesses(aDict, addr):
    terminateProcesses()
    LedController.Clear()
    
def searchImages(aDict, addr):
    data = SaveCanvas.GetImageNames()
    for i in range(len(data)):
        string = '{"LoadableImageName":"'+data[i]+'"}'
        sockRX.sendto( string.encode('utf-8'), addr)
        
def displayImage(aDict, addr):
    pixelsToSend = []
    pixelsToSend = DisplayImage.DisplayImageFile(aDict["DisplayImage"])
    for i in range(len(pixelsToSend)):
        sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        
def LoadUrl(aDict, addr):
    pixelsToSend = []
    pixelsToSend = DisplayImage.DisplayUrl()
    if pixelsToSend:
        for i in range(len(pixelsToSend)):
            sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
            
def RequestJSONdata(aDict, addr):
    data = JsonHelper.GetDecodedJSON()
    string = json.dumps({'JSONdata':[data]})
    sockRX.sendto( string.encode('utf-8'), addr)
    
def LoadUploadedFile(aDict, addr):
    pixelsToSend = []
    pixelsToSend = DisplayImageFile.LoadUploadedFile()
    for i in range(len(pixelsToSend)):
        sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        
def terminateProcesses():
    for proc in modeProcs:
        #proc.join(timeout=0)
        if proc.is_alive():
            proc.terminate()

def CheckJSON(): #this function creates an empty JSON file if one doesnt exist
    if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/config.json') != 1):
        JSONconfig = open(os.path.exists(os.path.dirname(os.path.realpath(__file__))+'config.json'), "w")
        JSONconfig.WriteToJsonFile("key", "value")
        JSONconfig.close()
    else: #Load all values that where set previously by the user
        JsonHelper.LoadJsonValues()        

def CheckDirectories():
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/savedImages'):
        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/savedImages')
        print("Made directory savedImages")
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/tmpImages'):
        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/tmpImages')
        print("Made directory tmpImages")
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/uploads'):
        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/uploads')
        print("Made directory uploads")

#start
if __name__ == "__main__":
    from StaticColor import StaticColor
    from LedPanel import LedPanel
    CheckDirectories()
    newclient()
    CheckJSON()
    LedPanel()
    staticColor = StaticColor()
    staticColor.setColor("#000000")
    mainProcess = Thread(target = CheckInput)
    mainProcess.start()

while True:
    sleep(1)



               