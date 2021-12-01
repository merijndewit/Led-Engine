from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
import json
import multiprocessing

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

brightnessValue = 0

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
        elif ("brightness" in aDict):
            print()
            Ledstrip.SetBrightness(float(aDict["brightness"])/100)
        elif ("A1" in aDict):
            brightnessValue = int(aDict["A1"])
            UpdateBrightness(brightnessValue)

def UpdateBrightness(value):
    sockTX.sendto(bytes('{"A1":' + str(value) + '}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))

            
#def UpdateClient():
#     while True:
#          sockTX.sendto(bytes('{"A1":' + str(brightnessValue) + '}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
#          sleep(3)


newclient()
#p1 = Thread(target = UpdateClient)
p2 = Thread(target = CheckInput)
#p1.start()
p2.start()

while True:
    sleep(10)



               