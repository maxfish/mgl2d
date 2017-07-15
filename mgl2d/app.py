import ctypes

import sdl2


class App(object):
    def __init__(self):
        super().__init__()
        self._running = False
        self._screen = None

    def run(self, screen, draw_func, update_func, fps=30):
        # TODO: support FPS setting

        self._screen = screen
        self._running = True
        event = sdl2.SDL_Event()
        ms_to_wait = 1
        delta_ms = 1

        while self._running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    self._running = False

            update_func(delta_ms)
            screen.begin_update()
            draw_func(screen)
            screen.end_update()
            sdl2.SDL_Delay(ms_to_wait)

        self.stop()

    def stop(self):
        self._running = False
        self._screen.close()
        sdl2.SDL_Quit()
