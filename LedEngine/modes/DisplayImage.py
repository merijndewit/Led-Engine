import os
import urllib.request
import json
from PIL import Image

from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class DisplayImage(LedPanel):
    
    def __init__(self):
        super().__init__()
        self.url = ""

    def super_init(self):
        super().__init__()
        
    def UpdateUrl(self, value):
        self.url = str(value)
        print(self.url)

    def LoadUploadedFile(self):
        super().__init__()
        path = os.path.dirname(os.path.realpath(__file__))+"/../uploads"
        imageName = "tmp.png"
        files = os.listdir(path)

        if (files == ""):
            return
        for f in files:
            if (f != ""):
                filePath = path+"/"+str(f)
                self.DownscaleImage(filePath, "tmp.png")
                os.remove(filePath)
        return self.DisplayImageFile(imageName)

    def DownscaleImage(self, imagePath, newName):
        image = Image.open(imagePath)
        resized_image = image.resize((self.ledPanelsPixelWidth, self.ledPanelsPixelHeight))
        #resized_image.save('savedImages/'+'new'+ '.png')
        resized_image.save(os.path.dirname(os.path.realpath(__file__))+'/../savedImages/'+newName)

    def DisplayImageFile(self, imageName):
        pixelList = []
        image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../savedImages/"+imageName)
        if (image.width == self.ledPanelsPixelWidth and image.height == self.ledPanelsPixelHeight):
            rgb_im = image.convert('RGB')
            PixelManager.clear()
            for y in range(self.ledPanelsPixelHeight):
                for x in range(self.ledPanelsPixelWidth):
                    pixel = int(self.getPixelNumber(x, y))
                    r, g, b = rgb_im.getpixel((x, y))  
                    col = Color(r, g, b)
                    PixelManager.set_color(col, pixel, False)
                    #self.neopixels[pixel] = (r * ((self.Rpercentage / 100)*(self.ledBrightness / 100)), g * (self.Gpercentage / 100)*(self.ledBrightness / 100), b * (self.Bpercentage / 100)*(self.ledBrightness / 100))
                    data_set = {"X": x, "Y": y, "R": r, "G": g, "B": b}
                    pixelList.append(json.dumps(data_set))
                PixelManager.show_all()
        return pixelList

    def DisplayUrl(self):
        super().__init__()
        if self.url != "":
            imageName = "tmp.png"
            path = os.path.dirname(os.path.realpath(__file__))+"/../tmpImages/" + imageName
            try:
                urllib.request.urlretrieve(self.url, path)
            except:
                return []
            self.DownscaleImage(path, "tmp.png")
            return self.DisplayImageFile(imageName)

        print("no url entered", self.url)
        return



