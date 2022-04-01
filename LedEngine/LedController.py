import board
import neopixel

class LedController:
    
    def __init__(self) -> None:
        
        self.Rpercentage = 100
        self.Gpercentage = 100
        self.Bpercentage = 100
        self.ledBrightness = 100
        self.oneColorModeHex = (50, 0, 0)
        self.pixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)
    
    def sethexOneColorEffect(string):
        LedController.oneColorModeHex = (int(string[1:3], 16), int(string[3:5], 16), int(string[5:7], 16))

    def SetPixelAmount(amount):
        from jsonHelper import JsonHelper
        LedController.pixels = neopixel.NeoPixel(board.D21, int(amount), auto_write=False)
        JsonHelper.WriteToJsonFile("LedCount", str(amount))
        print("set pixel amount to: " + amount)

    def Clear(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def SetBrightness(brightnessValue):
        from jsonHelper import JsonHelper
        LedController.ledBrightness = int(brightnessValue)
        JsonHelper.WriteToJsonFile("brightnessValue", brightnessValue)

    def RedCalibration(percentage):
        from jsonHelper import JsonHelper
        LedController.Rpercentage = int(percentage)
        JsonHelper.WriteToJsonFile("redCalibration", str(percentage))
    def GreenCalibration(percentage):
        from jsonHelper import JsonHelper
        LedController.Gpercentage = int(percentage)
        JsonHelper.WriteToJsonFile("greenCalibration", str(percentage))
    def BlueCalibration(percentage):
        from jsonHelper import JsonHelper
        LedController.Bpercentage = int(percentage)
        JsonHelper.WriteToJsonFile("blueCalibration", str(percentage))

    def sendToClient(message):
        import Controller
        Controller.sendToClient(message)
        