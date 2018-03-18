import array
import logging

import sdl2

logger = logging.getLogger(__name__)


class GameController(object):
    # BUTTONS
    MAX_BUTTONS = sdl2.SDL_CONTROLLER_BUTTON_MAX
    BUTTON_INVALID = sdl2.SDL_CONTROLLER_BUTTON_INVALID
    BUTTON_A = sdl2.SDL_CONTROLLER_BUTTON_A
    BUTTON_B = sdl2.SDL_CONTROLLER_BUTTON_B
    BUTTON_X = sdl2.SDL_CONTROLLER_BUTTON_X
    BUTTON_Y = sdl2.SDL_CONTROLLER_BUTTON_Y
    BUTTON_BACK = sdl2.SDL_CONTROLLER_BUTTON_BACK
    BUTTON_GUIDE = sdl2.SDL_CONTROLLER_BUTTON_GUIDE
    BUTTON_START = sdl2.SDL_CONTROLLER_BUTTON_START
    BUTTON_LEFT_STICK = sdl2.SDL_CONTROLLER_BUTTON_LEFTSTICK
    BUTTON_RIGHT_STICK = sdl2.SDL_CONTROLLER_BUTTON_RIGHTSTICK
    BUTTON_LEFT_SHOULDER = sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER
    BUTTON_RIGHT_SHOULDER = sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER
    BUTTON_DIR_PAD_UP = sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP
    BUTTON_DIR_PAD_DOWN = sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN
    BUTTON_DIR_PAD_LEFT = sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT
    BUTTON_DIR_PAD_RIGHT = sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT

    # AXIS
    MAX_AXIS = sdl2.SDL_CONTROLLER_AXIS_MAX
    AXIS_LEFT_X = sdl2.SDL_CONTROLLER_AXIS_LEFTX
    AXIS_LEFT_Y = sdl2.SDL_CONTROLLER_AXIS_LEFTY
    AXIS_RIGHT_X = sdl2.SDL_CONTROLLER_AXIS_RIGHTX
    AXIS_RIGHT_Y = sdl2.SDL_CONTROLLER_AXIS_RIGHTY
    AXIS_TRIGGER_LEFT = sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT
    AXIS_TRIGGER_RIGHT = sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT

    def __init__(self):
        self._connected = False
        self._axis = array.array('i', (0 for _ in range(0, self.MAX_AXIS)))
        self._button_pressed = array.array('i', (0 for _ in range(0, self.MAX_BUTTONS)))
        self._button_released = array.array('i', (0 for _ in range(0, self.MAX_BUTTONS)))
        self._button_down = array.array('i', (0 for _ in range(0, self.MAX_BUTTONS)))
        self._controller_name = '<not initialized>'
        self._num_axis = 0
        self._num_buttons = 0
        self._num_balls = 0

    def is_connected(self):
        return self._connected

    @property
    def name(self):
        return self._controller_name

    @property
    def num_axis(self):
        return self._num_axis

    @property
    def num_buttons(self):
        return self._num_buttons

    @property
    def num_balls(self):
        return self._num_balls

    def is_button_pressed(self, button_id):
        if not self._connected:
            return False
        return self._button_pressed[button_id]

    def is_button_down(self, button_id):
        if not self._connected:
            return False
        return self._button_down[button_id]

    def is_button_released(self, button_id):
        if not self._connected:
            return False
        return self._button_released[button_id]

    def open(self, device_index):
        raise NotImplementedError('This method has to be implemented by the subclass')

    def close(self):
        raise NotImplementedError('This method has to be implemented by the subclass')

    def update(self):
        raise NotImplementedError('This method has to be implemented by the subclass')

    def get_axis(self, axis_index):
        raise NotImplementedError('This method has to be implemented by the subclass')

    def get_axis_digital_value(self, axis_name):
        raise NotImplementedError('This method has to be implemented by the subclass')
