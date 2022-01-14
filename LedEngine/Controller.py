from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
import json
import multiprocessing
import re

#LedEngine Scripts
import LedstripController as Ledstrip

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
        elif (JsonStr.find('{"rainbowButton":0}') != -1):
            rainbow = multiprocessing.Process(target=Ledstrip.rainbow_cycle, args=()) #multiprocessing so we can stop the process
            rainbow.start()
        elif (JsonStr.find('{"stopButton":0}') != -1):
            rainbow.terminate()
            Ledstrip.Clear()
        elif ("A1" in aDict):
            if (aDict["A1"] != "0"):
                brightnessValue = int(aDict["A1"])
                Ledstrip.SetBrightness(brightnessValue)
        elif ("WaveLengthInput" in aDict):
            if (aDict["WaveLengthInput"] != "0" and aDict["WaveLengthInput"]):
                waveLengthValue = int(aDict["WaveLengthInput"])
                Ledstrip.SetwaveLength(waveLengthValue)
        elif ("SpeedInput" in aDict):
            if (aDict["SpeedInput"] != "0"):
                speedValue = int(aDict["SpeedInput"])
                Ledstrip.SetSpeedValue(speedValue)
        elif ("a" in aDict):
            #gets all values after ":"
            xy = re.findall(r'%s(\d+)' % ":", aDict) 
            x = xy[0]
            y = xy[1]
            #hexcode has letters so the above methode doesnt work
            #here we get every character after #
            hexString = (aDict.partition("#")[2]) 
            color = hexString[:6]
            Ledstrip.setPixel(x, y, color)
        elif ("ClearPixels" in aDict):
            Ledstrip.Clear()
        elif ("RedCalibration" in aDict):
            Ledstrip.RedCalibration(int(aDict["RedCalibration"]))
        elif ("GreenCalibration" in aDict):
            Ledstrip.GreenCalibration(int(aDict["GreenCalibration"]))
        elif ("BlueCalibration" in aDict):
            Ledstrip.BlueCalibration(int(aDict["BlueCalibration"]))
        elif ("MakePicture" in aDict):
            Ledstrip.CreateImage()
        elif ("ImageName" in aDict):
            Ledstrip.SetImageName(aDict["ImageName"])
        elif ("searchImages" in aDict):
            data = Ledstrip.GetImageNames()
            for i in range(len(data)):
                string = '{"ImageName":"'+data[i]+'"}'
                sockRX.sendto( string.encode('utf-8'), addr)
        elif ("DisplayImage" in aDict):
            Ledstrip.DisplayImageFile(aDict["DisplayImage"])
        elif ("LoadUrl" in aDict):
            pixelsToSend = []
            pixelsToSend = Ledstrip.DisplayUrl()
            try:
                print("Not supported image format or URL")
                for i in range(len(pixelsToSend)):
                    sockRX.sendto( pixelsToSend[i].encode('utf-8'), addr)
            except:
                print("Not supported image format or URL")
        elif ("Url" in aDict):
            Ledstrip.UpdateUrl(aDict["Url"])
            

if __name__ == "__main__":
    newclient()
    #p1 = Thread(target = UpdateClient)
    p2 = Thread(target = CheckInput)
    #p1.start()
    p2.start()

while True:
    sleep(10)



               