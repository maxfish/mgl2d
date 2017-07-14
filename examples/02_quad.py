#!/usr/bin/env python
import logging

from mgl2d.app import App
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

logging.basicConfig(level=logging.INFO)

app = App()
screen = Screen(800, 600, 'Quad drawable')
screen.print_info()

# Textured quad centered
quad = QuadDrawable(400, 300, 200, 200)
quad.texture = Texture.load_from_file('data/texture.png')
quad.anchor = Vector2(100, 100)


def draw_frame(screen):
    quad.draw(screen)


def update_frame(delta_ms):
    quad.angle += 0.1
    pass


app.run(screen, draw_frame, update_frame)
