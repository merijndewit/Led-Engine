import os
import urllib
import json
from PIL import Image

from LedPanel import LedPanel

class DisplayImage(LedPanel):

    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0

    url = ""

    @classmethod
    def LoadUploadedFile(cls):
        path = os.path.dirname(os.path.realpath(__file__))+"/uploads"
        imageName = "tmp.png"
        files = os.listdir(path)

        if (files == ""):
            return
        for f in files:
            if (f != ""):
                filePath = path+"/"+str(f)
                DisplayImage.DownscaleImage(filePath, "tmp.png")
                os.remove(filePath)
        return DisplayImage.DisplayImageFile(imageName)

    def DownscaleImage(imagePath, newName):
        DisplayImage.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        DisplayImage.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight
        image = Image.open(imagePath)
        resized_image = image.resize((DisplayImage.ledPanelsPixelWidth, DisplayImage.ledPanelsPixelHeight))
        #resized_image.save('savedImages/'+'new'+ '.png')
        resized_image.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+newName)

    @classmethod
    def DisplayImageFile(cls, imageName):
        DisplayImage.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        DisplayImage.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight
        pixelList = []
        image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/savedImages/"+imageName)
        if (image.width == DisplayImage.ledPanelsPixelWidth and image.height == DisplayImage.ledPanelsPixelHeight):
            rgb_im = image.convert('RGB')
            LedPanel.Clear()
            for y in range(DisplayImage.ledPanelsPixelHeight):
                for x in range(DisplayImage.ledPanelsPixelWidth):
                    pixel = int(LedPanel.getPixelNumber(x, y))
                    r, g, b = rgb_im.getpixel((x, y))  
                    LedPanel.pixels[pixel] = (r * ((cls.Rpercentage / 100)*(cls.ledBrightness / 100)), g * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), b * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
                    data_set = {"X": x, "Y": y, "R": r, "G": g, "B": b}
                    pixelList.append(json.dumps(data_set))
                LedPanel.pixels.show()
        return pixelList

    @classmethod
    def DisplayUrl(cls):
        DisplayImage.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        DisplayImage.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight
        if DisplayImage.url != "":
            imageName = "tmp.png"
            path = os.path.dirname(os.path.realpath(__file__))+"/tmpImages/" + imageName
            try:
                urllib.request.urlretrieve(DisplayImage.url, path)
            except:
                return []
            DisplayImage.DownscaleImage(path, "tmp.png")
            return DisplayImage.DisplayImageFile(imageName)

        print("no url entered")

    def UpdateUrl(value):
        DisplayImage.url = str(value)

