import time
import random

from LedStrip import LedStrip

class Stars(LedStrip):
    class Star:
        step = 1
        def __init__(self): #constructor
            self.value = 0
            self.declining = False
            self.position = 0
            self.maxValue = random.randint(20, 255)

        def nextStep(self):
            if self.declining == True:
                if self.value != 0:
                    self.value -= self.step
            else:
                if self.value == self.maxValue:
                    self.declining = True
                else:
                    self.value += self.step

    class TwingklingStar(Star):
        originalValue = 0
        def nextStep(self):
            self.value = self.originalValue
            if self.declining == True:
                if self.originalValue != 0:
                    self.originalValue -= self.step
            else:
                if self.originalValue == self.maxValue:
                    self.declining = True
                else:
                    self.originalValue += self.step
            if self.originalValue >= 5 and self.value <= self.maxValue:
                self.value = random.randint(-5, 5)
                self.value += self.originalValue

    starsPerSecond = 1

    def setStarsPerSecond(value):
        Stars.starsPerSecond = int(value)
        
    @classmethod
    def Start(cls):
        starList = []
        startTime = time.time()
        while True:
            if time.time() - startTime >= 1 / Stars.starsPerSecond:
                randomNumber = int(random.randint(0, 3))
                if randomNumber == 0:
                    newStar = Stars.TwingklingStar()
                else:
                    newStar = Stars.Star()
                newStar.position = int(random.randint(0, cls.pixelCount - 1))
                starList.append(newStar)
                startTime = time.time()

            for star in range(len(starList)):
                cls.pixels[starList[star].position] = ((cls.oneColorModeHex[0]*(starList[star].value / 255) * (cls.Rpercentage / 100)*(cls.ledBrightness / 100), cls.oneColorModeHex[1] * (starList[star].value / 255) * (cls.Gpercentage / 100)*(cls.ledBrightness / 100), cls.oneColorModeHex[2] * (starList[star].value / 255) * (cls.Bpercentage / 100)*(cls.ledBrightness / 100)))

                starList[star].nextStep()
            
            newList = starList.copy()
            for i in range(len(starList)):
                if starList[i].value == 0 and starList[i].declining == True:
                    del newList[i]
            starList = newList.copy()
            time.sleep(0.05)    
            cls.pixels.show()
