from PIL import Image
import os

from LedPanel import LedPanel

class SaveCanvas(LedPanel):
    imageName = ""

    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0

    def CreateImage():
        SaveCanvas.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        SaveCanvas.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight

        if SaveCanvas.imageName != "":
            img = Image.new('RGB', [SaveCanvas.ledPanelsPixelWidth, SaveCanvas.ledPanelsPixelHeight], 255)
            data = img.load()
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    string = str(LedPanel.pixelArray[x][y])
                    data[x,y] = (int(string[1:3], 16), int(string[3:5], 16), int(string[5:7], 16))

            img.save(os.path.dirname(os.path.realpath(__file__))+'/savedImages/'+SaveCanvas.imageName + '.png')

    def SetImageName(value):
        print("set image name: ", value)
        SaveCanvas.imageName = value

    def GetImageNames():
        imageNames = []
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/savedImages"):
            if file.endswith(".png"):
                imageNames.append(file)
        print(imageNames)
        return(imageNames)
