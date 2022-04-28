import jsonHelper

class LedController:
    
    def __init__(self) -> None:
        if (jsonHelper.Key_In_JSON("colorEffect")):
            string = str(jsonHelper.Get_Key_Value("colorEffect")).lstrip("#")
            self.oneColorModeHex = (int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16))
        else:
            self.oneColorModeHex = (50, 0, 0)
        