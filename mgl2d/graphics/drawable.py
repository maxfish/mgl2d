from mgl2d.math import Matrix4
from mgl2d.math import Vector2


class Drawable:
    # __slots__ = (
    #     '_pos', '_angle', '_scale', '_m_translation', '_m_rotation', '_m_scale', '_m_transform', '_is_transform_invalid'
    # )

    def __init__(self, x=0.0, y=0.0, scale_x=1, scale_y=1, angle=0):
        self._pos = Vector2(x, y)
        self._angle = angle
        self._scale = Vector2(scale_x, scale_y)
        self._texture = None
        self._shader = None
        self._flip_x = False
        self._flip_y = False

        self._m_translation = self._m_rotation = self._m_scale = None
        self._m_transform = None
        self._is_transform_invalid = True
        self._rebuild_matrices()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._m_translation = Matrix4.translate(self._pos.x, self._pos.y, 0)
        self._is_transform_invalid = True

    @property
    def translation_matrix(self):
        return self._m_translation

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self._m_rotation = Matrix4.rotate(self._angle)
        self._is_transform_invalid = True

    @property
    def rotation_matrix(self):
        return self._m_rotation

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
    def scaling_matrix(self):
        return self._m_scale

    def scale_from_texture(self):
        self.scale = Vector2(self._texture.width, self._texture.height)

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
    def transform_matrix(self):
        if self._is_transform_invalid:
            self._compute_transform()
        return self._m_transform

    def _rebuild_matrices(self):
        self._m_translation = Matrix4.translate(self._pos.x, self._pos.y, 0)
        self._m_rotation = Matrix4.rotate(self._angle)
        self._m_scale = Matrix4.scale(self._scale.x, self._scale.y, 1)

    def _compute_transform(self):
        self._m_transform = self._m_translation * self._m_rotation * self._m_scale

    def invalidate_matrices(self):
        self._is_transform_invalid = True

    def draw(self, screen):
        raise NotImplementedError("Implement this method in the subclasses")
