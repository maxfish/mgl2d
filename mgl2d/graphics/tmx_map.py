import logging

from pytmx import pytmx

from mgl2d.graphics.quad_drawable import QuadDrawable
from mgl2d.graphics.texture import Texture
from mgl2d.math.vector2 import Vector2

logger = logging.getLogger(__name__)


class TMXMap(object):
    def __init__(self, filename):
        self._tmx_data = pytmx.TiledMap(filename, invert_y=True, image_loader=self._image_loader)
        self._size = self._tmx_data.width * self._tmx_data.tilewidth, self._tmx_data.height * self._tmx_data.tileheight
        self._layer_offsets = [Vector2(0, 0) for _ in range(0, len(self._tmx_data.layers))]
        self._drawable = QuadDrawable()

    @staticmethod
    def _image_loader(filename, colorkey, **kwargs):
        if colorkey:
            logger.error('colorkey not implemented')

        image = Texture.load_from_file(filename)

        def load_image(rect=None, flags=None):
            if rect:
                try:
                    x, y, w, h = rect
                    y = image.height - y - h
                    tile = image.get_region(x, y, w, h)
                except:
                    logger.error('cannot get region %s of image', rect)
                    raise
            else:
                tile = image

            if flags:
                logger.error('tile flags are not implemented')

            return tile

        return load_image

    @property
    def width_in_pixels(self):
        return self._size[0]

    @property
    def height_in_pixels(self):
        return self._size[1]

    def draw(self, screen):
        self.draw_layers_range(screen, 0, len(self._tmx_data.layers))

    def draw_layers_range(self, screen, start, how_many):
        for index in range(start, start + how_many):
            layer = self._tmx_data.layers[index]
            if layer.visible == 0:
                continue

            offset_x = layer.offsetx + self._layer_offsets[index].x
            offset_y = layer.offsety + self._layer_offsets[index].y

            if isinstance(layer, pytmx.TiledTileLayer):
                # for x, y, image in layer.tiles():
                pass
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if hasattr(obj, 'points'):
                        # draw_lines(poly_color, obj.closed, obj.points, 3)
                        pass
                    elif obj.image:
                        self._drawable.texture = obj.image
                        self._drawable.scale = Vector2(obj.width, obj.height)
                        self._drawable.pos = Vector2(obj.x - offset_x, obj.y - offset_y)
                        self._drawable.draw(screen)

                        # obj.image.blit(obj.x - offset_x, (Gfx.screen_height - obj.y) - offset_y, 0, w, h)
                    else:
                        # draw_rect(rect_color, (obj.x, obj.y, obj.width, obj.height), 3)
                        pass
            elif isinstance(layer, pytmx.TiledImageLayer):
                if layer.image:
                    pass

    def set_layer_offset(self, layer_index, x, y):
        self._layer_offsets[layer_index].x = x
        self._layer_offsets[layer_index].y = y

    def all_objects_as_dict(self, layer_name):
        # Note: there shouldn't be duplicate or missing names
        if layer_name not in self._tmx_data.layernames:
            return {}

        objects = dict()
        layer = self._tmx_data.layernames[layer_name]
        for obj in layer:
            objects[obj.name] = obj

        return objects

    def all_objects_as_list(self, layer_name):
        if layer_name not in self._tmx_data.layernames:
            return []

        return list(self._tmx_data.layernames[layer_name])
