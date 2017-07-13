import logging

import numpy
from OpenGL.GL import *
from PIL import Image

logger = logging.getLogger(__name__)


class Texture(object):
    @classmethod
    def load_from_file(cls, filename, mode=GL_RGBA):
        logger.info('Loading ''%s''' % filename)
        image = Image.open(filename)
        if mode == GL_RGBA:
            image_new = image.convert('RGBA')
            image.close()
            image = image_new

        texture = Texture()
        texture._width = image.size[0]
        texture._height = image.size[1]

        pixels = numpy.array([component for pixel in image.getdata() for component in pixel], dtype=numpy.uint8)
        texture.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture.texture_id)

        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, mode, texture.width, texture.height, 0, mode, GL_UNSIGNED_BYTE, pixels)
        glBindTexture(GL_TEXTURE_2D, 0)

        image.close()
        return texture

    @classmethod
    def create_with_size(cls, width, height, mode=GL_RGBA):
        image = Image.new(mode=mode, size=(width, height))
        pixels = numpy.array([component for pixel in image.getdata() for component in pixel], dtype=numpy.uint8)

        texture = Texture()
        texture._width = width
        texture._height = height
        texture.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture.texture_id)

        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, mode, width, height, 0, mode, GL_UNSIGNED_BYTE, pixels)
        glBindTexture(GL_TEXTURE_2D, 0)

        image.close()
        return texture

    @classmethod
    def create_with_data(cls, width, height, texture_id):
        texture = Texture()
        texture._width = width
        texture._height = height
        texture.texture_id = texture_id
        return texture

    def __init__(self):
        self._width = 0
        self._height = 0
        self.texture_id = 0

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _next_power_of_two(self, n):
        return 2 ** (n - 1).bit_length()
