from cons import Cons
import pygame
import random


class RoadSprite(pygame.sprite.Sprite):
    def __init__(self, height, width):
        super().__init__()
        # Line parameters
        self.screen_width = width
        self.road_width = 300
        self.road_length_multiplier = 20  # How many screen heights the road length will be
        self.road_length = height * self.road_length_multiplier
        self.surface_height = height * self.road_length / 1000
        self.line_thickness = 3
        self.line_start = pygame.Vector2(self.screen_width / 2, self.surface_height - self.line_thickness // 2)
        self.line_direction = pygame.Vector2(-1, 0)  # Initially pointing horizontally 

        self.on_road = True 

        # Movement parameters
        self.move_up_distance = 200
        self.current_move_up = 0
        self.angle_change = 45
        self.current_angle = 0
        self.angle_change_step = -0.5  # Speed of angle change
        self.speed = 2  # Speed of vertical and angled movement
        self.move_direction = pygame.Vector2(0, 1)
        self.move_angle = 0
        self.move_angle_step = -0.5
        self.target_angle = 0

        self.run_test = False

        self.points = []
        self.coords_start = []
        self.coords_end = []
        self.move_vector = pygame.Vector2(0, -self.speed)

        self.line_surface = pygame.Surface([self.screen_width, self.surface_height], pygame.SRCALPHA)
        self.image = self.line_surface

        self.final_start = {}
        self.final_end = {}

        self.straight_length = 200
        self.going_border_correction = 0
        self._scroll_speed = 5
        self.max_speed = 14
        self.road_center_points = {}
        self.draw_road()

        self.mask = pygame.mask.from_surface(self.line_surface)
        
        # Test masking with outline
        self.olist = self.mask.outline()  # For testing of masking
        pygame.draw.lines(self.line_surface, (158,201,158), False, list(self.olist))
        self.rect = self.image.get_rect()

    @property
    def scroll_speed(self):
        return self._scroll_speed

    @scroll_speed.setter
    def scroll_speed(self, change):
        self._scroll_speed += change
        if self._scroll_speed > self.max_speed:
            self._scroll_speed = self.max_speed
        elif self._scroll_speed < 1:
            self._scroll_speed = 1

    def check_off_road(self):
        if not self.on_road and self._scroll_speed > 3:
            self._scroll_speed -= 1


    def fill_y(self, coords):
        # Fill missing y-coords
        # Look how big cap there is between two coords
        # Calculate size of x-coord step in order to have smooth change
        # Example: Y: 1001, 1004; X: 500, 502
        # X-step will be 3/(1+1) = 1.5
        index = 0
        while index < len(coords) - 1:
            index += 1

            prev_y = coords[index - 1][1]
            cur_y = coords[index][1]
            prev_x = coords[index - 1][0]
            cur_x = coords[index][0]
            steps_needed = cur_y - prev_y - 1 

            if steps_needed > 0:
                x_step = (cur_x - prev_x) / (steps_needed + 1)
                for i in range(1, steps_needed + 1):
                    coords.insert(index, [int(coords[index - 1][0] + x_step), prev_y + i] )
                    index += 1
        return coords

    # Currently not in use
    def fill_y_dict(self, stuff):
        #coords = copy.deepcopy(stuff)
        coords = dict(sorted(stuff.items()))
        min_y = min(list(coords.keys()))
        max_y = max(list(coords.keys()))
        prev_y = min_y

        for y in range(min_y + 1, max_y + 1):
            try:
                if not coords[y]:
                    continue

                prev_x = coords[prev_y] 
                
                steps_needed = y - prev_y - 1

                if steps_needed > 0:
                    x_step = (coords[y] - prev_x) / steps_needed
                    for count, i in enumerate(range(prev_y + 1, prev_y + steps_needed + 1)):
                        coords[i] = prev_x + (x_step * count)
                prev_y = y
            except KeyError:
                pass
        coords = dict(sorted(coords.items()))
        return coords

    def change_angle(self, angle, angle_change_step, move_angle_step):
        # Change direction by rotating the virtual angle
        print("target_angle at change: ", self.target_angle, "current angle: ", self.current_angle, angle_change_step)
        if self.target_angle != self.current_angle:
            self.current_angle += angle_change_step

            # Clamp the angle to avoid exceeding the allowed range
            self.current_angle = max(min(self.current_angle, 45), -45)

            # Rotate the direction vector clockwise
            self.line_direction = self.line_direction.rotate(angle_change_step)  
            self.move_angle -= move_angle_step
            self.move_direction = self.move_direction.rotate(move_angle_step)

        print("direction", self.line_direction, "line_direction", self.line_direction)

        # Move line in the new direction
        self.move_vector = self.move_direction * self.speed
        self.line_start -= self.move_vector 
        self.current_move_up += int(self.speed)
        print("at change start x: ", self.line_start.x, "end X", self.line_end.x, "move vector", self.move_vector)

    def check_borders(self):
        # Check that road lines are not crossing screen width limits
        # Don't do normal angle changes when correction is going on
        if self.going_border_correction > 0:
            self.going_border_correction -= 1
            print("corr step: ", self.step, "X", self.line_start.x, self.line_end.x)
            return

        # Left side of the screen
        if self.line_end.x < 400: #self.road_width + 400: #self.screen_width / 4: # 400:
            print("\nPREV ANGLE: ", self.prev_angle)
            print("\nCHECK LEFT", self.current_move_up, ":",  self.line_end.x, self.angles, self.changes)
            
            # Add new correction angle to directions
            self.angles.insert(0, 45)
            # How many cycles border correction lasts
            self.going_border_correction = 300

            # Increase change points to make room for this angle correction
            # Otherwise the next ordinary angle change will start too soon
            for i in range(0, len(self.changes)):
                self.changes[i] += self.going_border_correction + 350

            self.changes.insert(0, self.current_move_up + 1)
            print("\n", self.angles, self.changes)
            print("step: ", self.step)
            print("Correcction left")

        # Right side
        elif self.line_start.x > self.screen_width -400: #- self.road_width - 150: # self.screen_width / 4: # 1400:
            print("\nPREV ANGLE: ", self.prev_angle)
            print("CHECK RIGHT", self.current_move_up, ":",  self.line_start.x, self.angles, self.changes)
            self.angles.insert(0, -25)
            self.going_border_correction = 200            

            for i in range(0, len(self.changes)):
                self.changes[i] += self.going_border_correction + 350

            self.changes.insert(0, self.current_move_up + 1)
            print("\n", self.angles, self.changes)
            print("step: ", self.step)
            print("Correction right")



    def make_directions(self):
        # Must have initial values
        self.changes = [200]  # At which y-coords each each turn shall be
        self.angles = [0]  # Angles for all turns
        amount_turns = int(self.road_length / Cons.height * 3)

        # Make distances between turn points
        for i in range(amount_turns):
            change = random.randrange(250, 700) + self.changes[i]
            if change < self.road_length - 2000:
                self.changes.append(change)
            else:
                break
        self.changes.append(self.changes[-1] + 500)

        # Make angle changes
        for i in range(len(self.changes) - 1):
            nr = random.randrange(-25, 25, 5)
            try:
                while nr == self.angles[-1]:
                    nr = random.randrange(-25, 25)
            except IndexError:
                pass

            self.angles.append(nr)
        # End with 0 angle
        self.angles.append(0)

        self.prev_angle = 0
        self.step = 0
        print(self.angles, self.changes, self.road_length)
        print(len(self.angles), len(self.changes))

    def draw_road(self):
        # Road is first drawn virtually
        # A vector makes a route according to directions
        # Start/end coordinates of the vector are registered are registered in each position
        # After that missing coords are filled
        # Drawing is made with horizontal lines connecting start/end coordinates

        self.make_directions()
        while self.current_move_up < self.road_length:
            
            # Move straight up at start
            if self.current_move_up < 200:
                self.move_vector.y = -self.speed
                self.line_start += self.move_vector
                self.current_move_up += int(self.speed)   # Was no int

            else:
                self.check_borders()
                try:
                    # Pick new angle change
                    if self.current_move_up >= self.changes[0]:
                        print("Step at draw before change", self.step)
                        # Choose direction of steps
                        if self.prev_angle < self.angles[0]: 
                            self.step = 0.25
                        elif self.prev_angle > self.angles[0]:
                            self.step = -0.25

                        self.target_angle = self.angles[0]
                        self.changes.pop(0)
                        self.prev_angle = self.angles.pop(0)
                except IndexError as err:
                    print("IndexError at draw", err) 
               
                # Example: cur angle -25 and prev -10
                # Direction must be corrected in such situations
                if self.current_angle > self.target_angle:
                    self.step = -0.25
                elif self.current_angle < self.target_angle:
                    self.step = 0.25
                self.change_angle(self.target_angle, self.step, self.step)

            # Calculate the end point of the line, end means the left side of the road
            self.line_end = self.line_start - self.line_direction * self.road_width
          
            # For testing if border check works in every situation
            if self.line_end.x < 0 or self.line_start.x > Cons.width:
                print("\n\n", self.changes, self.angles, self.line_start, self.line_end, self.prev_angle, self.current_move_up, self.current_angle)
                print("step", self.step)
                self.run_test = True
                raise

            self.coords_start.append( [int(self.line_start.x), int(self.line_start.y) ])
            self.coords_end.append( [int(self.line_end.x), int(self.line_end.y)] ) 

            # Currently not in use
            self.final_start[int(self.line_start.y)] = int(self.line_start.x)
            self.final_end[int(self.line_end.y)] = int(self.line_end.x)

        ###############
        
        # Sort and fill missing y-coordinates
        self.coords_start.sort(key=lambda x: x[1])
        self.coords_end.sort(key=lambda x: x[1])

        self.coords_start = self.fill_y(self.coords_start)
        self.coords_end = self.fill_y(self.coords_end)

        # Not needed
        self.final_start = self.fill_y_dict(self.final_start)
        self.final_end = self.fill_y_dict(self.final_end)

        def remove_duplicates(item):
            prev = 0
            idx = 0
            try:
                while True:
                    if item[idx][1] == prev:
                        item.pop(idx)
                    else:
                        prev = item[idx][1]
                        idx += 1
            except IndexError:
                return item

        self.coords_end = remove_duplicates(self.coords_end)
        self.coords_start = remove_duplicates(self.coords_start)

        # Testing
        self.final_start = {}
        self.final_end = {}
        for elem in self.coords_start:
            self.final_start[elem[1]] = elem[0]
        for elem in self.coords_end:
            self.final_end[elem[1]] = elem[0]


        start = self.coords_start[0][1]
        end = self.coords_end[0][1]
        diff = start - end

        # Adjust lists so that they start from the same y-coord
        # Because of vector drawing they don't start from same coords
        temp_list = []
        if diff > 0:
            for e in self.coords_end:
                if e[1] < start:
                    temp_list.append(e)
            for elem in temp_list:
                self.coords_end.remove(elem)
        elif diff < 0:
            for e in self.coords_start:
                if e[1] < end:
                    temp_list.append(e)
            for e in temp_list:
                self.coords_start.remove(e)

        # Draw lines between start and end coordinates
        for start, end in zip(self.coords_start, self.coords_end):
            pygame.draw.aaline(self.line_surface, "gray", (start[0], start[1]), (end[0], end[1]))
            self.road_center_points[-start[1] + ((self.road_length_multiplier) * Cons.height + Cons.height -2)] = int( start[0] - ((start[0] - end[0]) / 2) )

    def move(self):
        self.check_off_road()
        self.rect.y += self._scroll_speed

    # Not in use, calculates available space for obstacles
    def get_obstacle_space(self, y, height):
        start1 = int(self.final_start[y])
        end1 = int(self.final_end[y])
        start2 = int(self.final_start[y + height])
        end2 = int(self.final_end[y + height])
        max_start = min([start1, start2])
        max_end = max([end1, end2])
        return (max_start, max_end)

    def update(self):
        self.move()

        

