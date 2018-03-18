import numpy as np
from OpenGL.GL import *

from mgl2d.graphics.shader import Shader


class Shapes:
    def __init__(self):
        self._setup_lines()

    def draw_line(self, screen, x1, y1, x2, y2, color):
        self._line_shader.bind()
        self._line_shader.set_uniform_matrix4('projection', screen.projection_matrix.m)
        self._line_shader.set_uniform_2f('p1', x1, y1)
        self._line_shader.set_uniform_2f('p2', x2, y2)
        self._line_shader.set_uniform_4f('color', color.r, color.g, color.b, color.a)
        glBindVertexArray(self._lines_vao)
        glDrawArrays(GL_LINES, 0, 2)
        glBindVertexArray(0)

    def draw_polygon(self, screen, vertices, color):
        for i in range(0, len(vertices)):
            self.draw_line(screen, int(vertices[i][0]), int(vertices[i][1]), int(vertices[(i + 1) % len(vertices)][0]),
                           int(vertices[(i + 1) % len(vertices)][1]), color)

    def _setup_lines(self):
        self._lines_vao = glGenVertexArrays(1)
        glBindVertexArray(self._lines_vao)
        self._lines_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._lines_vbo)
        self._lines_vertices = np.array([0, 0, 1, 1], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self._lines_vertices.nbytes, self._lines_vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindVertexArray(0)

        vertex_shader = """
        #version 330 core

        uniform mat4 projection;
        uniform vec2 p1;
        uniform vec2 p2;

        void main() {
            if(gl_VertexID==0) {
                gl_Position = projection * vec4(p1, 0, 1);
            } else if (gl_VertexID==1) {
                gl_Position = projection * vec4(p2, 0, 1);
            }
        }
        """

        fragment_shader = """
        #version 330 core

        uniform vec4 color;
        out vec4 fragment;

        void main() {
            fragment = color;
        }
        """

        self._line_shader = Shader(vertex_shader, fragment_shader)
