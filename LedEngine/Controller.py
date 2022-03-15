from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
import json
import multiprocessing
import os
from jsonHelper import JsonHelper
from LedStrip import LedStrip

#LedEngine Scripts
import LedController as Ledstrip

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
ModeToPlay = ""

def newclient():
    if GPIO.input(21):
        sockTX.sendto(bytes('{"LedStrip0":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          
def CheckInput():
    global ModeToPlay
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

    while True:
        data, addr = sockRX.recvfrom(2048) # buffer size is 2048 bytes
        JsonStr = data.decode('utf_8')
        if JsonStr:
            sockTX.sendto(bytes(JsonStr, "utf-8"), (UDP_TX_IP, UDP_TX_PORT)) 
            aDict = json.loads(JsonStr)
        if (JsonStr.find('{"NewClient":1}') != -1):
            newclient()
        elif ("rainbowButton" in aDict):
            terminateProcesses()
            rainbow = Rainbow()
            rainbowProcecss = multiprocessing.Process(target=rainbow.Play, args=()) #multiprocessing so we can stop the process
            modeProcs.append(rainbowProcecss)
            rainbowProcecss.start()
        elif ("stopButton" in aDict):
            rainbowProcecss.terminate()
            LedController.Clear()
        elif ("setPixel" in aDict):
            #gets all values after ":"
            x = aDict["setPixel"].get("X")
            y = aDict["setPixel"].get("Y")
            hexString = aDict["setPixel"].get("color")
            drawingCanvas = DrawingCanvas()
            drawingCanvas.setPixel(x, y, hexString)
        elif ("ClearPixels" in aDict):
            Ledstrip.Clear()
        elif ("RedCalibration" in aDict):
            Ledstrip.RedCalibration(int(aDict["RedCalibration"]))
            JsonHelper.WriteToJsonFile("redCalibration", str(aDict["RedCalibration"]))
        elif ("GreenCalibration" in aDict):
            Ledstrip.GreenCalibration(int(aDict["GreenCalibration"]))
            JsonHelper.WriteToJsonFile("greenCalibration", str(aDict["GreenCalibration"]))
        elif ("BlueCalibration" in aDict):
            Ledstrip.BlueCalibration(int(aDict["BlueCalibration"]))
            JsonHelper.WriteToJsonFile("blueCalibration", str(aDict["BlueCalibration"]))
        elif ("LedCount" in aDict):
            Ledstrip.BlueCalibration(int(aDict["LedCount"]))
            JsonHelper.WriteToJsonFile("LedCount", str(aDict["LedCount"]))
        elif ("MakePicture" in aDict):
            Ledstrip.CreateImage()
        elif ("ImageName" in aDict):
            Ledstrip.SetImageName(aDict["ImageName"])
        elif ("searchImages" in aDict):
            data = Ledstrip.GetImageNames()
            for i in range(len(data)):
                string = '{"LoadableImageName":"'+data[i]+'"}'
                sockRX.sendto( string.encode('utf-8'), addr)
        elif ("DisplayImage" in aDict):
            Ledstrip.DisplayImageFile(aDict["DisplayImage"])
        elif ("LoadUrl" in aDict):
            pixelsToSend = []
            pixelsToSend = Ledstrip.DisplayUrl()
            if pixelsToSend:
                for i in range(len(pixelsToSend)):
                    sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        elif ("Url" in aDict):
            Ledstrip.UpdateUrl(aDict["Url"])
        elif ("LoadgifUrl" in aDict):
            path = Ledstrip.ConvertGif()
            gifProcess = multiprocessing.Process(target=Ledstrip.PlayGif, args=()) #multiprocessing so we can stop the process
            modeProcs.append(gifProcess)
            gifProcess.start()
        elif ("gifUrl" in aDict):
            Ledstrip.UpdategifUrl(aDict["gifUrl"])
        elif ("StopgifUrl" in aDict):
            gifProcess.terminate()
        elif ("setConfigPanelWidth" in aDict):
            Ledstrip.setConfigPanelWidth(int(aDict["setConfigPanelWidth"]))
            JsonHelper.WriteToJsonFile("LEDPanelWidth", str(aDict["setConfigPanelWidth"]))
        elif ("setConfigPanelHeight" in aDict):
            Ledstrip.setConfigPanelHeight(int(aDict["setConfigPanelHeight"]))
            JsonHelper.WriteToJsonFile("LEDPanelHeight", str(aDict["setConfigPanelHeight"]))
        elif ("RequestJSONdata" in aDict):
            data = JsonHelper.GetDecodedJSON()
            string = json.dumps({'JSONdata':[data]})
            sockRX.sendto( string.encode('utf-8'), addr)
        elif ("LoadUploadedFile" in aDict):
            pixelsToSend = []
            pixelsToSend = Ledstrip.LoadUploadedFile()
            for i in range(len(pixelsToSend)):
                sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        elif ("startGameOfLife" in aDict):
            terminateProcesses()
            if (aDict["startGameOfLife"] == 1):
                terminateProcesses()
                gameOfLife = GameOfLife()
                gameOfLifeProcess = multiprocessing.Process(target=gameOfLife.Start, args=())
                modeProcs.append(gameOfLifeProcess)
                gameOfLifeProcess.start()
        elif ("stopGameOfLife" in aDict):
            if (aDict["stopGameOfLife"] == 1):
                gameOfLifeProcess.terminate()
                LedController.Clear()
        elif ("startAnt" in aDict):
            if (aDict["startAnt"] == 1):
                terminateProcesses()
                langtonsAnt = LangtonsAnt()
                antProcess = multiprocessing.Process(target=langtonsAnt.Start, args=())
                modeProcs.append(antProcess)
                antProcess.start()
        elif ("stopAnt" in aDict):
                antProcess.terminate()
                LedController.Clear()
        elif ("startBriansBrain" in aDict):
            if (aDict["startBriansBrain"] == 1):
                terminateProcesses()
                briansBrain = BriansBrain()
                briansBrainProcess = multiprocessing.Process(target=briansBrain.Start, args=())
                modeProcs.append(briansBrainProcess)
                briansBrainProcess.start()
        elif ("stopBriansBrain" in aDict):
                briansBrainProcess.terminate()
                LedController.Clear()
        elif ("setPixelWireWorld" in aDict):
            #gets all values after ":"
            x = aDict["setPixelWireWorld"].get("X")
            y = aDict["setPixelWireWorld"].get("Y")
            mode = aDict["setPixelWireWorld"].get("mode")
            WireWorld.setWireWorldPixel(x, y, mode)
        elif ("startWireWorld" in aDict):
            if (aDict["startWireWorld"] == 1):
                terminateProcesses()
                wireWorld = WireWorld()
                wireWorldProcess = multiprocessing.Process(target=wireWorld.Start, args=())
                modeProcs.append(wireWorldProcess)
                wireWorldProcess.start()
        elif ("stopWireWorld" in aDict):
            wireWorldProcess.terminate()
        elif ("SineWave" in aDict):
            ModeToPlay = "SineWave"
        elif ("FireEffect" in aDict):
            ModeToPlay = "FireEffect"
        elif ("StarsEffect" in aDict):
            ModeToPlay = "StarsEffect"
        elif ("KnightRider" in aDict):
            ModeToPlay = "KnightRider"
        elif ("DisplayText" in aDict):
            ModeToPlay = "DisplayText"
        elif ("StartOneColorMode" in aDict):
            terminateProcesses()
            OneColorProcess = None
            if (ModeToPlay == "SineWave"):
                sineWave = SineWave()
                OneColorProcess = multiprocessing.Process(target=sineWave.Start, args=())
            elif (ModeToPlay == "FireEffect"):
                fire = Fire()
                OneColorProcess = multiprocessing.Process(target=fire.Start, args=())
            elif (ModeToPlay == "StarsEffect"):
                starsEffect = Stars()
                OneColorProcess = multiprocessing.Process(target=starsEffect.Start, args=())
            elif (ModeToPlay == "KnightRider"):
                knightRider = KnightRider()
                OneColorProcess = multiprocessing.Process(target=knightRider.Start, args=())
            elif (ModeToPlay == "DisplayText"):
                displayText = DisplayText()
                OneColorProcess = multiprocessing.Process(target=displayText.Start, args=())
            if OneColorProcess != None:
                OneColorProcess.start()
        elif ("StopOneColorMode" in aDict):
            OneColorProcess.terminate()
        elif ("valuePanelChanged" in aDict):
            Ledstrip.setPanelArray(int(aDict["valuePanelChanged"].get("x")), int(aDict["valuePanelChanged"].get("y")), int(aDict["valuePanelChanged"].get("value")))
        elif ("valueChanged" in aDict):
            objectID = aDict["valueChanged"].get("objectID")
            objectValue = aDict["valueChanged"].get("objectValue")
            if (objectID == "effecthexChanged"):
                string = str(objectValue).lstrip("#")
                LedController.sethexOneColorEffect((int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16)))
            elif (objectID == "SpeedInput"): #rainbow mode
                Rainbow.SetSpeedValue(int(objectValue))
            elif (objectID == "WaveLengthInput"): #rainbow mode
                Rainbow.SetwaveLength(int(objectValue))
            elif (objectID == "HEX"):
                string = str(objectValue).lstrip("#")
                staticColor = StaticColor()
                staticColor.setColor(int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16)) #simple way to convert hex to rgb
            elif (objectID == "A1"):
                LedController.SetBrightness(int(objectValue))
                JsonHelper.WriteToJsonFile("brightnessValue", objectValue)
            elif (objectID == "sineWaveFrequency"):
                SineWave.setSineWaveFrequency(int(objectValue))
            elif (objectID == "sineWaveLength"):
                SineWave.setSineWaveLength(int(objectValue))
            elif (objectID == "starsPerSecond"):
                Stars.setStarsPerSecond(int(objectValue))
            elif (objectID == "knightRiderFade"):
                Ledstrip.setKnightRiderFade(int(objectValue))
            elif (objectID == "knightRiderSpeed"):
                Ledstrip.setKnightRiderSpeed(int(objectValue))
            elif (objectID == "displayTextText"):
                DisplayText.SetDisplayText(str(objectValue))
            elif (objectID == "textSpeed"):
                DisplayText.SetTextSpeed(int(objectValue))
            elif (objectID == "removeTopPixels"):
                DisplayText.SetRemoveTopPixels(int(objectValue))
            elif (objectID == "textFontSize"):
                DisplayText.SetTextFontSize(int(objectValue))
            elif (objectID == "amountOfPanelsInWidth"):
                LedPanel.SetAmountOfPanelsInWidth(int(objectValue))
                JsonHelper.WriteToJsonFile("amountOfPanelsInWidth", str(objectValue))
            elif (objectID == "amountOfPanelsInHeight"):
                LedPanel.SetAmountOfPanelsInHeight(int(objectValue))
                JsonHelper.WriteToJsonFile("amountOfPanelsInHeight", str(objectValue))
        
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
    CheckDirectories()
    newclient()
    CheckJSON()
    staticColor = StaticColor()
    staticColor.setColor(0, 0, 0)
    mainProcess = Thread(target = CheckInput)
    mainProcess.start()

while True:
    sleep(1)



               