from PIL import Image, ImageFont, ImageDraw
import time

from LedPanel import LedPanel

class DisplayText(LedPanel):
    textToDisplay = ""
    textSpeed = 300
    textFontSize = 9
    removeTopPixels = 0

    def SetDisplayText(value):
        DisplayText.textToDisplay = value

    def SetTextSpeed(value):
        DisplayText.textSpeed = value

    def SetTextFontSize(value):
        DisplayText.textFontSize = value

    def SetRemoveTopPixels(value):
        DisplayText.removeTopPixels = value
    
    @classmethod
    def Start(cls):
        font = ImageFont.truetype('font/PixeloidSans.ttf', cls.textFontSize)
        print("length", font.getsize(cls.textToDisplay))
        img = Image.new(mode="RGB", size=font.getsize(cls.textToDisplay))
        
        draw = ImageDraw.Draw(im=img)

        draw.text(xy=(0, 0), text=cls.textToDisplay, font=font, fill='#ffffff')
        waitExtraSec = 1.25
        while True:
            if img.width < cls.ledPanelsPixelWidth:
                for width in range(min( img.width, cls.ledPanelsPixelWidth)):
                    for height in range(min(img.height - cls.removeTopPixels, cls.ledPanelsPixelHeight)):
                        r, g, b = img.getpixel((width, height + cls.removeTopPixels))  
                        cls.pixels[LedPanel.getPixelNumber(width, height)] = (r * ((cls.Rpercentage / 100)*(cls.ledBrightness / 100)), g * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), b * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
                
                cls.pixels.show()
                return
            else: #scroll function if thext doesnt fit in the led panel completely
                for widthPos in range(img.width - cls.ledPanelsPixelWidth):
                    for width in range(min( img.width, cls.ledPanelsPixelWidth)):
                        for height in range(min(img.height - cls.removeTopPixels, cls.ledPanelsPixelHeight)):
                            r, g, b = img.getpixel((width + widthPos, height + cls.removeTopPixels))  
                            print(r, g, b)
                            print("setPixel", LedPanel.getPixelNumber(width, height) )
                            cls.pixels[LedPanel.getPixelNumber(width, height)] = (((r / 255) * cls.oneColorModeHex[0]) * ((cls.Rpercentage / 100)*(cls.ledBrightness / 100)), ((g / 255) * cls.oneColorModeHex[1]) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), ((b / 255) * cls.oneColorModeHex[2]) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
                    cls.pixels.show()
                    time.sleep((cls.textSpeed / 1000) + waitExtraSec)
                    waitExtraSec = 0
            waitExtraSec = 0.75
            time.sleep(waitExtraSec)