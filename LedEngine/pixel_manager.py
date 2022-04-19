import board
import neopixel
import jsonHelper

class PixelManager():
    
    canvas_pixel_list = []
    if (jsonHelper.Key_In_JSON("redCalibration")):
        Rpercentage = int(jsonHelper.Get_Key_Value("redCalibration"))
    else:
        Rpercentage = 100
    if (jsonHelper.Key_In_JSON("greenCalibration")):
        Gpercentage = int(jsonHelper.Get_Key_Value("greenCalibration"))
    else:
        Gpercentage = 100
    if (jsonHelper.Key_In_JSON("blueCalibration")):
        Bpercentage = int(jsonHelper.Get_Key_Value("blueCalibration"))
    else:
        Bpercentage = 100
    if (jsonHelper.Key_In_JSON("brightnessValue")):
        ledBrightness = int(jsonHelper.Get_Key_Value("brightnessValue"))
    else:
        ledBrightness = 10
    if (jsonHelper.Key_In_JSON("LedCount")):
        neopixels = neopixel.NeoPixel(board.D21, int(jsonHelper.Get_Key_Value("LedCount")), auto_write=False)
    else:
        neopixels = neopixel.NeoPixel(board.D21, 256, auto_write=False)
          
    @classmethod 
    def Clear(cls):
        cls.neopixels.fill((0, 0, 0))
        
    @classmethod 
    def ClearLeds(cls):
        cls.neopixels.fill((0, 0, 0))
        cls.Show_All()
        
    @classmethod
    def Fill(cls, color):
        cls.neopixels.fill((color[0] * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), color[1] * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), color[2] * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
        
    @classmethod    
    def Show_Pixel(cls, pixel, color, save):
        cls.neopixels[pixel] = (color[0] * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), color[1] * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), color[2] * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
        cls.Show_All()
        if save:
            cls.Save_Pixel(pixel, color)
            
    @classmethod    
    def Set_Pixel(cls, pixel, color, save):
        cls.neopixels[pixel] = (color[0] * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), color[1] * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), color[2] * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
        if save:
            cls.Save_Pixel(pixel, color)
     
    @classmethod     
    def Save_Pixel(cls, pixel, color):
        tup = (pixel, color)
        cls.canvas_pixel_list.append(tup)
        
    @classmethod     
    def Show_All(cls):
        PixelManager.neopixels.show()
