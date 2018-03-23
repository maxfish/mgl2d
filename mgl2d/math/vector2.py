import math

import numpy


class Vector2(object):
    __slots__ = '_v'

    def __init__(self, x=0.0, y=0.0):
        # To simplify the matrices operations the vector has 4 components
        self._v = numpy.array([x, y, 0, 0], dtype=numpy.float)

    @property
    def v(self):
        return self._v

    @property
    def x(self):
        return self._v[0]

    @x.setter
    def x(self, value):
        self._v[0] = value

    @property
    def y(self):
        return self._v[1]

    @y.setter
    def y(self, value):
        self._v[1] = value

    @classmethod
    def from_vector(cls, vector):
        return Vector2(vector.x, vector.y)

    def length(self):
        return math.hypot(self._v[0], self._v[1])

    def normalise(self):
        length = math.hypot(self._v[0], self._v[1])
        self._v[0] /= length
        self._v[1] /= length

    def angle_to(self, vector):
        return math.atan2(vector.y, vector.x) - math.atan2(self._v[1], self._v[0])

    def direction(self):
        length = math.hypot(self._v[0], self._v[1])
        return Vector2(self._v[0] / length, self._v[1] / length)

    def dot(self, vector):
        return Vector2(self._v[0] * vector.x, self._v[1] * vector.y)

    def copy(self):
        return Vector2(self._v[0], self._v[1])

    def to_list(self):
        return self._v[:2]

    def to_tuple(self):
        return self._v[0], self._v[1]

    def to_string(self):
        return f'{self._v[0]}, {self._v[1]}'

    def __eq__(self, vector):
        return self._v[0] == vector.x and self._v[1] == vector.y

    def __cmp__(self, vector):
        return self.__eq__(vector)

    def __ne__(self, vector):
        return not self.__eq__(vector)

    def __add__(self, vector):
        return Vector2(self._v[0] + vector.x, self._v[1] + vector.y)

    def __sub__(self, vector):
        return Vector2(self._v[0] - vector.x, self._v[1] - vector.y)

    def __div__(self, value):
        return Vector2(self._v[0] / value, self._v[1] / value)

    __truediv__ = __div__

    def __mul__(self, value):
        return Vector2(self._v[0] * value, self._v[1] * value)

    def __neg__(self):
        return Vector2(-self._v[0], -self._v[1])

    def __str__(self):
        return '(%.1f,%.1f)' % (self._v[0], self._v[1])

    def __repr__(self):
        return str(self)
