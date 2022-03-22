import board
import neopixel

class LedController:
    Rpercentage = 100
    Gpercentage = 100
    Bpercentage = 100
    ledBrightness = 100

    oneColorModeHex = (50, 0, 0)

    def sethexOneColorEffect(value):
        LedController.oneColorModeHex = value

    pixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)
    
    def SetPixelAmount(amount):
        from jsonHelper import JsonHelper
        LedController.pixels = neopixel.NeoPixel(board.D21, int(amount), auto_write=False)
        JsonHelper.WriteToJsonFile("LedCount", str(amount))

    def Clear():
        LedController.pixels.fill((0, 0, 0))
        LedController.pixels.show()

    def SetBrightness(brightnessValue):
        LedController.ledBrightness = brightnessValue

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
        