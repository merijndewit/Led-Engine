from LedController import LedController
import jsonHelper

class LedStrip(LedController):
    def __init__(self) -> None:
        super().__init__()
        if (jsonHelper.Key_In_JSON("LedCount")):
            self.pixelCount = int(jsonHelper.Get_Key_Value("LedCount"))
        else:
            self.pixelCount = 256
