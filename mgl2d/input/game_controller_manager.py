import logging

import sdl2

from mgl2d.input import JoystickController
from mgl2d.input import KeyboardController

logger = logging.getLogger(__name__)


class GameControllerManager:
    _joysticks_initialized = False

    def __init__(self, allow_keyboard=True):
        self.allow_keyboard = allow_keyboard

        if not self._joysticks_initialized:
            sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
            self._joysticks_initialized = True

        self._num_joysticks = sdl2.joystick.SDL_NumJoysticks()
        logger.info('Found %d connected joystick[s]' % self._num_joysticks)
        self._instances = [None] * (self._num_joysticks + (1 if allow_keyboard else 0))

    @property
    def num_joysticks(self):
        return self._num_joysticks

    def load_joysticks_database(cls, filename):
        # Use a configurations DB file, e.g. https://github.com/gabomdq/SDL_GameControllerDB
        num_entries = sdl2.SDL_GameControllerAddMappingsFromFile(str.encode(filename))
        logger.info('Loaded %d joystick definitions' % num_entries)

    def grab_controller(self):
        for index in range(0, self._num_joysticks):
            if self._instances[index] is None:
                controller = JoystickController()
                controller.open(index)
                logger.info('Got joystick \'%s\'' % controller.to_string())
                self._instances[index] = controller
                return controller

        # No joysticks available
        if self.allow_keyboard and self._instances[self._num_joysticks] is None:
            controller = KeyboardController()
            controller.open(0)
            self._instances[self._num_joysticks] = controller
            return controller

        return None

    def release_controller(self, controller):
        for index in range(0, len(self._instances)):
            if self._instances[index] == controller:
                controller.close()
                self._instances[index] = None
