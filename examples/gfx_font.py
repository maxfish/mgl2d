#!/usr/bin/env python
import math

from mgl2d.app import App
from mgl2d.graphics.font import Font
from mgl2d.graphics.screen import Screen

app = App()
main_screen = Screen(800, 600, 'Font example')
main_screen.print_info()

font = Font()
font.load_bmfont_file('data/prosto_one_64.txt')
font.load_bmfont_file('data/prosto_one_16.txt')


def draw_frame(screen):
    font.draw_string(screen, 64, 'A big text...', 100, 150)
    font.draw_string(screen, 64, 'A smaller text', 160, 250, scale=0.7)
    font.draw_string(screen, 16, 'font: Prosto One // public domain', 30, 550)


def update_frame(delta_ms):
    return


app.run(main_screen, draw_frame, update_frame)
