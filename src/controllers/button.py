import wpilib


class JoystickButton:
    joystick: wpilib.Joystick
    button_id: int

    def __init__(self, joystick: wpilib.Joystick, button_id: int):
        self.joystick = joystick
        self.button_id = button_id

    def get(self):
        return self.joystick.getRawButton(self.button_id)
