import jsonHelper
import os
import color
from led_lib import LedLib
from PIL import Image

class PixelManager():
    
    @classmethod
    def init(cls):
        cls.canvas_pixel_list = []
        if (jsonHelper.Key_In_JSON("redCalibration")):
            cls.Rpercentage = int(jsonHelper.Get_Key_Value("redCalibration"))
        else:
            cls.Rpercentage = 100
        if (jsonHelper.Key_In_JSON("greenCalibration")):
            cls.Gpercentage = int(jsonHelper.Get_Key_Value("greenCalibration"))
        else:
            cls.Gpercentage = 100
        if (jsonHelper.Key_In_JSON("blueCalibration")):
            cls.Bpercentage = int(jsonHelper.Get_Key_Value("blueCalibration"))
        else:
            cls.Bpercentage = 100
        if (jsonHelper.Key_In_JSON("brightnessValue")):
            cls.ledBrightness = int(jsonHelper.Get_Key_Value("brightnessValue"))
        else:
            cls.ledBrightness = 10
        if (jsonHelper.Key_In_JSON("LedCount")):
            LedLib(int(jsonHelper.Get_Key_Value("LedCount")))
        else:
            LedLib(256)
        if (jsonHelper.Key_In_JSON("LEDPanelWidth")):
            ledPanelWidth = int(jsonHelper.Get_Key_Value("LEDPanelWidth"))
        else:
            ledPanelWidth = 16
        if (jsonHelper.Key_In_JSON("LEDPanelHeight")):
            ledPanelHeight = int(jsonHelper.Get_Key_Value("LEDPanelHeight"))
        else:
            ledPanelHeight = 16
        if (jsonHelper.Key_In_JSON("amountOfPanelsInWidth")):
            amountOfPanelsInWidth = int(jsonHelper.Get_Key_Value("amountOfPanelsInWidth"))
        else:
            amountOfPanelsInWidth = 1
        if (jsonHelper.Key_In_JSON("amountOfPanelsInHeight")):
            amountOfPanelsInHeight = int(jsonHelper.Get_Key_Value("amountOfPanelsInHeight"))
        else:
            amountOfPanelsInHeight = 1
            
        cls.ledPanelsPixelWidth = ledPanelWidth * amountOfPanelsInWidth
        cls.ledPanelsPixelHeight = ledPanelHeight * amountOfPanelsInHeight
        cls.clear()
    
    @classmethod
    def clear(cls, show=False):
        cls.canvas_pixel_list = []
        for i in range(cls.ledPanelsPixelWidth * cls.ledPanelsPixelHeight):
            cls.canvas_pixel_list.append(color.Color()) #this appends a black color to the list
        if show:
            cls.show_all()
            
    @classmethod
    def fill_colors(cls, fill_color):
        cls.canvas_pixel_list = []
        for i in range(cls.ledPanelsPixelWidth * cls.ledPanelsPixelHeight):
            cls.canvas_pixel_list.append(fill_color)
        
    @classmethod    
    def set_color(cls, color, pixel_number, show=False):
        cls.save_color(color, pixel_number)
        if show:
            cls.show_all()
     
    @classmethod     
    def save_color(cls, color, pixel_number):
        cls.canvas_pixel_list[pixel_number] = color
        
    @classmethod     
    def show_all(cls):
        for i in range(len(cls.canvas_pixel_list)):
            LedLib.set_neopixel(i, (cls.canvas_pixel_list[i].r * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), cls.canvas_pixel_list[i].g * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), cls.canvas_pixel_list[i].b * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))
        LedLib.show_pixels()
        
    @classmethod
    def SetImageName(cls, value):
        cls.imageName = value
        
    @classmethod
    def Create_Image(cls):
        cls.imageName = "test"
        if cls.imageName != "":
            img = Image.new('RGB', [16, 16])
            data = img.load()
            snake_pattern = True
            for i in range(len(cls.canvas_pixel_list)):
                if (snake_pattern and int(i / cls.ledPanelsPixelWidth) % 2 != 1):
                    data[((cls.ledPanelsPixelWidth - 1) - i) % cls.ledPanelsPixelWidth, i / cls.ledPanelsPixelWidth] = cls.canvas_pixel_list[i].get_color_tup()
                else:
                    data[i % cls.ledPanelsPixelWidth, i / cls.ledPanelsPixelWidth] = cls.canvas_pixel_list[i].get_color_tup()
            img.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+cls.imageName + '.png')
