import os
from LedController import LedController

class LedPanel(LedController):
    pixelArray = []
    panels2DArray = []
    width = 0
    height = 0
    ledPanelWidth = 0
    ledPanelHeight = 0
    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0
    amountOfPanelsInWidth = 1
    amountOfPanelsInHeight = 1

    def make2DArray(cols, rows):
        listRow = [0] * cols
        listCol = []
        for i in range(rows): 
            listCol.append(listRow.copy())
        return listCol

    def __init__(self):
        if(os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/config.json') == 1):
            from jsonHelper import JsonHelper
            JsonHelper.LoadJsonValues()
            LedPanel.ledPanelsPixelWidth = LedPanel.ledPanelWidth * LedPanel.amountOfPanelsInWidth
            LedPanel.ledPanelsPixelHeight = LedPanel.ledPanelHeight * LedPanel.amountOfPanelsInHeight
            LedPanel.pixelArray = LedPanel.make2DArray(LedPanel.ledPanelsPixelWidth, LedPanel.ledPanelsPixelHeight)
            LedPanel.panels2DArray = LedPanel.make2DArray(LedPanel.amountOfPanelsInWidth, LedPanel.amountOfPanelsInHeight)
            LedPanel.NewPixelArray()

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

    def getPixelNumber(corX, corY):
        index = 0
        
        #these calculations calculates what part of the grid the pixel is 
        panelX = int(corX / LedPanel.ledPanelWidth) 
        panelY = int(corY / LedPanel.ledPanelHeight)

        #these calculations calculate the pixel number of the ledpanel
        panelPixelX = corX - (panelX * LedPanel.ledPanelWidth)
        panelPixelY = corY - (panelY * LedPanel.ledPanelHeight)
    
        if (int(panelPixelY) % 2) == 0: #you can easely mirror the image by changing == to !=
            index = (int(panelPixelY) * LedPanel.ledPanelWidth) + (LedPanel.ledPanelWidth - int(panelPixelX)) - 1
        else:
            index = (int(panelPixelY) * LedPanel.ledPanelWidth) + int(panelPixelX)
        
        index += LedPanel.panels2DArray[panelY][panelX] * (LedPanel.ledPanelWidth * LedPanel.ledPanelHeight)
        return index

    def setPanelArray(x, y, value):
        LedPanel.panels2DArray[x][y] = value

    def SetAmountOfPanelsInWidth(value):
        LedPanel.amountOfPanelsInWidth = value
        LedPanel.panels2DArray = LedPanel.make2DArray(LedPanel.amountOfPanelsInWidth, LedPanel.amountOfPanelsInHeight)

    def SetAmountOfPanelsInHeight(value):
        LedPanel.amountOfPanelsInHeight = value
        LedPanel.panels2DArray = LedPanel.make2DArray(LedPanel.amountOfPanelsInWidth, LedPanel.amountOfPanelsInHeight)

    def NewPixelArray():
        LedPanel.pixelArray = []
        for i in range(LedPanel.ledPanelsPixelWidth):
            rowY = []
            for ii in range(LedPanel.ledPanelsPixelHeight):
                rowY.append('#000000')
            LedPanel.pixelArray.append(rowY)

    def setConfigPanelWidth(value):
        LedPanel.ledPanelsPixelWidth = value
        LedPanel.NewPixelArray()

    def setConfigPanelHeight(value):
        LedPanel.ledPanelsPixelHeight = value
        LedPanel.NewPixelArray()