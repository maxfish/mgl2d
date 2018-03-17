from mgl2d.graphics import FrameBuffer
from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.math.vector2 import Vector2


class PostProcessingStep(object):
    def __init__(self, width, height, flip_y=True):
        super().__init__()

        self._fbo = FrameBuffer(width, height)
        self._drawable = QuadDrawable()
        self._drawable.scale = Vector2(width, height)
        self._drawable.flip_y = flip_y
        self._drawable.pos = Vector2(0, height)
        self._drawable.invalidate_matrices()
        self._drawable.texture = self._fbo.texture

    def draw(self, screen):
        self._drawable.draw(screen)

    @property
    def fbo(self):
        return self._fbo

    @property
    def drawable(self):
        return self._drawable

    @drawable.setter
    def drawable(self, drawable):
        self._drawable = drawable
