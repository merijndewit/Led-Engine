from LedPanel import LedPanel

class LangtonsAnt(LedPanel):
    antGrid = []
    x = 0
    y = 0
    dir = 0
    color = (0, 0, 0)

    ledPanelsPixelWidth = 0
    ledPanelsPixelHeight = 0

    ANTUP = 0
    ANTRIGHT = 1
    ANTDOWN = 2
    ANTLEFT = 3
    
    @classmethod
    def Start(cls):
        LangtonsAnt.ledPanelsPixelWidth = LedPanel.ledPanelsPixelWidth
        LangtonsAnt.ledPanelsPixelHeight = LedPanel.ledPanelsPixelHeight
        LangtonsAnt.antGrid = LedPanel.make2DArray(LangtonsAnt.ledPanelsPixelWidth, LangtonsAnt.ledPanelsPixelHeight)
        LangtonsAnt.x = int(LangtonsAnt.ledPanelsPixelWidth / 2)
        LangtonsAnt.y = int(LangtonsAnt.ledPanelsPixelHeight / 2)
        LangtonsAnt.dir = LangtonsAnt.ANTUP
        while True:
            LangtonsAnt.drawAnt()

    def turnRight():
        LangtonsAnt.dir += 1
        if (LangtonsAnt.dir > LangtonsAnt.ANTLEFT):
            LangtonsAnt.dir = LangtonsAnt.ANTUP
    
    def turnLeft():
        LangtonsAnt.dir -= 1
        if (LangtonsAnt.dir < LangtonsAnt.ANTUP):
            LangtonsAnt.dir = LangtonsAnt.ANTLEFT

    def moveForward():
        if (LangtonsAnt.dir == LangtonsAnt.ANTUP):
            LangtonsAnt.color = (2, 0, 1.5)
            LangtonsAnt.y -= 1 
        elif (LangtonsAnt.dir == LangtonsAnt.ANTRIGHT):
            LangtonsAnt.color = (2, 1.5, 0)
            LangtonsAnt.x += 1
        elif (LangtonsAnt.dir == LangtonsAnt.ANTDOWN):
            LangtonsAnt.color = (2, 1.5, 1.5)
            LangtonsAnt.y += 1
        elif (LangtonsAnt.dir == LangtonsAnt.ANTLEFT):
            LangtonsAnt.color = (2, 0, 0)
            LangtonsAnt.x -= 1

        if (LangtonsAnt.x > LangtonsAnt.ledPanelsPixelWidth - 1):
            LangtonsAnt.x = 0
        elif (LangtonsAnt.x < 0):
            LangtonsAnt.x = LangtonsAnt.ledPanelsPixelWidth - 1
        if (LangtonsAnt.y > LangtonsAnt.ledPanelsPixelHeight - 1):
            LangtonsAnt.y = 0
        elif (LangtonsAnt.y < 0) :
            LangtonsAnt.y = LangtonsAnt.ledPanelsPixelHeight - 1

    def drawAnt():
        for n in range(100):
            state = LangtonsAnt.antGrid[LangtonsAnt.x][LangtonsAnt.y]
            if (state == 0):
                LangtonsAnt.turnRight()
                LangtonsAnt.antGrid[LangtonsAnt.x][LangtonsAnt.y] = 1
            elif (state == 1):
                LangtonsAnt.turnLeft()
                LangtonsAnt.antGrid[LangtonsAnt.x][LangtonsAnt.y] = 0
            if (LangtonsAnt.antGrid[LangtonsAnt.x][LangtonsAnt.y] == 1):
                LangtonsAnt.color = (0, 0, 0)

            pixel = LedPanel.getPixelNumber(LangtonsAnt.x, LangtonsAnt.y)
            LedPanel.pixels[pixel] = (LangtonsAnt.color)

            LangtonsAnt.moveForward()
            #time.sleep(0.05)
            LedPanel.pixels.show()