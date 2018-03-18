import json
import logging
import os
from collections import OrderedDict

from mgl2d.graphics.texture import Texture
from mgl2d.math.rect import Rect
from mgl2d.math.vector2 import Vector2

logger = logging.getLogger(__name__)


class FramesStore:
    DEFAULT_FPS = 30
    FLAG_FLIP_X = 1
    FLAG_FLIP_Y = 2
    FLAG_LOOP_ANIMATION = 16

    def __init__(self):
        self.images = {}
        self.frames = {}
        self.animations = {}
        self.animation_fps = self.DEFAULT_FPS

    def load(self, path, file_name):
        logger.info("Loading '%s/%s'" % (path, file_name))

        json_data = open(os.path.join(path, file_name))
        data = json.load(json_data)
        json_data.close()

        meta = data.get('meta')
        if meta:
            fps = meta.get('fps')
            if fps:
                self.animation_fps = fps

        for animation_name in data['animations']:
            animation_data = data['animations'][animation_name]
            # Check if this is a clone of another one
            clone_of = animation_data.get('clone_of')
            if clone_of:
                animation_data = data['animations'][clone_of]
                animation_data['clone_of'] = clone_of
            self.animations[animation_name] = Animation(animation_data, animation_name)

        # Load images and frames
        for frame_name in data['frames']:
            frame = data['frames'][frame_name]
            if not frame['image_file'] in self.images:
                self.images[frame['image_file']] = frame['image'] = Texture.load_from_file(
                    os.path.join(path, frame['image_file']))
                self.frames[frame_name] = Frame(frame, frame_name)

    def get_frame(self, frame_name):
        return self.frames[frame_name]

    def get_animation(self, animation_name):
        return self.animations[animation_name]

    def get_animations(self):
        return self.animations

    def to_dictionary(self):
        d = OrderedDict()
        d['animations'] = {}
        for a_name in self.animations.keys():
            a = self.animations[a_name]
            d['animations'][a.name] = a.to_dictionary()
        d['frames'] = {}
        for f_name in self.frames:
            f = self.frames[f_name]
            d['frames'][f.name] = f.to_dictionary()
        return d


class Frame:
    def __init__(self, data, frame_name):
        self.name = frame_name
        self.image_file = data['image_file']
        self.image = data['image']

        anchor = data.get('anchor')
        if anchor:
            self.anchor = Vector2(anchor['x'], anchor['y'])
        else:
            self.anchor = Vector2(0, 0)

        rect = data.get('rect')
        if rect:
            self.rect = Rect(rect['x'], rect['y'], rect['width'], rect['height'])
        else:
            self.rect = Rect(0, 0, self.image.width, self.image.height)

        attack_box = data.get('attack_box')
        if attack_box:
            if attack_box['width'] < 0:
                attack_box['x'] += attack_box['width']
                attack_box['width'] = -attack_box['width']
            if attack_box['height'] < 0:
                attack_box['y'] += attack_box['height']
                attack_box['height'] = -attack_box['height']

            self.attack_box = Rect(attack_box['x'], attack_box['y'], attack_box['width'], attack_box['height'])
        else:
            self.attack_box = None

        hit_box = data.get('hit_box')
        if hit_box:
            if hit_box['width'] < 0:
                hit_box['x'] += hit_box['width']
                hit_box['width'] = -hit_box['width']
            if hit_box['height'] < 0:
                hit_box['y'] += hit_box['height']
                hit_box['height'] = -hit_box['height']

            self.hit_box = Rect(hit_box['x'], hit_box['y'], hit_box['width'], hit_box['height'])
        else:
            self.hit_box = Rect(0, 0, 0, 0)

    def to_dictionary(self):
        d = OrderedDict()

        d['anchor'] = OrderedDict()
        d['anchor']['x'] = self.anchor.x
        d['anchor']['y'] = self.anchor.y

        if not (self.rect.x == self.rect.y == 0 and self.rect.w == self.image.width
                and self.rect.h == self.image.height):
            # Save the rect only if it is different from the whole image
            d['rect'] = OrderedDict()
            d['rect']['x'] = self.rect.x
            d['rect']['y'] = self.rect.y
            d['rect']['width'] = self.rect.w
            d['rect']['height'] = self.rect.h
        if self.hit_box and self.hit_box.w != 0 and self.hit_box.h != 0:
            d['hit_box'] = OrderedDict()
            d['hit_box']['x'] = self.hit_box.x
            d['hit_box']['y'] = self.hit_box.y
            d['hit_box']['width'] = self.hit_box.w
            d['hit_box']['height'] = self.hit_box.h
        if self.attack_box and self.attack_box.w != 0 and self.attack_box.h != 0:
            d['attack_box'] = OrderedDict()
            d['attack_box']['x'] = self.attack_box.x
            d['attack_box']['y'] = self.attack_box.y
            d['attack_box']['width'] = self.attack_box.w
            d['attack_box']['height'] = self.attack_box.h
        d['image_file'] = self.image_file
        return d


class AnimationFrame:
    def __init__(self, data):
        self.frame_name = data['frame']
        self.flip_x = int(data.get('flip_x', 0))
        self.flip_y = int(data.get('flip_y', 0))
        self.delay = int(data.get('delay', 1))

    def to_dictionary(self):
        d = OrderedDict()
        d['frame'] = self.frame_name
        if self.flip_x == 1:
            d['flip_x'] = 1
        if self.flip_y == 1:
            d['flip_y'] = 1
        if self.delay > 1:
            d['delay'] = self.delay
        return d


class Animation:
    def __init__(self, data, name):
        self.name = name
        self.clone_of = data.get('clone_of')
        self.frames = []
        if data.get('frames'):
            for frame in data['frames']:
                self.frames.append(AnimationFrame(frame))

    def to_dictionary(self):
        d = OrderedDict()
        if self.clone_of:
            d['clone_of'] = self.clone_of
        else:
            d['frames'] = [f.to_dictionary() for f in self.frames]
        return d
