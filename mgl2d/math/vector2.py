import math


class Vector2(object):
    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @classmethod
    def from_vector(cls, vector):
        return Vector2(vector.x, vector.y)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalise(self):
        length = math.hypot(self.x, self.y)
        self.x /= length
        self.y /= length

    def angle_to(self, vector):
        angle = (math.atan2(vector.y, vector.x) - math.atan2(self.y, self.x))
        return math.degrees(angle)

    def direction(self):
        length = math.hypot(self.x, self.y)
        return Vector2(self.x / length, self.y / length)

    def dot(self, vector):
        return Vector2(self.x * vector.x, self.y * vector.y)

    def copy(self):
        return Vector2(self.x, self.y)

    def to_list(self):
        return [self.x, self.y]

    def to_tuple(self):
        return self.x, self.y

    def to_string(self):
        return f'{self.x}, {self.y}'

    def __eq__(self, vector):
        return self.x == vector.x and self.y == vector.y

    def __cmp__(self, vector):
        return self.__eq__(vector)

    def __ne__(self, vector):
        return not self.__eq__(vector)

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def __div__(self, value):
        return Vector2(self.x / value, self.y / value)

    __truediv__ = __div__

    def __mul__(self, value):
        return Vector2(self.x * value, self.y * value)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __str__(self):
        return '(%.1f,%.1f)' % (self.x, self.y)

    def __repr__(self):
        return str(self)
