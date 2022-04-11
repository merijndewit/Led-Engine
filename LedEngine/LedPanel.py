import os
import jsonHelper
from LedController import LedController

class LedPanel(LedController):

    def make2DArray(self, cols, rows):
        listRow = [0] * cols
        listCol = []
        for i in range(rows):
            listCol.append(listRow.copy())
        return listCol
    
    def __init__(self) -> None:
        super().__init__()
        self.pixelArray = []
        self.panels2DArray = []

        if (jsonHelper.Key_In_JSON("LEDPanelWidth")):
            self.ledPanelWidth = int(jsonHelper.Get_Key_Value("LEDPanelWidth"))
        else:
            self.ledPanelWidth = 16
        if (jsonHelper.Key_In_JSON("LEDPanelHeight")):
            self.ledPanelHeight = int(jsonHelper.Get_Key_Value("LEDPanelHeight"))
        else:
            self.ledPanelHeight = 16
        if (jsonHelper.Key_In_JSON("amountOfPanelsInWidth")):
            self.amountOfPanelsInWidth = int(jsonHelper.Get_Key_Value("amountOfPanelsInWidth"))
        else:
            self.amountOfPanelsInWidth = 1
        if (jsonHelper.Key_In_JSON("amountOfPanelsInHeight")):
            self.amountOfPanelsInHeight = int(jsonHelper.Get_Key_Value("amountOfPanelsInHeight"))
        else:
            self.amountOfPanelsInHeight = 1

        self.ledPanelsPixelWidth = self.ledPanelWidth * self.amountOfPanelsInWidth
        self.ledPanelsPixelHeight = self.ledPanelHeight * self.amountOfPanelsInHeight
        self.pixelArray = self.make2DArray(self.ledPanelsPixelWidth, self.ledPanelsPixelHeight)
        self.panels2DArray = self.make2DArray(self.amountOfPanelsInWidth, self.amountOfPanelsInHeight)
        self.NewPixelArray()

    # get pixel number with lookup table methode
    # converts coordinates to the pixel number on the led panel
    # this function is for an led panel with a zigzag pattern
    # LedStrip:  
    #   _________
    #   _________|
    #  |_________
    #   _________|
    #  |_________

    #def getPixelNumber(corX, corY):
    #    rowX = []
    #    x = 16 #width
    #    y = 16 #height
    #    for i in range(x):
    #        rowY = []
    #        for ii in range(y):
    #            if (i % 2) == 0: #check if number is even
    #                rowY.append((i * y) + ii)
    #            else:
    #                rowY.insert(0, ((i * y) + ii))
    #        rowX.append(rowY)
    #    return rowX[int(corY)][int(corX)]¨

    def getPixelNumber(self, corX, corY):
        index = 0
        
        #these calculations calculates what part of the grid the pixel is 
        panelX = int(corX / self.ledPanelWidth) 
        panelY = int(corY / self.ledPanelHeight)

        #these calculations calculate the pixel number of the ledpanel
        panelPixelX = corX - (panelX * self.ledPanelWidth)
        panelPixelY = corY - (panelY * self.ledPanelHeight)
    
        if (int(panelPixelY) % 2) == 0: #you can easely mirror the image by changing == to !=
            index = (int(panelPixelY) * self.ledPanelWidth) + (self.ledPanelWidth - int(panelPixelX)) - 1
        else:
            index = (int(panelPixelY) * self.ledPanelWidth) + int(panelPixelX)
        
        index += self.panels2DArray[panelY][panelX] * (self.ledPanelWidth * self.ledPanelHeight)
        return index

    def setPanelArray(aDict):
        self.panels2DArray[int(aDict.get("x"))][int(aDict.get("y"))] = int(aDict.get("value"))

    def SetAmountOfPanelsInWidth(value):
        from jsonHelper import JsonHelper
        self.amountOfPanelsInWidth = int(value)
        self.panels2DArray = self.make2DArray(self.amountOfPanelsInWidth, self.amountOfPanelsInHeight)
        JsonHelper.WriteToJsonFile("amountOfPanelsInWidth", str(value))

    def SetAmountOfPanelsInHeight(value):
        from jsonHelper import JsonHelper
        self.amountOfPanelsInHeight = int(value)
        self.panels2DArray = self.make2DArray(self.amountOfPanelsInWidth, self.amountOfPanelsInHeight)
        JsonHelper.WriteToJsonFile("amountOfPanelsInHeight", str(value))

    def NewPixelArray(self):
        self.pixelArray = []
        for i in range(self.ledPanelsPixelWidth):
            rowY = []
            for ii in range(self.ledPanelsPixelHeight):
                rowY.append('#000000')
            self.pixelArray.append(rowY)
        #self.Clear()

    def setConfigPanelWidth(value):
        from jsonHelper import JsonHelper
        self.ledPanelsPixelWidth = int(value)
        self.NewPixelArray()
        JsonHelper.WriteToJsonFile("LEDPanelWidth", str(value))

    def setConfigPanelHeight(value):
        from jsonHelper import JsonHelper
        self.ledPanelsPixelHeight = int(value)
        self.NewPixelArray()
        JsonHelper.WriteToJsonFile("LEDPanelHeight", str(value))