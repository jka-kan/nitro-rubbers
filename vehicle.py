import pygame
import copy
from cons import Cons

class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface([500, 500])
       # self.image = pygame.image.load('bus10.png').convert_alpha()
        self.image = pygame.image.load('car.png').convert_alpha()
        self.scale_width = 100
        self.scale_height = 100
        self.rotation = 0
        self.horiz_speed = 0
        self.doing_rotation = 0
        self.off_road = False
        self.y_corr = 0

        # Get the original dimensions
        original_width, original_height = self.image.get_size()
        
        if self.scale_width and not self.scale_height:
            # Calculate new height to maintain the aspect ratio
            aspect_ratio = original_height / original_width
            self.scale_height = int(self.scale_width * aspect_ratio)
        elif self.scale_height and not self.scale_width:
            # Calculate new width to maintain the aspect ratio
            aspect_ratio = original_width / original_height
            self.scale_width = int(self.scale_height * aspect_ratio)
        elif not self.scale_width and not self.scale_height:
            # No scaling provided, use original dimensions
            self.scale_width, self.scale_height = original_width, original_height

        # Scale the image while maintaining aspect ratio
#        self.image.fill("blue")
        self.image = pygame.transform.scale(self.image, (self.scale_width, self.scale_height))
#        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image_clean = copy.copy(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(Cons.width / 2, Cons.height + 100))

    def make_turn(self, rotation):
        self.rotation += rotation

    def turn(self):
        if self.rotation == 0:
            return False

        if self.rotation < 0:
            self.rect.x += int(-(self.rotation / 5))

        if self.rotation > 0:
            self.rect.x -= int(self.rotation / 5)

        if self.rotation > 45:
            self.rotation = 45
        elif self.rotation < -45:
            self.rotation = -45

#        self.image = pygame.transform.rotate(self.image_clean, self.rotation)
#        if self.rotation > -5 and self.rotation < 5 and self.y_corr == 0:
#            self.y_corr = 5
#        
#        if self.y_corr > 0:
#            self.rect.y -= 1
#            self.y_corr -= 1

        self.image = pygame.transform.rotozoom(self.image_clean, self.rotation, 1)
        return True

    def move(self):
    
        if self.turn():
            self.mask = pygame.mask.from_surface(self.image)
   
    def get_center_rect(self):
        return self.image.get_rect(center=(self.rect.x, self.rect.y))

    def check_screen_border(self):
        if self.rect.left < 40:
            self.make_turn(-2)
        elif self.rect.right > Cons.width - 40:
            self.make_turn(2)

    def update(self, *args):
        self.check_screen_border()
        self.move()


class Player(Vehicle):
    def __init__(self, screen):
        super().__init__()
        self.olist = self.mask.outline()
        pygame.draw.lines(screen, "yellow", False, list(self.olist), 10)

       


class EnemyCar(Vehicle):
    def __init__(self, center_points, road_width):
        super().__init__()
        self.road_width = road_width
        self.center_points = center_points
        self.prev_x = self.rect.x
        self.avg_center_points = {}
        self.center_ahead = 0
        self.temp_points = []
        self.target = 0
        self.speed = 5 
        self.cycle = 0
        self.rotated = 0
        self.on_road = True

        for key in self.center_points:
            self.temp_points.append(self.center_points[key])


    def move_enemy(self, test, road_scroll_speed):
#        print("ROAD SPRITE: ", test)
#        print("Y     ", self.rect.y)

        road_y = test + (1000 - (self.rect.y))  # Was abs()

#        print("ROAD_Y:" , road_y, "rect.y:", self.rect.y, "speed:", self.speed)
#        center = self.center_points[road_y] 
        
#        self.center_ahead = self.center_points[road_y + 2]
       
        segment_len = 5 
        if road_y % segment_len == 0:
            try:
                self.center_ahead = self.center_points[road_y + segment_len + int(self.speed)]
                self.target = -(self.center_ahead - self.rect.x) 
            except KeyError:
                pass

#        off_center = self.rect.x - center
        #print("ahead:", self.center_ahead, "center:", center, "target:", self.target, "rot:", self.rotation, "off:", off_center, "rect.x:", self.rect.x)

        if self.rect.x > self.center_ahead + self.road_width / 8:  # 7 50
            self.rotation += 1.5  # 0.5
            self.doing_rotation = 1
        elif self.rect.x < self.center_ahead - (self.road_width / 8): 
            self.rotation -= 1.5
            self.doing_rotation = -1

        elif self.rect.x < self.center_ahead + self.road_width / 12 and self.doing_rotation == 1: # 8
            self.rotation -= 3.5
            if self.rotation < 0:
                self.rotation = 0
        elif self.rect.x > self.center_ahead - self.road_width / 12 and self.doing_rotation == -1:  # 30
            self.rotation += 3.5
            if self.rotation > 0:
                self.rotation = 0

        elif self.rect.x < self.center_ahead + self.road_width / 17 and self.doing_rotation == 1: 
            self.rotation -= 2.5
            if self.rotation < 0:
                self.rotation = 0
        elif self.rect.x > self.center_ahead - self.road_width / 17 and self.doing_rotation == -1:
            self.rotation += 2.5
            if self.rotation > 0:
                self.rotation = 0

        if self.rect.x < self.center_ahead + 4 and self.rect.x > self.center_ahead - 4:
            self.doing_rotation = 0

        if abs(self.rotation) > 15:
            self.speed -= 0.1
        else:
            self.speed += 0.5


        if self.speed <= 0.3:
            self.speed = 0.3
        elif self.speed > 14:
            self.speed = 14

        if self.rotation > 45:
            self.rotation = 45
        elif self.rotation < -45:
            self.rotation = -45


#        print("test:", test, "rect.x:", self.rect.x, "speed:", self.speed)

        self.rect.y -= int(self.speed) - road_scroll_speed
        self.turn()
        self.check_off_road()
        self.cycle += 1


    def check_off_road(self):
 #       print("ENEMY SPEED:", self.speed, "ON_ROAD: ", self.on_road)
        if not self.on_road and self.speed > 3:
            self.speed -= 1

    def update(self, *args):
        self.move_enemy(*args)
