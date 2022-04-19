from LedPanel import LedPanel
from pixel_manager import PixelManager

import random
import time
            
class FishTank(LedPanel):
    
    #fish_tank_grid = []
    def __init__(self) -> None:
        super().__init__()
        self.fish_list = []
        self.food_list = []
        self.start_time = time.time()
        self.food_respawn_time = 10
        self.fish_count = 3

    
    def Start(self):
        super().__init__()
        #FishTank.fish_tank_grid = LedPanel.make2DArray(LedPanel.ledPanelsPixelWidth, LedPanel.ledPanelsPixelHeight)
        
        for i in range(self.fish_count):
            new_fish = Fish()
            new_fish.x = random.randint(0, self.ledPanelsPixelWidth - 1)
            new_fish.y = random.randint(0, self.ledPanelsPixelWidth - 1)
            self.fish_list.append(new_fish)
        
        while True:
            self.Update()
        
        
        
    def Update(self):
        #draw fish
        PixelManager.Clear()
        
        if time.time() - self.start_time >= self.food_respawn_time: # spawn food
            new_food = FishFood()
            self.food_list.append(new_food)
            self.start_time = time.time()
            
        if self.food_list == []:
            for i in range(len(self.fish_list)):
                self.fish_list[i].Idle()
        else:  
            for j in range(len(self.fish_list)):
                for i in range(len(self.food_list[::-1])): # draw all food
                    pixel = self.getPixelNumber(self.food_list[i].x, self.food_list[i].y)
                    PixelManager.Set_Pixel(pixel, (0, 255, 200), False)
                    if self.food_list[i].x == self.fish_list[j].x and self.food_list[i].y == self.fish_list[j].y:
                        self.food_list.remove(self.food_list[i])
                    else:
                        if (self.fish_list[j].Check_Food_Distance(self.food_list[i].x, self.food_list[i].y)):
                            self.fish_list[j].Go_To_Food(self.food_list[i].x, self.food_list[i].y)
                        else:
                            self.fish_list[j].Idle()
                            
        for i in range(len(self.fish_list)): # draw all fish with their tails
            pixel = self.getPixelNumber(self.fish_list[i].x, self.fish_list[i].y)
            PixelManager.Set_Pixel(pixel, (255, 50, 0), False)
            print(self.fish_list[i].x, self.fish_list[i].y)
            pixel = self.getPixelNumber(self.fish_list[i].GetTailLocation()[0], self.fish_list[i].GetTailLocation()[1])
            PixelManager.Set_Pixel(pixel, (255, 50, 0), False)
                
        time.sleep(0.2)
        print("show")
        PixelManager.Show_All()
        
        
class Fish(FishTank):
    def __init__(self):
        super().__init__()
        self.FISHUP = 0
        self.FISHRIGHT = 1
        self.FISHDOWN = 2
        self.FISHLEFT = 3
        
        self.sight_radius = 7
        self.moving_direction = self.FISHRIGHT
        self.x = 0
        self.y = 0
        
    def Idle(self):
        if (random.randint(0, 1)):
            self.moving_direction = random.randint(0, 3)
            
        if self.moving_direction == self.FISHUP:
            self.y -= 1
            if self.y == -1:
                self.y = 1
                self.moving_direction = self.FISHDOWN
        elif self.moving_direction == self.FISHRIGHT:
            self.x += 1
            if self.x == self.ledPanelsPixelWidth:
                self.x = self.ledPanelsPixelWidth - 2
                self.moving_direction = self.FISHLEFT
        elif self.moving_direction == self.FISHDOWN:
            self.y += 1
            if self.y == self.ledPanelsPixelHeight:
                self.y = self.ledPanelsPixelHeight - 2
                self.moving_direction = self.FISHUP
        elif self.moving_direction == self.FISHLEFT:
            self.x -= 1
            if self.x == -1:
                self.x = 1
                self.moving_direction = self.FISHRIGHT
                
    def GetTailLocation(self):
        tail_x = self.x
        tail_y = self.y
        if self.moving_direction == self.FISHUP:
            tail_y = self.y + 1
        elif self.moving_direction == self.FISHRIGHT:
            tail_x = self.x - 1
        elif self.moving_direction == self.FISHDOWN:
            tail_y = self.y - 1
        elif self.moving_direction == self.FISHLEFT:
            tail_x = self.x + 1
        return tail_x, tail_y

    def Check_Food_Distance(self, food_x, food_y):
        if food_x < self.x + self.sight_radius and food_y < self.y + self.sight_radius and food_x > self.x - self.sight_radius and food_y > self.y - self.sight_radius: #collision
            return True
        return False
    
    def Go_To_Food(self, food_x, food_y):
        x_distance = self.x - food_x
        y_distance = self.y - food_y
        
        if abs(x_distance) > abs(y_distance):
            if x_distance < 0:
                self.moving_direction = self.FISHRIGHT
                self.x += 1
            else:
                self.moving_direction = self.FISHLEFT
                self.x -= 1
        else:
            if y_distance < 0:
                self.moving_direction = self.FISHDOWN
                self.y += 1
            else:
                self.moving_direction = self.FISHUP
                self.y -= 1
            
        
class FishFood(FishTank):
    def __init__(self):
        super().__init__()
        self.x = random.randint(0, self.ledPanelsPixelWidth - 1)
        self.y = random.randint(0, self.ledPanelsPixelWidth - 1)