#!/usr/bin/env python
from mgl2d.app import App
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.texture import Texture

app = App()
main_screen = Screen(800, 600, 'Quad drawable')
main_screen.print_info()

# Textured quad centered
quad = QuadDrawable(400, 300, 200, 200)
quad.texture = Texture.load_from_file('data/texture.png')
quad.anchor_to_center()


def draw_frame(screen):
    quad.draw(screen)


def update_frame(delta_ms):
    return


app.run(main_screen, draw_frame, update_frame)
