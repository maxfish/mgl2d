import array
import logging

import sdl2

logger = logging.getLogger(__name__)


class GameController(object):
    _joysticks_initialized = False

    MAX_AXIS = sdl2.SDL_CONTROLLER_AXIS_MAX
    MAX_BUTTONS = sdl2.SDL_CONTROLLER_BUTTON_MAX

    BUTTON_INVALID = sdl2.SDL_CONTROLLER_BUTTON_INVALID
    BUTTON_A = sdl2.SDL_CONTROLLER_BUTTON_A
    BUTTON_B = sdl2.SDL_CONTROLLER_BUTTON_B
    BUTTON_X = sdl2.SDL_CONTROLLER_BUTTON_X
    BUTTON_Y = sdl2.SDL_CONTROLLER_BUTTON_Y
    BUTTON_BACK = sdl2.SDL_CONTROLLER_BUTTON_BACK
    BUTTON_GUIDE = sdl2.SDL_CONTROLLER_BUTTON_GUIDE
    BUTTON_START = sdl2.SDL_CONTROLLER_BUTTON_START
    BUTTON_LEFTSTICK = sdl2.SDL_CONTROLLER_BUTTON_LEFTSTICK
    BUTTON_RIGHTSTICK = sdl2.SDL_CONTROLLER_BUTTON_RIGHTSTICK
    BUTTON_LEFTSHOULDER = sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER
    BUTTON_RIGHTSHOULDER = sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER
    BUTTON_DPAD_UP = sdl2.SDL_CONTROLLER_BUTTON_DPAD_UP
    BUTTON_DPAD_DOWN = sdl2.SDL_CONTROLLER_BUTTON_DPAD_DOWN
    BUTTON_DPAD_LEFT = sdl2.SDL_CONTROLLER_BUTTON_DPAD_LEFT
    BUTTON_DPAD_RIGHT = sdl2.SDL_CONTROLLER_BUTTON_DPAD_RIGHT

    def __init__(self):
        self._connected = False
        if not self._joysticks_initialized:
            sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
            self._joysticks_initialized = True

        self._axis = array.array('i', (0 for i in range(0, self.MAX_AXIS)))
        self._button_pressed = array.array('i', (0 for i in range(0, self.MAX_BUTTONS)))
        self._button_released = array.array('i', (0 for i in range(0, self.MAX_BUTTONS)))
        self._button_down = array.array('i', (0 for i in range(0, self.MAX_BUTTONS)))

    @classmethod
    def load_database(cls, filename):
        # Use a configurations DB file, e.g. https://github.com/gabomdq/SDL_GameControllerDB
        num_entries = sdl2.SDL_GameControllerAddMappingsFromFile(str.encode(filename))
        logger.info('Loaded %d joystick definitions' % num_entries)

    def is_connected(self):
        return self._connected

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

    def get_axis(self, axis_name):
        raise NotImplementedError('This method has to be implemented by the subclass')

    def get_axis_digital_value(self, axis_name):
        raise NotImplementedError('This method has to be implemented by the subclass')
