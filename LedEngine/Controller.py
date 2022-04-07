from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import json
import os
import sys
import RPi.GPIO as GPIO
import multiprocessing
from jsonHelper import JsonHelper
from LedStrip import LedStrip
from LedController import LedController
from LedPanel import LedPanel
from SaveCanvas import SaveCanvas

#LedEngine Scripts
sys.path.append(os. getcwd() + '/modes/')

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
from DisplayImage import DisplayImage
from DisplayGif import DisplayGif
from DisplayImageFile import DisplayImageFile
from StaticColor import StaticColor

LedPanel()
LedController()
LedStrip()

rainbow = Rainbow()
fire = Fire()
sine_wave = SineWave()
stars = Stars()
knight_rider = KnightRider()
display_text = DisplayText()
game_of_life = GameOfLife()
langtons_ant = LangtonsAnt()
brians_brain = BriansBrain()
wire_world = WireWorld()
drawing_canvas = DrawingCanvas()
display_image = DisplayImage()
display_gif = DisplayGif()
display_image_file = DisplayImageFile()
static_color = StaticColor()

get_instantiated_class = {
    "Rainbow": rainbow,
    "Fire": fire,
    "SineWave": sine_wave,
    "Stars": stars,
    "KnightRider": knight_rider,
    "DisplayText": display_text,
    "GameOfLife": game_of_life,
    "LangtonsAnt": langtons_ant,
    "BriansBrain": brians_brain,
    "WireWorld": wire_world,
    "DrawingCanvas": drawing_canvas,
    "DisplayImage": display_image,
    "DisplayGif": display_gif,
    "DisplayImageFile": display_image_file,
    "StaticColor": static_color
}



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
    instantiated_class = get_instantiated_class.get(string[0], doNothing)
    func = getattr(instantiated_class, string[1])
    process = multiprocessing.Process(target=func, args=()) #multiprocessing so we can stop the process
    modeProcs.append(process)
    process.start()
    
def SetValueFunction(aDict, addr):
    string = aDict["SetValueFunction"].split(".", 1)
    instantiated_class = get_instantiated_class.get(string[0], doNothing)
    func = getattr(instantiated_class, string[1])
    func(aDict["args"])
    
def SetOneValueFunction(aDict, addr):
    string = aDict["SetOneValueFunction"].split(".", 1)
    instantiated_class = get_instantiated_class.get(string[0], doNothing)
    func = getattr(instantiated_class, string[1])
    func(aDict["value"])
    
def StopProcesses(aDict, addr):
    terminateProcesses()
    controller = LedController()
    controller.Clear()
    
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
    
    CheckDirectories()
    newclient()
    CheckJSON()
    
    static_color.setColor("#000000")
    mainProcess = Thread(target = CheckInput)
    mainProcess.start()

while True:
    sleep(1)
