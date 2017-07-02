import math

import numpy


class Matrix4(object):
    __slots__ = ('m')

    def __init__(self, m=None):
        self.m = m
        if self.m is None:
            self.m = numpy.array([
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1
            ], dtype=numpy.float32)

    @staticmethod
    def translate(x, y, z):
        m = numpy.array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            x, y, z, 1
        ], dtype=numpy.float32)
        return Matrix4(m)

    @staticmethod
    def scale(x, y, z):
        m = numpy.array([
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1
        ], dtype=numpy.float32)
        return Matrix4(m)

    @staticmethod
    def rotate(degree):
        z_sin = math.sin(math.radians(degree))
        z_cos = math.cos(math.radians(degree))
        m = numpy.array([
            z_cos, z_sin, 0, 0,
            -z_sin, z_cos, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ], dtype=numpy.float32)
        return Matrix4(m)

    def __mul__(self, other):
        a = self.m
        b = other.m
        m00 = a[0] * b[0] + a[4] * b[1] + a[8] * b[2] + a[12] * b[3]
        m01 = a[1] * b[0] + a[5] * b[1] + a[9] * b[2] + a[13] * b[3]
        m02 = a[2] * b[0] + a[6] * b[1] + a[10] * b[2] + a[14] * b[3]
        m03 = a[3] * b[0] + a[7] * b[1] + a[11] * b[2] + a[15] * b[3]

        m10 = a[0] * b[4] + a[4] * b[5] + a[8] * b[6] + a[12] * b[7]
        m11 = a[1] * b[4] + a[5] * b[5] + a[9] * b[6] + a[13] * b[7]
        m12 = a[2] * b[4] + a[6] * b[5] + a[10] * b[6] + a[14] * b[7]
        m13 = a[3] * b[4] + a[7] * b[5] + a[11] * b[6] + a[15] * b[7]

        m20 = a[0] * b[8] + a[4] * b[9] + a[8] * b[10] + a[12] * b[11]
        m21 = a[1] * b[8] + a[5] * b[9] + a[9] * b[10] + a[13] * b[11]
        m22 = a[2] * b[8] + a[6] * b[9] + a[10] * b[10] + a[14] * b[11]
        m23 = a[3] * b[8] + a[7] * b[9] + a[11] * b[10] + a[15] * b[11]

        m30 = a[0] * b[12] + a[4] * b[13] + a[8] * b[14] + a[12] * b[15]
        m31 = a[1] * b[12] + a[5] * b[13] + a[9] * b[14] + a[13] * b[15]
        m32 = a[2] * b[12] + a[6] * b[13] + a[10] * b[14] + a[14] * b[15]
        m33 = a[3] * b[12] + a[7] * b[13] + a[11] * b[14] + a[15] * b[15]

        m = numpy.array([
            m00, m01, m02, m03,
            m10, m11, m12, m13,
            m20, m21, m22, m23,
            m30, m31, m32, m33
        ], dtype=numpy.float32)

        return Matrix4(m)
