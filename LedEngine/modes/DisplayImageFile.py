import os
import json
from PIL import Image

from LedPanel import LedPanel
from pixel_manager import PixelManager

class DisplayImageFile(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
        self.imageName = "tmp.png"

    def LoadUploadedFile(self):
        super().__init__()
        path = os.path.dirname(os.path.realpath(__file__))+"/../uploads"
        
        files = os.listdir(path)

        if (files == ""):
            return
        for f in files:
            if (f != ""):
                filePath = path+"/"+str(f)
                self.DownscaleImage(filePath, "tmp.png")
                os.remove(filePath)

        pixelList = []
        image = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../savedImages/"+self.imageName)
        if (image.width == self.ledPanelsPixelWidth and image.height == self.ledPanelsPixelHeight):
            rgb_im = image.convert('RGB')
            self.Clear()
            for y in range(self.ledPanelsPixelHeight):
                for x in range(self.ledPanelsPixelWidth):
                    pixel = int(self.getPixelNumber(x, y))
                    r, g, b = rgb_im.getpixel((x, y))  
                    #self.neopixels[pixel] = (r * ((self.Rpercentage / 100)*(self.ledBrightness / 100)), g * (self.Gpercentage / 100)*(self.ledBrightness / 100), b * (self.Bpercentage / 100)*(self.ledBrightness / 100))
                    PixelManager.Set_Pixel(pixel, (r, g, b), True)
                    data_set = {"X": x, "Y": y, "R": r, "G": g, "B": b}
                    pixelList.append(json.dumps(data_set))
                PixelManager.Show_All()
        return pixelList

    def DownscaleImage(self, imagePath, newName):
        image = Image.open(imagePath)
        resized_image = image.resize((self.ledPanelsPixelWidth, self.ledPanelsPixelHeight))
        #resized_image.save('savedImages/'+'new'+ '.png')
        resized_image.save(os.path.dirname(os.path.realpath(__file__))+'/../savedImages/'+newName)



