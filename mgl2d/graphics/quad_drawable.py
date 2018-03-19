import numpy as np
from OpenGL.GL import *

from mgl2d.graphics.shader import Shader
from mgl2d.math.matrix4 import Matrix4
from mgl2d.math.vector2 import Vector2


class QuadDrawable:
    _default_shader = None

    def __init__(self, pos_x=0.0, pos_y=0.0, size_x=100, size_y=100, scale_x=1, scale_y=1, angle=0):
        self._pos = Vector2(pos_x, pos_y)
        # Size in pixels of the quad
        self._size = Vector2(size_x, size_y)
        # Anchor point
        self._anchor = Vector2(0, 0)
        # Angle to rotate around the anchor (degrees)
        self._angle = angle
        # Scale to apply to the drawable (1.0 == 100%)
        self._scale = Vector2(scale_x, scale_y)
        # Defines if the texture is flipped horizontally
        self._flip_x = False
        # Defines if the texture is flipped vertically
        self._flip_y = False
        self._texture = None
        self._shader = None

        self._m_translation = None
        self._m_size = None
        self._m_rotation = None
        self._m_scale = None
        self._m_anchor = None
        self._m_transform = None
        self._is_transform_invalid = True
        self._rebuild_matrices()

        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)

        # Vertices
        self._vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        self._vertices = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

        # Texture coordinates
        self._vbo_uvs = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo_uvs)
        self._texture_coordinates = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self._texture_coordinates.nbytes, self._texture_coordinates, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

        glBindVertexArray(0)
        if self._default_shader is None:
            self._setup_default_shader()
        self.shader = self._default_shader

    def size_from_texture(self):
        self.size = Vector2(self._texture.width, self._texture.height)

    def invalidate_matrices(self):
        self._is_transform_invalid = True

    def anchor_to_center(self):
        self.anchor = self.size / 2

    def scale_to_texture_size(self):
        self.scale = self.texture.size

    def draw(self, screen):
        if self._texture is not None:
            self._texture.bind()

        if self._shader is not None:
            self._shader.bind()
            self._shader.set_uniform_matrix4('model', self.transform_matrix.m)
            self._shader.set_uniform_matrix4('projection', screen.projection_matrix.m)

        glBindVertexArray(self._vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self._vertices))
        glBindVertexArray(0)

        if self._texture is not None:
            self._texture.unbind()

        if self._shader is not None:
            self._shader.unbind()

    # Properties
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._m_translation = Matrix4.translate(self._pos.x, self._pos.y, 0)
        self._is_transform_invalid = True

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, vector2):
        self._anchor = vector2
        self._m_anchor = Matrix4.translate(-self._anchor.x, -self._anchor.y, 0)
        self._is_transform_invalid = True

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._m_size = Matrix4.scale(self._size.x, self._size.y, 1)
        self._is_transform_invalid = True

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self._m_rotation = Matrix4.rotate(self._angle)
        self._is_transform_invalid = True

    @property
    def flip_x(self):
        return self._flip_x

    @flip_x.setter
    def flip_x(self, value):
        self._flip_x = value
        self.scale = self._scale

    @property
    def flip_y(self):
        return self._flip_y

    @flip_y.setter
    def flip_y(self, value):
        self._flip_y = value
        self.scale = self._scale

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        flip_x = -1 if self._flip_x else 1
        flip_y = -1 if self._flip_y else 1
        self._m_scale = Matrix4.scale(self._scale.x * flip_x, self._scale.y * flip_y, 1)
        self._is_transform_invalid = True

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, texture):
        self._texture = texture

    @property
    def shader(self):
        return self._shader

    @shader.setter
    def shader(self, shader):
        self._shader = shader

    @property
    def translation_matrix(self):
        return self._m_translation

    @property
    def rotation_matrix(self):
        return self._m_rotation

    @property
    def scaling_matrix(self):
        return self._m_scale

    @property
    def transform_matrix(self):
        if self._is_transform_invalid:
            self._compute_transform()
        return self._m_transform

    # Private methods
    def _rebuild_matrices(self):
        self._m_translation = Matrix4.translate(self._pos.x, self._pos.y, 0)
        self._m_size = Matrix4.scale(self._size.x, self._size.y, 1)
        self._m_anchor = Matrix4.translate(-self._anchor.x, -self._anchor.y, 0)
        self._m_rotation = Matrix4.rotate(self._angle)
        self._m_scale = Matrix4.scale(self._scale.x, self._scale.y, 1)

    def _compute_transform(self):
        self._m_transform = self._m_translation * self._m_rotation * self._m_scale * self._m_anchor * self._m_size
        self._is_transform_invalid = False

    def _setup_default_shader(self):
        vertex_shader = """
        #version 330 core

        uniform mat4 model;
        uniform mat4 projection;

        layout(location=0) in vec2 vertex;
        layout(location=1) in vec2 uv;

        out vec2 uv_out;

        void main() {
            vec4 vertex_world = model * vec4(vertex, 1, 1);
            gl_Position = projection * vertex_world;
            uv_out = uv;
        }
        """

        fragment_shader = """
        #version 330 core

        in vec2 uv_out;
        out vec4 color;

        uniform sampler2D tex;

        void main() {
            color = texture(tex, uv_out);
        }
        """

        self._default_shader = Shader(vertex_shader, fragment_shader)
