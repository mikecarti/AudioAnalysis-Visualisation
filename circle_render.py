import random

import pygame as pg
import random
import math

FULL_CIRCLE = 6


class Circle():
    def __init__(self, position, max_x, max_y, angle_in_rad):
        self.x = position[0]
        self.y = position[1]
        self.h_velocity = 0
        self.v_velocity = 0
        self.inner_color = (0, 0, 0)

        self.max_x = max_x
        self.max_y = max_y
        self.h_coef = math.cos(angle_in_rad)
        self.v_coef = math.sin(angle_in_rad)

    def set_velocity(self, horizontal, vertical):
        # velocity is a number between -1 and 1
        self.h_velocity = horizontal
        self.v_velocity = vertical

    def move(self):
        self.x = self.x + self.h_velocity * self.h_coef
        self.y = self.y + self.v_velocity * self.v_coef

        # if self.x > self.max_x:
        #     self.x = 0
        # if self.y > self.max_y:
        #     self.y = 0
        # if self.x < 0:
        #     self.x = self.max_x
        # if self.y < 0:
        #     self.y = self.max_y
        if self.x > self.max_x:
            self.h_coef = - self.h_coef
        if self.y > self.max_y:
            self.v_coef = - self.v_coef
        if self.x < 0:
            self.h_coef = - self.h_coef
        if self.y < 0:
            self.v_coef = - self.v_coef
        return int(self.x), int(self.y)


class Texter:
    def __init__(self, texts, screen):
        pg.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.font = pg.freetype.SysFont('Comic Sans MS', 15)
        self.texts = texts
        self.screen = screen

    def update_text_position(self, n, new_pos):
        text = self.texts[n]
        self.font.render_to(self.screen, new_pos, text, (255, 255, 255))


class Renderer:
    def __init__(self, n_of_objects, file_names):
        pg.init()
        self.global_width = 500
        self.global_height = 500
        self.screen = pg.display.set_mode((self.global_width, self.global_height))

        self.screen_color = (0, 0, 0)
        self.circle_color = (255, 0, 255)
        self.texter = Texter(file_names, self.screen)
        self.circle_radius = 30

        self.objects = []
        self.create_circles(n=n_of_objects)

    def update(self):
        pg.display.update()

    def prepare_screen(self):
        self.screen.fill(self.screen_color)

    def create_circles(self, n):
        for _ in range(n):
            pos = (random.randint(0, self.global_width), random.randint(0, self.global_height))
            circle = Circle(pos, max_x=self.global_width, max_y=self.global_height,
                            angle_in_rad=random.randrange(0, FULL_CIRCLE))
            self.objects.append(circle)
            pg.draw.circle(self.screen, self.circle_color, pos, self.circle_radius, 1)
        self.update()

    def move_object(self, speed, color, object_number):
        circle = self.objects[object_number]
        circle.set_velocity(speed, speed)
        new_circle_pos = circle.move()
        pg.draw.circle(self.screen, color, new_circle_pos, 30)
        new_text_pos = (new_circle_pos[0] + self.circle_radius, new_circle_pos[1] - self.circle_radius)
        self.texter.update_text_position(object_number, new_text_pos)
