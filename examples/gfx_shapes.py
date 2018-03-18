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


def draw_frame(screen):
    x1 = random.randint(0, screen.width)
    y1 = random.randint(0, screen.height)
    x2 = random.randint(0, screen.width)
    y2 = random.randint(0, screen.height)

    c = Color()
    c.r = random.random()
    c.g = random.random()
    c.b = random.random()
    c.a = 1

    shapes.draw_line(screen, x1, y1, x2, y2, c)


def update_frame(delta_ms):
    return


app.run(main_screen, draw_frame, update_frame)
