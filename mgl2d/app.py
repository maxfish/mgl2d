import ctypes

import sdl2

DEFAULT_FPS = 50


class App(object):
    def __init__(self):
        super().__init__()
        self._running = False
        self._screen = None
        self._fps = DEFAULT_FPS
        self._frame_time_ms = 1000 / DEFAULT_FPS

    def run(self, screen, draw_func, update_func, fps=DEFAULT_FPS):
        self._screen = screen
        self._running = True
        self._fps = fps
        self._frame_time_ms = 1000 / fps
        event = sdl2.SDL_Event()

        time_accumulator_ms = 0
        old_time = sdl2.SDL_GetPerformanceCounter()
        timer_resolution = sdl2.SDL_GetPerformanceFrequency() / 1000  # ms

        while self._running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    self._running = False

            # Adjust the loop speed based on the time passed
            current_time = sdl2.SDL_GetPerformanceCounter()
            delta_time_ms = (current_time - old_time) / timer_resolution

            time_accumulator_ms += delta_time_ms
            while time_accumulator_ms > self._frame_time_ms:
                update_func(delta_time_ms)
                time_accumulator_ms -= self._frame_time_ms
            old_time = current_time

            # Update the screen
            screen.begin_update()
            draw_func(screen)
            screen.end_update()

        self.stop()

    def stop(self):
        self._running = False
        self._screen.close()
        sdl2.SDL_Quit()

    @property
    def fps(self):
        return self._fps

    @property
    def frame_time_ms(self):
        return self._frame_time_ms
