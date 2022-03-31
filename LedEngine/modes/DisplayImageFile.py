import os
import json
from PIL import Image

from LedPanel import LedPanel

class DisplayImageFile(LedPanel):
    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0

    @classmethod
    def LoadUploadedFile(cls):
        DisplayImageFile.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        DisplayImageFile.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight

        path = os.path.dirname(os.path.realpath(__file__))+"/uploads"
        imageName = "tmp.png"
        files = os.listdir(path)

        if (files == ""):
            return
        for f in files:
            if (f != ""):
                filePath = path+"/"+str(f)
                DisplayImageFile.DownscaleImage(filePath, "tmp.png")
                os.remove(filePath)

        pixelList = []
        image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/savedImages/"+imageName)
        if (image.width == DisplayImageFile.ledPanelsPixelWidth and image.height == DisplayImageFile.ledPanelsPixelHeight):
            rgb_im = image.convert('RGB')
            LedPanel.Clear()
            for y in range(DisplayImageFile.ledPanelsPixelHeight):
                for x in range(DisplayImageFile.ledPanelsPixelWidth):
                    pixel = int(LedPanel.getPixelNumber(x, y))
                    r, g, b = rgb_im.getpixel((x, y))  
                    LedPanel.pixels[pixel] = (r * ((cls.Rpercentage / 100)*(cls.ledBrightness / 100)), g * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), b * (cls.Bpercentage / 100)*(cls.ledBrightness / 100))
                    data_set = {"X": x, "Y": y, "R": r, "G": g, "B": b}
                    pixelList.append(json.dumps(data_set))
                LedPanel.pixels.show()
        return pixelList

    def DownscaleImage(imagePath, newName):
        image = Image.open(imagePath)
        resized_image = image.resize((DisplayImageFile.ledPanelsPixelWidth, DisplayImageFile.ledPanelsPixelHeight))
        #resized_image.save('savedImages/'+'new'+ '.png')
        resized_image.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+newName)



