import logging

import numpy
import sdl2
from OpenGL.GL import *
from sdl2 import video

from mgl2d.math import Rect
from mgl2d.math.matrix4 import Matrix4

logger = logging.getLogger(__name__)


class Screen(object):
    def __init__(self, width, height, title='Window', alpha_blending=True, full_screen=False, gl_major=4, gl_minor=1):
        self._width = width
        self._height = height
        self._aspect_ratio = float(width) / float(height)
        self._viewport = Rect(0, 0, width, height)
        self._full_screen = full_screen

        # Create the window
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            print(sdl2.SDL_GetError())

        self._window = sdl2.SDL_CreateWindow(str.encode(title),
                                             sdl2.SDL_WINDOWPOS_UNDEFINED,
                                             sdl2.SDL_WINDOWPOS_UNDEFINED, width, height,
                                             sdl2.SDL_WINDOW_OPENGL)

        if not self._window:
            print(sdl2.SDL_GetError())
            return

        # Set up OpenGL
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, gl_major)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, gl_minor)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)
        self._context = sdl2.SDL_GL_CreateContext(self._window)
        self._projection_matrix = self._ortho_projection()

        if alpha_blending:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if full_screen:
            self.full_screen = True

        # Post processing steps
        self._pp_steps = []

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def viewport(self):
        return self._viewport

    @property
    def is_opened(self):
        return self._window is not None

    @property
    def projection_matrix(self):
        return self._projection_matrix

    @property
    def full_screen(self):
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value):
        sdl2.SDL_SetWindowFullscreen(self._window, value)

    def _ortho_projection(self):
        z_far = 1.0
        z_near = -1.0

        m = numpy.zeros((4, 4), dtype=numpy.float32)
        m[0, 0] = + 2.0 / self._width
        m[3, 0] = - 1.0
        m[1, 1] = - 2.0 / self._height
        m[3, 1] = + 1.0
        m[2, 2] = - 2.0 / (z_far - z_near)
        m[3, 2] = (z_far + z_near) / (z_near - z_far)
        m[3, 3] = + 1.0

        return Matrix4(m)

    def close(self):
        sdl2.SDL_GL_DeleteContext(self._context)
        self._context = None
        sdl2.SDL_DestroyWindow(self._window)
        self._window = None

    def begin_update(self):
        if len(self._pp_steps) > 0:
            self._pp_steps[0].fbo.bind()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def end_update(self):
        if len(self._pp_steps) > 0:
            if len(self._pp_steps) > 1:
                for x in range(1, len(self._pp_steps)):
                    self._pp_steps[x].fbo.bind()
                    self._pp_steps[x - 1].draw(self)

            self._pp_steps[-1].fbo.unbind()
            self._pp_steps[-1].draw(self)

        sdl2.SDL_GL_SwapWindow(self._window)

    def add_postprocessing_step(self, step):
        self._pp_steps.append(step)

    def print_info(self):
        logger.info('Resolution: %dx%d ratio: %.2f' % (self._width, self._height, self._aspect_ratio))
        logger.info('Rendeer: %s (%s)' % (glGetString(GL_RENDERER), glGetString(GL_VENDOR)))
        logger.info('OpenGL: %s GLSL: %s' % (glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION)))
