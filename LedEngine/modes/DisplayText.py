from PIL import Image, ImageFont, ImageDraw
import time

from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class DisplayText(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
        self.textToDisplay = ""
        self.textSpeed = 300
        self.textFontSize = 9
        self.removeTopPixels = 0

    def super_init(self):
        super().__init__()

    def SetDisplayText(self, value):
        self.textToDisplay = value

    def SetTextSpeed(self, value):
        self.textSpeed = int(value)

    def SetTextFontSize(self, value):
        self.textFontSize = int(value)

    def SetRemoveTopPixels(self, value):
        self.removeTopPixels = int(value)

    def Start(self):
        super().__init__()
        font = ImageFont.truetype('font/PixeloidSans.ttf', self.textFontSize)
        print("length", font.getsize(self.textToDisplay))
        img = Image.new(mode="RGB", size=font.getsize(self.textToDisplay))
        
        draw = ImageDraw.Draw(im=img)

        draw.text(xy=(0, 0), text=self.textToDisplay, font=font, fill='#ffffff')
        waitExtraSec = 1.25
        while True:
            if img.width < self.ledPanelsPixelWidth:
                for width in range(min( img.width, self.ledPanelsPixelWidth)):
                    for height in range(min(img.height - self.removeTopPixels, self.ledPanelsPixelHeight)):
                        r, g, b = img.getpixel((width, height + self.removeTopPixels))  
                        if (r != 0 and g != 0 and b != 0):
                            red = (self.oneColorModeHex[0] + r) / 2
                            green = (self.oneColorModeHex[1] + g) / 2
                            blue = (self.oneColorModeHex[2] + b) / 2
                            col = Color(red, green, blue)
                            PixelManager.set_color(col, self.getPixelNumber(width, height))
                
                PixelManager.show_all()
                return
            else: #scroll function if thext doesnt fit in the led panel completely
                for widthPos in range(img.width - self.ledPanelsPixelWidth):
                    for width in range(min( img.width, self.ledPanelsPixelWidth)):
                        for height in range(min(img.height - self.removeTopPixels, self.ledPanelsPixelHeight)):
                            r, g, b = img.getpixel((width + widthPos, height + self.removeTopPixels))  
                            if (r != 0 and g != 0 and b != 0):
                                red = (self.oneColorModeHex[0] + r) / 2
                                green = (self.oneColorModeHex[1] + g) / 2
                                blue = (self.oneColorModeHex[2] + b) / 2
                                col = Color(red, green, blue)
                                PixelManager.set_color(col, self.getPixelNumber(width, height))
                    PixelManager.show_all()
                    PixelManager.clear()
                    time.sleep((self.textSpeed / 1000) + waitExtraSec)
                    waitExtraSec = 0
            waitExtraSec = 0.75
            time.sleep(waitExtraSec)
            