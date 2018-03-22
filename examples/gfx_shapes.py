#!/usr/bin/env python
import random

from mgl2d.app import App
from mgl2d.graphics.color import Color
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.shapes import Shapes

app = App()
main_screen = Screen(800, 600, 'Shapes')
main_screen.print_info()

shapes = Shapes()

line_x1 = line_y1 = line_x2 = line_y2 = 0
center_x = center_y = radius = 0
color = Color()


def get_new_parameters():
    global line_x1, line_x2, line_y1, line_y2, center_x, center_y, radius, color
    color = Color(r=random.random(), g=random.random(), b=random.random(), a=1)

    line_x1 = random.randint(0, main_screen.width)
    line_y1 = random.randint(0, main_screen.height)
    line_x2 = random.randint(0, main_screen.width)
    line_y2 = random.randint(0, main_screen.height)

    center_x = random.randint(0, main_screen.width)
    center_y = random.randint(0, main_screen.height)
    radius = random.randint(10, 150)


def draw_frame(screen):
    # Draws a line
    shapes.draw_line(main_screen, line_x1, line_y1, line_x2, line_y2, color)
    # Draws an polygonal approximation of a circle
    shapes.draw_circle(main_screen, center_x, center_y, radius, color, num_segments=50)
    # 'G'
    shapes.draw_polyline(main_screen, vertices=[
        (60, 20),
        (20, 20),
        (20, 70),
        (60, 70),
        (60, 45),
        (40, 45),
    ], color=color)
    # 'L'
    shapes.draw_polyline(main_screen, vertices=[
        (70, 20),
        (70, 70),
        (110, 70),
    ], color=color)


def update_frame(delta_ms):
    get_new_parameters()


app.run(main_screen, draw_frame, update_frame, fps=2)
