#!/usr/bin/env python

from mgl2d.app import App
from mgl2d.graphics.post_processing_step import PostProcessingStep
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.screen import Screen
from mgl2d.graphics.shader import Shader
from mgl2d.graphics.texture import Texture

app = App()
main_screen = Screen(800, 600, 'Post processing')
main_screen.print_info()

# Textured quad centered
quad = QuadDrawable(400, 300, 200, 200)
quad.texture = Texture.load_from_file('data/texture.png')
quad.anchor_to_center()

# A couple of simple postprocessing steps
# 1. makes the graphics gray
step1 = PostProcessingStep(main_screen.width, main_screen.height)
step1.drawable.shader = Shader.from_files('data/base.vert', 'data/grayscale.frag')
main_screen.add_postprocessing_step(step1)
# 2. apply an old-style scan line effect
step2 = PostProcessingStep(main_screen.width, main_screen.height)
step2.drawable.shader = Shader.from_files('data/base.vert', 'data/scanline.frag')
main_screen.add_postprocessing_step(step2)


def draw_frame(screen):
    quad.draw(screen)


def update_frame(delta_ms):
    quad.angle += 0.1


app.run(main_screen, draw_frame, update_frame)
