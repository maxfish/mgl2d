import numpy as np
from OpenGL.GL import *

from mgl2d.graphics import Drawable
from mgl2d.graphics import Shader
from mgl2d.math.matrix4 import Matrix4
from mgl2d.math.vector2 import Vector2


class QuadDrawable(Drawable):
    _default_shader = None

    def __init__(self, x=0.0, y=0.0, scale_x=1, scale_y=1, angle=0):
        super().__init__(x=x, y=y, scale_x=scale_x, scale_y=scale_y, angle=angle)
        self._anchor = Vector2(0, 0)
        self._m_anchor = Matrix4()

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
        self._texture_coords = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self._texture_coords.nbytes, self._texture_coords, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

        glBindVertexArray(0)
        if self._default_shader is None:
            self._setup_default_shader()
        self.shader = self._default_shader

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, vector2):
        self._anchor = vector2
        # Because of the matrices order, the anchor has to be scaled by scale
        self._m_anchor = Matrix4.translate(-self._anchor.x / self.scale.x, -self._anchor.y / self.scale.y, 0)
        self._is_transform_invalid = True

    def anchor_to_center(self):
        self.anchor = self.scale / 2

    def scale_to_texture_size(self):
        self.scale = self.texture.size

    def _compute_transform(self):
        self._m_transform = self._m_translation * self._m_rotation * self._m_scale * self._m_anchor

    def draw(self, screen):
        if self._texture is not None:
            self._texture.bind()

        if self._shader is not None:
            self._shader.bind()
            self._shader.set_uniform_matrix4('model', self.transform_matrix.m)
            self._shader.set_uniform_matrix4('projection', screen.projection_matrix.m)

        glBindVertexArray(self._vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self._vertices))
        glBindVertexArray(0)

        if self._texture is not None:
            self._texture.unbind()

        if self._shader is not None:
            self._shader.unbind()

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
