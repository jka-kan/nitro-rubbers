import pygame
import sys
from road import RoadSprite
from cons import Cons
from vehicle import Player, EnemyCar
from obstacle import Obstacle
import random
#from sounds import playerSound
#import threading
#import io
#import numpy as np



# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((Cons.width, Cons.height))
pygame.display.set_caption("Moving and Turning Line with Vectors")

running = True
clock = pygame.time.Clock()

vehicle_sprites_list = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
road_objects_list = pygame.sprite.Group()

# Test road math

#TEST = True 
TEST = False
if TEST:
    while True:
        print("\n----------------" * 5)
        road = RoadSprite(Cons.height, Cons.width)
        if road.run_test:
            break
else:
    road = RoadSprite(Cons.height, Cons.width)


road.rect.y = -(road.road_length - Cons.height)
road_objects_list.add(road)

player = Player(screen)
player.rect.x, player.rect.y = Cons.width / 2 + 100, Cons.height - Cons.player_y_offset
player_sprites_list = pygame.sprite.Group()
vehicle_sprites_list.add(player)

enemy1 = EnemyCar(road.road_center_points, road.road_width)
enemy1.rect.x, enemy1.rect.y = Cons.width / 2 + 100, 1000
vehicle_sprites_list.add(enemy1)

enemy2 = EnemyCar(road.road_center_points, road.road_width)
enemy2.rect.x, enemy2.rect.y = Cons.width / 2 + 200, 1000
vehicle_sprites_list.add(enemy2)

obs = Obstacle(road.road_center_points, road.road_length)

for o in obs.obstacle:
    obstacle_sprites.add(o)


# road_y keeps track on roads relative y-coord when it is scrolled
road_y = list(road.road_center_points.keys())[0]  
count = 0


# Testing sound
#current_pitch = 0.1 
#sound_thread = None
#sound_channel = pygame.mixer.Channel(0)  # Create a mixer channel
####sound_obj = playerSound()
####sound_obj.make_pitches()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.make_turn(-1)
    if keys[pygame.K_LEFT]:
        player.make_turn(1)
    if keys[pygame.K_UP]:
        road.scroll_speed = 0.1 # Player speed = road scrolling speed
        current_pitch += 1 
    if keys[pygame.K_DOWN]:
        road.scroll_speed = -0.1
        current_pitch -= 1
    new_rect = player.image.get_rect(center=(player.rect.x, player.rect.y))
    
    # Clamp the acceleration value to a reasonable range
    current_pitch = max(0.1, min(current_pitch, 0.3))

    # TODO: Sounds
    #sound_obj.sound_routine(current_pitch)

    # Clear screen
    screen.fill("darkgreen")

    road_objects_list.update()
    vehicle_sprites_list.update(road_y, road.scroll_speed)
    obstacle_sprites.update(road.scroll_speed)
    road_y = road.rect.bottom 
    
    #offset = (player.rect.left - road.rect.left, player.rect.top - road.rect.top)

    # Check road end
    if road_y > road.road_length + Cons.player_y_offset:
        running = False
        print("GAME OVER!")
   
    # Check car collision with obstacles
    # TODO: Faster collision check with rectangles
    obstacle_coll = pygame.sprite.groupcollide(obstacle_sprites, vehicle_sprites_list, False, False, pygame.sprite.collide_mask)
    if obstacle_coll:
        print(obstacle_coll)
        for group in obstacle_coll:
            print(group)
            for car in obstacle_coll[group]: 
                print(car)
                car.rotation = 25
                car.rect.x += random.choice([-7, 7])


    # Remove obstacles when they have scrolled out of screen to save time
    # Problem: enemy cars behind won't collide with obstacles
    # Solution: remove when last car has passed obstacle?
    #try:
    #    cur_obs =  obstacle_sprites.sprites()[0]
    #    if cur_obs.rect.y > 1000:
    #        obstacle_sprites.remove(cur_obs)
    #except IndexError:
    #    pass


    # Check if vehicle is on road, else slow down
    # For player must road scroll speed be changed
    on_road = pygame.sprite.spritecollide(road, vehicle_sprites_list, False, pygame.sprite.collide_mask)
    for vehicle in vehicle_sprites_list:
        if vehicle in on_road:
            if isinstance(vehicle, Player):
                road.on_road = True
            else:
                vehicle.on_road = True
        else:
            if isinstance(vehicle, Player):
                road.on_road = False
            else:
                vehicle.on_road = False
    road.check_off_road()

    # Check vehicle collision
    sprites = list(vehicle_sprites_list)
    for i in range(len(sprites)):
        for j in range(i + 1, len(sprites)):
            sprite1 = sprites[i]
            sprite2 = sprites[j]
            if pygame.sprite.collide_mask(sprite1, sprite2):
                
                coords1 = pygame.sprite.collide_mask(sprite1, sprite2)
                
                # If collision, change speed and rotation
                if coords1:
                    if coords1[1] >= 0 and sprite2.rect.top > sprite1.rect.top:
                        sprite1.speed = 0
                        sprite2.speed += 5
                    elif coords1[1] >= 0 and sprite2.rect.top < sprite1.rect.top:
                        sprite1.speed += 10
                        sprite2.speed -= 5
    
                    if coords1[0] >= 0 and sprite2.rect.left > sprite1.rect.left:
                        sprite1.speed = 0
                        sprite1.rotation = 20
                        sprite1.rect.x -= 20
                    elif coords1[1] >= 0 and sprite2.rect.right < sprite1.rect.right:
                        sprite1.speed = 0
                        sprite1.rotation = -20
                        sprite1.rect.x += 20
            
    count += 1

    road_objects_list.draw(screen)
    vehicle_sprites_list.draw(screen)
    obstacle_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()



