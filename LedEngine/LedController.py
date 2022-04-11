import board
import neopixel
import jsonHelper

class LedController:
    
    def __init__(self) -> None:
        if (jsonHelper.Key_In_JSON("redCalibration")):
            self.Rpercentage = int(jsonHelper.Get_Key_Value("redCalibration"))
        else:
            self.Rpercentage = 100
        if (jsonHelper.Key_In_JSON("greenCalibration")):
            self.Gpercentage = int(jsonHelper.Get_Key_Value("greenCalibration"))
        else:
            self.Gpercentage = 100
        if (jsonHelper.Key_In_JSON("blueCalibration")):
            self.Bpercentage = int(jsonHelper.Get_Key_Value("blueCalibration"))
        else:
            self.Bpercentage = 100
        if (jsonHelper.Key_In_JSON("brightnessValue")):
            self.ledBrightness = int(jsonHelper.Get_Key_Value("brightnessValue"))
        else:
            self.ledBrightness = 10
        if (jsonHelper.Key_In_JSON("LedCount")):
            self.pixels = neopixel.NeoPixel(board.D21, int(jsonHelper.Get_Key_Value("LedCount")), auto_write=False)
        else:
            self.pixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)
        if (jsonHelper.Key_In_JSON("colorEffect")):
            string = str(jsonHelper.Get_Key_Value("colorEffect")).lstrip("#")
            self.oneColorModeHex = (int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16))
        else:
            self.oneColorModeHex = (50, 0, 0)
            
        
    
    def sethexOneColorEffect(string):
        LedController.oneColorModeHex = (int(string[1:3], 16), int(string[3:5], 16), int(string[5:7], 16))

    def SetPixelAmount(amount):
        LedController.pixels = neopixel.NeoPixel(board.D21, int(amount), auto_write=False)
        jsonHelper.WriteToJsonFile("LedCount", str(amount))
        print("set pixel amount to: " + amount)

    def Clear(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def SetBrightness(brightnessValue):
        LedController.ledBrightness = int(brightnessValue)
        jsonHelper.WriteToJsonFile("brightnessValue", brightnessValue)

    def RedCalibration(percentage):
        LedController.Rpercentage = int(percentage)
        jsonHelper.WriteToJsonFile("redCalibration", str(percentage))
    def GreenCalibration(percentage):
        LedController.Gpercentage = int(percentage)
        jsonHelper.WriteToJsonFile("greenCalibration", str(percentage))
    def BlueCalibration(percentage):
        LedController.Bpercentage = int(percentage)
        jsonHelper.WriteToJsonFile("", str(percentage))

    def sendToClient(message):
        import Controller
        Controller.sendToClient(message)
        