#!/usr/bin/env python
import math

from mgl2d.app import App
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

app = App()
main_screen = Screen(800, 600, 'Quad drawable')
main_screen.print_info()

quads = []
for y in range(3):
    for x in range(4):
        quad = QuadDrawable(100 + x * 200, 100 + y * 200, size_x=120, size_y=120)
        quad.texture = Texture.load_from_file('data/texture.png')
        quad.anchor_to_center()
        quads.append(quad)

# Flipped horizontally
quads[1].flip_x = True
# Flipped vertically
quads[2].flip_y = True
# Flipped in both directions
quads[3].flip_x = quads[3].flip_y = True
# Scaled smaller
quads[4].scale = Vector2(0.8, 0.8)
# Scaled bigger
quads[5].scale = Vector2(1.2, 1.2)
# Rotated 45 degrees
quads[6].angle = 45
# Rotated 22 degrees and scaled to 50%
quads[7].angle = 22
quads[7].scale = Vector2(0.8, 0.8)
# Stretched
quads[8].scale = Vector2(0.5, 1.2)


def draw_frame(screen):
    for q in quads:
        q.draw(screen)


animation_angle = 0
animation_scale = 0


def update_frame(delta_ms):
    global animation_scale, animation_angle
    animation_angle += 0.4
    animation_scale = math.fabs(math.sin(math.radians(animation_angle * 2)))
    quads[9].scale = Vector2(animation_scale, animation_scale)
    quads[10].angle = animation_angle
    quads[11].scale = Vector2(animation_scale, animation_scale)
    quads[11].angle = animation_angle


app.run(main_screen, draw_frame, update_frame)
