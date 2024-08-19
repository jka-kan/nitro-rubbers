import pygame
from cons import Cons
import random
import time


# For storing and handling of obstacle objects
class Obstacle():
    def __init__(self, center_points, road_length):
        self.center_points = center_points
        self.road_length = road_length
        self.obstacles = []  # Container for obstacle instances
        self._obstacle = None
        self.create_obstacles()

    @property
    def obstacle(self):
        try:
            if self.obstacles[0].rect.y > Cons.height:
                self.obstacles.pop(0)
        except IndexError:
            pass
        for obs in self.obstacles:
            yield obs
        
    def create_obstacles(self):
        # Make random placements for the obstacles
        points = []
        count = Cons.height
        for i in range(1, 18):
            try:
                distance = random.randint(800, 1300)
                y = count + distance
                points.append(y)
                x = self.center_points[y]
                self.obstacles.append(ObstacleSprite(x, Cons.height * 2 - y))
                count += distance
                if count > self.road_length - 500:
                    break
            except KeyError as err:
                print("Error at obstacles", err)
        points.sort()


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('rock1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, scroll_speed):
        self.rect.y += scroll_speed

    def update(self, *args):
        self.move(*args)

