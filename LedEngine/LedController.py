from threading import Thread
from time import sleep     # Import the sleep function from the time module
import socket
import RPi.GPIO as GPIO

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
          sockTX.sendto(bytes('{"GPIO21T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))

               
def Update():
     while True:
          data, addr = sockRX.recvfrom(1024) # buffer size is 1024 bytes
          JsonStr = data.decode('utf_8')
          print(JsonStr)
          if (JsonStr.find('{"NewClient":1}') != -1):
               newclient()
          elif (JsonStr.find('{"GPIO21T":1}') != -1):
               if GPIO.input(21):
                  GPIO.output(21,GPIO.LOW)
                  sockTX.sendto(bytes('{"GPIO21T":0}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
               else:
                  GPIO.output(21,GPIO.HIGH)  
                  sockTX.sendto(bytes('{"GPIO21T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
          elif (JsonStr.find('{"GPIO21M":1}') != -1):
                  sockTX.sendto(bytes('{"GPIO21T":1}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
                  GPIO.output(21,GPIO.HIGH)  
          elif (JsonStr.find('{"GPIO21M":0}') != -1):
                  sockTX.sendto(bytes('{"GPIO21T":0}', "utf-8"), (UDP_TX_IP, UDP_TX_PORT))
                  GPIO.output(21,GPIO.LOW)  


newclient()
p2 = Thread(target = Update)
p2.start()

while True:  
     sleep(10)
