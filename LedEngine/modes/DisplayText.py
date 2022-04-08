from PIL import Image, ImageFont, ImageDraw
import time

from LedPanel import LedPanel

class DisplayText(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
        self.textToDisplay = ""
        self.textSpeed = 300
        self.textFontSize = 9
        self.removeTopPixels = 0

    def SetDisplayText(self, value):
        self.textToDisplay = value

    def SetTextSpeed(self, value):
        self.textSpeed = int(value)

    def SetTextFontSize(self, value):
        self.textFontSize = int(value)

    def SetRemoveTopPixels(self, value):
        self.removeTopPixels = int(value)

    def Start(self):
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
                        self.pixels[self.getPixelNumber(width, height)] = (r * ((self.Rpercentage / 100)*(self.ledBrightness / 100)), g * (self.Gpercentage / 100)*(self.ledBrightness / 100), b * (self.Bpercentage / 100)*(self.ledBrightness / 100))
                
                self.pixels.show()
                return
            else: #scroll function if thext doesnt fit in the led panel completely
                for widthPos in range(img.width - self.ledPanelsPixelWidth):
                    for width in range(min( img.width, self.ledPanelsPixelWidth)):
                        for height in range(min(img.height - self.removeTopPixels, self.ledPanelsPixelHeight)):
                            r, g, b = img.getpixel((width + widthPos, height + self.removeTopPixels))  
                            print(r, g, b)
                            print("setPixel", self.getPixelNumber(width, height) )
                            self.pixels[self.getPixelNumber(width, height)] = (((r / 255) * self.oneColorModeHex[0]) * ((self.Rpercentage / 100)*(self.ledBrightness / 100)), ((g / 255) * self.oneColorModeHex[1]) * (self.Gpercentage / 100)*(self.ledBrightness / 100), ((b / 255) * self.oneColorModeHex[2]) * (self.Bpercentage / 100)*(self.ledBrightness / 100))
                    self.pixels.show()
                    time.sleep((self.textSpeed / 1000) + waitExtraSec)
                    waitExtraSec = 0
            waitExtraSec = 0.75
            time.sleep(waitExtraSec)
            