import sdl2

from mgl2d.input import GameController


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

    def get_axis(self, axis_index):
        axis_value = sdl2.SDL_GameControllerGetAxis(self._sdl_controller, axis_index)

        # Sticks have a dead zone
        if axis_index != self.AXIS_TRIGGER_LEFT and axis_index != self.AXIS_TRIGGER_RIGHT:
            if abs(axis_value) < self.AXIS_DEAD_ZONE:
                return 0

        # Return scaled value
        return axis_value / self.AXIS_MAX_VALUE if axis_value > 0 else -axis_value / self.AXIS_MIN_VALUE

    def get_axis_digital_value(self, axis_name):
        return 0

    def to_string(self):
        return f'[\'{self._controller_name}\',axis:{self._num_axis},btns:{self._num_buttons}]'
