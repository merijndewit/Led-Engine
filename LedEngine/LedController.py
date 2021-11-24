from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO
from rpi_ws281x import Color
import json
from PIL import ImageColor
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
          
def Update():
     Ledstrip.setColor(Color(0, 0, 0))
     while True:
          data, addr = sockRX.recvfrom(2048) # buffer size is 1024 bytes
          JsonStr = data.decode('utf_8')
          key = "HEX"
          if JsonStr:
               sockTX.sendto(bytes(JsonStr, "utf-8"), (UDP_TX_IP, UDP_TX_PORT)) 
               aDict = json.loads(JsonStr)
               

          if (JsonStr.find('{"NewClient":1}') != -1):
               newclient()
          elif (JsonStr.find('{"LedStrip0":1}') != -1):
                  sockTX.sendto(bytes('{"LedStrip0":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
                  Ledstrip.setColor(Color(255, 0, 0)) 
          elif (JsonStr.find('{"LedStrip0":0}') != -1):
                  sockTX.sendto(bytes('{"LedStrip0":0}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
                  Ledstrip.setColor(Color(0, 0, 0))
          elif (key in aDict):
               string = str(ImageColor.getrgb(aDict[key])).lstrip('()')
               numbers = re.findall(r'\d+', string)
               Ledstrip.setColor(Color(int(numbers[0]), int(numbers[1]), int(numbers[2])))

newclient()
p2 = Thread(target = Update)
p2.start()

while True:  
     sleep(10)
