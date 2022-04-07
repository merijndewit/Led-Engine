from LedController import LedController

class LedStrip(LedController):
    
    def __init__(self) -> None:
        super().__init__()
    
    pixelCount = 0

    def setPixelCount(amount):
        LedStrip.pixelCount = amount
        LedController.SetPixelAmount(amount)
