from LedPanel import LedPanel
from pixel_manager import PixelManager
from color import Color

class LangtonsAnt(LedPanel):
    
    def __init__(self) -> None:
        super().__init__()
    
        self.antGrid = []
        self.x = 0
        self.y = 0
        self.dir = 0
        self.color = (0, 0, 0)

        self.ANTUP = 0
        self.ANTRIGHT = 1
        self.ANTDOWN = 2
        self.ANTLEFT = 3
    

    def Start(self):
        super().__init__()
        self.antGrid = self.make2DArray(self.ledPanelsPixelWidth, self.ledPanelsPixelHeight)
        self.x = int(self.ledPanelsPixelWidth / 2)
        self.y = int(self.ledPanelsPixelHeight / 2)
        self.dir = self.ANTUP
        while True:
            self.drawAnt()

    def turnRight(self):
        self.dir += 1
        if (self.dir > self.ANTLEFT):
            self.dir = self.ANTUP
    
    def turnLeft(self):
        self.dir -= 1
        if (self.dir < self.ANTUP):
            self.dir = self.ANTLEFT

    def moveForward(self):
        if (self.dir == self.ANTUP):
            self.color = (255, 0, 150)
            self.y -= 1 
        elif (self.dir == self.ANTRIGHT):
            self.color = (255, 150, 0)
            self.x += 1
        elif (self.dir == self.ANTDOWN):
            self.color = (255, 150, 150)
            self.y += 1
        elif (self.dir == self.ANTLEFT):
            self.color = (255, 0, 0)
            self.x -= 1

        if (self.x > self.ledPanelsPixelWidth - 1):
            self.x = 0
        elif (self.x < 0):
            self.x = self.ledPanelsPixelWidth - 1
        if (self.y > self.ledPanelsPixelHeight - 1):
            self.y = 0
        elif (self.y < 0) :
            self.y = self.ledPanelsPixelHeight - 1

    def drawAnt(self):
        for n in range(100):
            state = self.antGrid[self.x][self.y]
            if (state == 0):
                self.turnRight()
                self.antGrid[self.x][self.y] = 1
            elif (state == 1):
                self.turnLeft()
                self.antGrid[self.x][self.y] = 0
            if (self.antGrid[self.x][self.y] == 1):
                self.color = (0, 0, 0)
            col = Color()
            col.set_color_rgb_tup(self.color)
            pixel = self.getPixelNumber(self.x, self.y)
            PixelManager.set_color(col, pixel)

            self.moveForward()
            #time.sleep(0.05)
            PixelManager.show_all()