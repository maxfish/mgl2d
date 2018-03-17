from mgl2d.graphics import FramesStore
from mgl2d.graphics import QuadDrawable
from mgl2d.math.vector2 import Vector2


class Sprite:
    DEBUG = False

    def __init__(self, frames_store):
        self._frames_store = frames_store
        self._x = 0
        self._y = 0
        self._flags = 0
        self._angle = 0
        self._scale = Vector2(1, 1)

        # Collision detection
        self._attack_box = None
        self._hit_box = None

        # Frames and animations
        self._frame = None
        self._animation = None
        self._animation_name = None
        self._animation_frame_index = None
        self._animation_frame_delay = 0
        self._animation_speed = 1
        self._animating = False

        # Drawing
        self._drawable = QuadDrawable()

    def draw(self, screen):
        if self._frame is None:
            return

        self._drawable.pos = Vector2(self._x, self._y)  # - camera.offset.x, self._y - camera.offset.y)
        self._drawable.draw(screen)

        # DEBUG boxes
        if Sprite.DEBUG:
            # TODO: !!!
            pass
            # anchor_x = self.frame.rect['x'] + self.frame.anchor['x'] - window_x
            # anchor_y = self.frame.rect['y'] + self.frame.anchor['y'] - window_y
            # pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(anchor_x, anchor_y, 1, 1), 1)

            # if self.hit_box and self.hit_box.w > 0 and self.hit_box.h > 0:
            #     pygame.draw.rect(surface, (0, 200, 0), self.hit_box.move(-window_x, -window_y), 1)
            # if self.attack_box and self.attack_box.w > 0 and self.attack_box.h > 0:
            #     pygame.draw.rect(surface, (200, 0, 0), self.attack_box.move(-window_x, -window_y), 1)

    def set_frame(self, frame_name):
        self.stop_animation()
        self._animation = None
        self._frame = self._frames_store.get_frame(frame_name)

    def stop_animation(self):
        self._animation_frame_delay = 0
        self._animation_frame_index = 0
        self._animating = False

    def play_animation(self, animation_name, flags=0, speed=1):
        if (self._flags & FramesStore.FLAG_LOOP_ANIMATION) > 0 and \
                        self._flags == flags and animation_name == self._animation_name:
            return

        self._animating = True
        self._animation_speed = speed
        self._animation_name = animation_name
        self._flags = flags
        self._set_animation_frame(0)

    def skip_to_last_animation_frame(self):
        if not self._animating:
            return

        self._animating = False
        self._set_animation_frame(len(self._animation.frames) - 1)

    def update(self, game_speed):
        self._update_collision_boxes()
        if not self._animating:
            return

        if self._animation_frame_delay <= 0:
            self.next_animation_frame()
            return
        else:
            self._animation_frame_delay -= game_speed * self._animation_speed
            return

    def next_animation_frame(self):
        new_animation_frame_index = self._animation_frame_index + 1
        if new_animation_frame_index > len(self._animation.frames) - 1:
            if not (self._flags & FramesStore.FLAG_LOOP_ANIMATION) > 0:
                self._animating = False
                return
            else:
                new_animation_frame_index = 0

        self._set_animation_frame(new_animation_frame_index)

    def previous_animation_frame(self):
        new_animation_frame_index = self._animation_frame_index - 1
        if new_animation_frame_index < 0:
            new_animation_frame_index = len(self._animation.frames) - 1

        self._set_animation_frame(new_animation_frame_index)

    def _set_animation_frame(self, frame_index):
        self._animation = self._frames_store.get_animation(self._animation_name)
        self._animation_frame_index = frame_index
        self.animation_frame = self._animation.frames[self._animation_frame_index]
        new_frame = self._animation.frames[frame_index]
        self._animation_frame_delay = new_frame.delay
        self._frame = self._frames_store.get_frame(new_frame.frame_name)

        # Override animation flip if the frame is also flipped
        flags = self._flags
        if self.animation_frame.flip_x:
            flags |= FramesStore.FLAG_FLIP_X
        if self.animation_frame.flip_y:
            flags |= FramesStore.FLAG_FLIP_Y

        # Updates the drawable
        self._drawable.texture = self._frame.image
        self._drawable.scale = Vector2(self._frame.rect.w, self._frame.rect.h).dot(self._scale)
        self._drawable.anchor = self._frame.anchor.dot(self._scale)
        self._drawable.flip_x = (flags & FramesStore.FLAG_FLIP_X > 0)
        self._drawable.flip_y = (flags & FramesStore.FLAG_FLIP_Y > 0)

    def _update_collision_boxes(self):
        if not self._animating:
            self._attack_box = None
            self._hit_box = None

        # TODO: flip_y should be handled as well
        animation_frame = self._animation.frames[self._animation_frame_index]
        flip_x = ((self._flags & FramesStore.FLAG_FLIP_X) > 0) ^ animation_frame.flip_x

        if self._frame.hit_box:
            self._hit_box = self._frame.hit_box.copy()
            if flip_x:
                self._hit_box.x = - self._hit_box.x - self._hit_box.width
            self._hit_box.move_ip(self._x, self._y)
        else:
            self._hit_box = None

        if self._frame.attack_box:
            self._attack_box = self._frame.attack_box.copy()
            if flip_x:
                self._attack_box.x = - self._attack_box.x - self._attack_box.width
            self._attack_box.move_ip(self._x, self._y)
        else:
            self._attack_box = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self._drawable.angle = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._drawable.scale *= value

    @property
    def hit_box(self):
        return self._hit_box

    @property
    def attack_box(self):
        return self._attack_box

    @property
    def animating(self):
        return self._animating

    @property
    def shader(self):
        return self._drawable.shader

    @shader.setter
    def shader(self, shader):
        self._drawable.shader = shader
