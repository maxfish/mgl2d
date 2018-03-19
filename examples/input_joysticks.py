#!/usr/bin/env python
from mgl2d.input.game_controller import GameController
from mgl2d.input.game_controller_manager import GameControllerManager

# No graphics output! Look at the console
# Hot-plugging is currently not supported
game_controller = GameControllerManager()
num_controllers = game_controller.num_joysticks

if num_controllers == 0:
    print('No joysticks found')
    exit(0)

joysticks = []

# Initializes the joysticks
for j in range(num_controllers):
    joystick = game_controller.grab_controller()
    joysticks.append(joystick)
    print(f'Found a joystick -> {joystick.to_string()}')

# Use the joysticks here
button_a = joysticks[0].is_button_down(GameController.BUTTON_A)  # True/False
right_trigger = joysticks[0].get_axis(GameController.AXIS_TRIGGER_RIGHT)  # 0 <= value <= 1
left_stick_x = joysticks[0].get_axis(GameController.AXIS_LEFT_X)  # -1 <= value <= 1

# Close the joysticks
for joystick in joysticks:
    game_controller.release_controller(joystick)
