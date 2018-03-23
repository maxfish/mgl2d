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
            ], dtype=numpy.float)

    @property
    def m(self):
        return self._m

    @staticmethod
    def translate(x, y, z):
        return Matrix4(numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1]
        ], dtype=numpy.float))

    @staticmethod
    def scale(x, y, z):
        return Matrix4(numpy.array([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float))

    @staticmethod
    def rotate_z(degree):
        radians = math.radians(degree)
        z_sin = math.sin(radians)
        z_cos = math.cos(radians)
        return Matrix4(numpy.array([
            [z_cos, z_sin, 0, 0],
            [-z_sin, z_cos, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=numpy.float))

    def __mul__(self, other):
        if isinstance(other, Vector2):
            result = self._m @ other.v
            return Vector2(result[0], result[1])
        elif isinstance(other, Matrix4):
            return Matrix4(other._m @ self._m)
        return None
