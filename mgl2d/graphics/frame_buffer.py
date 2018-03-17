import logging

from OpenGL.GL import *

from mgl2d.graphics import Texture

logger = logging.getLogger(__name__)


class FrameBuffer(object):
    def __init__(self, width, height):
        super().__init__()

        self._fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self._fbo)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture_id, 0)
        self._texture = Texture.create_with_data(width, height, texture_id)

        if not glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE:
            logger.error('error binding!')
            exit()

        self._width = width
        self._height = height

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

    @property
    def texture(self):
        return self._texture

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self._fbo)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
