from pathlib import Path

from OpenGL.GL import *


class Shader(object):
    def __init__(self, vertex_shader_src, fragment_shader_src):
        self._uniforms = {}
        self.program_id = glCreateProgram()

        vs_id = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs_id, vertex_shader_src)
        glCompileShader(vs_id)
        glAttachShader(self.program_id, vs_id)

        fs_id = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs_id, fragment_shader_src)
        glCompileShader(fs_id)
        glAttachShader(self.program_id, fs_id)

        glLinkProgram(self.program_id)

        glDetachShader(self.program_id, vs_id)
        glDeleteShader(vs_id)
        glDetachShader(self.program_id, fs_id)
        glDeleteShader(fs_id)

    @staticmethod
    def from_files(vert_file, frag_file):
        vert_source = Path(vert_file).read_text()
        frag_source = Path(frag_file).read_text()
        return Shader(vert_source, frag_source)

    def bind(self):
        glUseProgram(self.program_id)

    def unbind(self):
        glUseProgram(0)

    def get_uniform(self, name):
        uniform = self._uniforms.get(name)
        if not uniform:
            uniform = glGetUniformLocation(self.program_id, name)
            self._uniforms[name] = uniform

        return uniform

    def set_uniform_matrix4(self, name, matrix):
        uniform = self.get_uniform(name)
        glUniformMatrix4fv(uniform, 1, GL_FALSE, matrix)

    def set_uniform_float(self, name, value):
        uniform = self.get_uniform(name)
        glUniform1f(uniform, value)
