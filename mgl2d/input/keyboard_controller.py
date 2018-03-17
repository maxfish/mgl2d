import sdl2

from mgl2d.input.game_controller import GameController


class KeyboardController(GameController):
    def __init__(self):
        super().__init__()
        self._connected = True
        self._controller_name = "Keyboard"
        self._num_axis = 0
        self._num_balls = 0
        self._num_buttons = 11

        self._button_mapping = {
            self.BUTTON_A: sdl2.SDL_SCANCODE_A,
            self.BUTTON_B: sdl2.SDL_SCANCODE_S,
            self.BUTTON_X: sdl2.SDL_SCANCODE_D,
            self.BUTTON_Y: sdl2.SDL_SCANCODE_F,
            self.BUTTON_DPAD_UP: sdl2.SDL_SCANCODE_UP,
            self.BUTTON_DPAD_DOWN: sdl2.SDL_SCANCODE_DOWN,
            self.BUTTON_DPAD_LEFT: sdl2.SDL_SCANCODE_LEFT,
            self.BUTTON_DPAD_RIGHT: sdl2.SDL_SCANCODE_RIGHT,
            self.BUTTON_BACK: 0,
            self.BUTTON_GUIDE: 0,
            self.BUTTON_START: 0,
            self.BUTTON_LEFTSTICK: 0,
            self.BUTTON_RIGHTSTICK: 0,
            self.BUTTON_LEFTSHOULDER: 0,
            self.BUTTON_RIGHTSHOULDER: 0,
        }

    def open(self, device_index):
        pass

    def close(self):
        pass

    def update(self):
        keystatus = sdl2.SDL_GetKeyboardState(None)
        for btn_index in range(0, self.MAX_BUTTONS):
            self._button_pressed[btn_index] = 0

            is_down = keystatus[self._button_mapping[btn_index]]
            if is_down and not self._button_down[btn_index]:
                self._button_pressed[btn_index] = True

            self._button_down[btn_index] = is_down

    def get_axis(self, axis_index):
        return None

    def get_axis_digital_value(self, axis_name):
        return 0
