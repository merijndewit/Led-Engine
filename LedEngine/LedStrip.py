from LedController import LedController

class LedStrip(LedController):
    
    pixelCount = 0

    def setPixelCount(amount):
        LedStrip.pixelCount = amount
        LedStrip.LedController.SetPixelAmount(amount)
