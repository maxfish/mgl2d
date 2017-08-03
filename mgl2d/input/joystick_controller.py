import sdl2

from mgl2d.input.game_controller import GameController


class JoystickController(GameController):
    _DEBUG_CONTROLLER = False

    def __init__(self):
        super().__init__()
        self._sdl_controller = None
        self._sdl_joystick = None
        self._sdl_joystick_id = None

    def open(self, device_index):
        self._sdl_controller = sdl2.SDL_GameControllerOpen(device_index)
        self._sdl_joystick = sdl2.SDL_GameControllerGetJoystick(self._sdl_controller)
        self._sdl_joystick_id = sdl2.SDL_JoystickInstanceID(self._sdl_joystick)

        self._controller_name = sdl2.SDL_JoystickName(self._sdl_joystick)
        self._num_axis = sdl2.SDL_JoystickNumAxes(self._sdl_joystick),
        self._num_buttons = sdl2.SDL_JoystickNumButtons(self._sdl_joystick)
        self._num_balls = sdl2.SDL_JoystickNumBalls(self._sdl_joystick)

        for btn_index in range(0, self.MAX_BUTTONS):
            self._button_down[btn_index] = 0
            self._button_pressed[btn_index] = 0
            self._button_released[btn_index] = 0

        if self._sdl_joystick_id != -1:
            self._connected = True

    def close(self):
        sdl2.SDL_GameControllerClose(self._sdl_controller)
        self._sdl_controller = None
        self._sdl_joystick = None
        self._sdl_joystick_id = None

    def update(self):
        if not self._connected:
            return

        for btn_index in range(0, self._num_buttons):
            self._button_pressed[btn_index] = 0

            is_down = sdl2.SDL_GameControllerGetButton(self._sdl_controller, btn_index)
            if is_down and not self._button_down[btn_index]:
                self._button_pressed[btn_index] = True

            self._button_down[btn_index] = is_down

    def get_axis(self, axis_name):
        pass

    def get_axis_digital_value(self, axis_name):
        pass
