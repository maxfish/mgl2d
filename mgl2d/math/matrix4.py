import math

import numpy

from mgl2d.math.vector2 import Vector2


class Matrix4(object):
    __slots__ = '_m'

    def __init__(self, m=None):
        self._m = m
        if self._m is None:
            self._m = numpy.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ], dtype=numpy.float32)

    @property
    def m(self):
        return self._m

    def set_translate(self, x, y, z):
        self._m[0] = [1, 0, 0, 0]
        self._m[1] = [0, 1, 0, 0]
        self._m[2] = [0, 0, 1, 0]
        self._m[3] = [x, y, z, 1]

    @staticmethod
    def translate(x, y, z):
        return Matrix4(numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]
        ], dtype=numpy.float32))

    def set_scale(self, x, y, z):
        self._m[0] = [x, 0, 0, 0]
        self._m[1] = [0, y, 0, 0]
        self._m[2] = [0, 0, z, 0]
        self._m[3] = [0, 0, 0, 1]

    @staticmethod
    def scale(x, y, z):
        return Matrix4(numpy.array([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32))

    def set_rotate_z(self, radians):
        z_sin = math.sin(radians)
        z_cos = math.cos(radians)
        self._m[0] = [z_cos, z_sin, 0, 0]
        self._m[1] = [-z_sin, z_cos, 0, 0]
        self._m[2] = [0, 0, 1, 0]
        self._m[3] = [0, 0, 0, 1]

    @staticmethod
    def rotate_z(radians):
        z_sin = math.sin(radians)
        z_cos = math.cos(radians)
        return Matrix4(numpy.array([
            [z_cos, z_sin, 0, 0],
            [-z_sin, z_cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float32))

    def __mul__(self, other):
        if isinstance(other, Vector2):
            result = self._m @ other.v
            return Vector2(result[0], result[1])
        elif isinstance(other, Matrix4):
            return Matrix4(other._m @ self._m)
        return None
