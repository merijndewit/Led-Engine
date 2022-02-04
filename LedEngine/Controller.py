from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
import json
import multiprocessing
import re
import os

#LedEngine Scripts
import LedstripController as Ledstrip
import jsonHelper

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

def newclient():
    if GPIO.input(21):
        sockTX.sendto(bytes('{"LedStrip0":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          
def CheckInput():
    Ledstrip.setColor(0, 0, 0)
    while True:
        data, addr = sockRX.recvfrom(2048) # buffer size is 2048 bytes
        JsonStr = data.decode('utf_8')
        key = "HEX"
        if JsonStr:
            sockTX.sendto(bytes(JsonStr, "utf-8"), (UDP_TX_IP, UDP_TX_PORT)) 
            aDict = json.loads(JsonStr)
        if (JsonStr.find('{"NewClient":1}') != -1):
            newclient()
        elif (key in aDict):
            string = str(aDict[key]).lstrip("#")
            Ledstrip.setColor(int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16)) #simple way to convert hex to rgb
        elif ("rainbowButton" in aDict):
            rainbow = multiprocessing.Process(target=Ledstrip.rainbow_cycle, args=()) #multiprocessing so we can stop the process
            rainbow.start()
        elif ("stopButton" in aDict):
            rainbow.terminate()
            Ledstrip.Clear()
        elif ("A1" in aDict):
            if (aDict["A1"] != "0"):
                Ledstrip.SetBrightness(int(aDict["A1"]))
                jsonHelper.WriteToJsonFile("brightnessValue", str(aDict["A1"]))
        elif ("WaveLengthInput" in aDict):
            if (aDict["WaveLengthInput"] != "0" and aDict["WaveLengthInput"]):
                waveLengthValue = int(aDict["WaveLengthInput"])
                Ledstrip.SetwaveLength(waveLengthValue)
        elif ("SpeedInput" in aDict):
            if (aDict["SpeedInput"] != "0"):
                speedValue = int(aDict["SpeedInput"])
                Ledstrip.SetSpeedValue(speedValue)
        elif ("setPixel" in aDict):
            #gets all values after ":"
            x = aDict["setPixel"].get("X")
            y = aDict["setPixel"].get("Y")
            hexString = aDict["setPixel"].get("color")
            Ledstrip.setPixel(x, y, hexString)
        elif ("ClearPixels" in aDict):
            Ledstrip.Clear()
        elif ("RedCalibration" in aDict):
            Ledstrip.RedCalibration(int(aDict["RedCalibration"]))
            jsonHelper.WriteToJsonFile("redCalibration", str(aDict["RedCalibration"]))
        elif ("GreenCalibration" in aDict):
            Ledstrip.GreenCalibration(int(aDict["GreenCalibration"]))
            jsonHelper.WriteToJsonFile("greenCalibration", str(aDict["GreenCalibration"]))
        elif ("BlueCalibration" in aDict):
            Ledstrip.BlueCalibration(int(aDict["BlueCalibration"]))
            jsonHelper.WriteToJsonFile("blueCalibration", str(aDict["BlueCalibration"]))
        elif ("LedCount" in aDict):
            Ledstrip.BlueCalibration(int(aDict["LedCount"]))
            jsonHelper.WriteToJsonFile("LedCount", str(aDict["LedCount"]))
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
            for i in range(len(pixelsToSend)):
                sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        elif ("Url" in aDict):
            Ledstrip.UpdateUrl(aDict["Url"])
        elif ("LoadgifUrl" in aDict):
            path = Ledstrip.DisplayGIF()
            gifProcess = multiprocessing.Process(target=Ledstrip.PlayGif, args=()) #multiprocessing so we can stop the process
            gifProcess.start()
        elif ("gifUrl" in aDict):
            Ledstrip.UpdategifUrl(aDict["gifUrl"])
        elif ("StopgifUrl" in aDict):
            gifProcess.terminate()
        elif ("setConfigPanelWidth" in aDict):
            jsonHelper.WriteToJsonFile("LEDPanelWidth", str(aDict["setConfigPanelWidth"]))
        elif ("setConfigPanelHeight" in aDict):
            jsonHelper.WriteToJsonFile("LEDPanelHeight", str(aDict["setConfigPanelHeight"]))
        elif ("RequestJSONdata" in aDict):
            data = jsonHelper.GetDecodedJSON()
            string = json.dumps({'JSONdata':[data]})
            sockRX.sendto( string.encode('utf-8'), addr)
        elif ("LoadUploadedFile" in aDict):
            pixelsToSend = []
            pixelsToSend = Ledstrip.LoadUploadedFile()
            for i in range(len(pixelsToSend)):
                sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
        elif ("startGameOfLife" in aDict):
            if (aDict["startGameOfLife"] == 1):
                gameOfLifeProcess = multiprocessing.Process(target=Ledstrip.startGameOfLife, args=())
                gameOfLifeProcess.start()
        elif ("stopGameOfLife" in aDict):
            if (aDict["stopGameOfLife"] == 1):
                gameOfLifeProcess.terminate()
                Ledstrip.Clear()
        elif ("startAnt" in aDict):
            if (aDict["startAnt"] == 1):
                antProcess = multiprocessing.Process(target=Ledstrip.StartAnt, args=())
                antProcess.start()
        elif ("stopAnt" in aDict):
            antProcess.terminate()
        elif ("startBriansBrain" in aDict):
            if (aDict["startBriansBrain"] == 1):
                BrainProcess = multiprocessing.Process(target=Ledstrip.startBriansBrain, args=())
                BrainProcess.start()
        elif ("stopBriansBrain" in aDict):
            BrainProcess.terminate()
        elif ("setPixelWireWorld" in aDict):
            #gets all values after ":"
            x = aDict["setPixelWireWorld"].get("X")
            y = aDict["setPixelWireWorld"].get("Y")
            mode = aDict["setPixelWireWorld"].get("mode")
            print("setPixel", x, y, mode)
            Ledstrip.setWireWorldPixel(x, y, mode)
        elif ("startWireWorld" in aDict):
            if (aDict["startWireWorld"] == 1):
                WireWorldProcess = multiprocessing.Process(target=Ledstrip.StartWireWorld, args=())
                WireWorldProcess.start()
        elif ("stopWireWorld" in aDict):
            WireWorldProcess.terminate()

        

def CheckJSON(): #this function creates an empty JSON file if one doesnt exist
    if(os.path.exists('./config.json')):
        JSONconfig = open("config.json", "x")
        jsonHelper.WriteToJsonFile("key", "value")
        JSONconfig.close()
    else: #Load all values that where set previously by the user
        Ledstrip.LoadJsonValues()

#start
if __name__ == "__main__":
    newclient()
    CheckJSON()
    mainProcess = Thread(target = CheckInput)
    mainProcess.start()

while True:
    sleep(1)



               