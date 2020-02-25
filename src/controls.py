from wpilib import Joystick


class Controls:
    def __init__(self, joystick: Joystick, joystick2: Joystick):
        self.joystick = joystick
        self.joystick2 = joystick2

    @property
    def shoot(self):
        return self.joystick.getRawButton(3)

    @property
    def feed(self):
        return self.joystick.getRawButton(5)


    @property
    def intake(self):
        return self.joystick.getRawButton(1)

    @property
    def reset_intake_arm_to_down(self):
        return self.joystick.getRawButtonPressed(11)

    @property
    def tank_drive_left(self):
        return self.joystick.getRawAxis(1)

    @property
    def tank_drive_right(self):
        return self.joystick.getRawAxis(1)

    @property
    def arcade_drive_turn(self):
        return self.joystick.getRawAxis(0)

    @property
    def arcade_drive_twist(self):
        return pow(self.joystick.getRawAxis(2), 3) * .5

    @property
    def arcade_drive_forward(self):
        return -self.joystick.getRawAxis(1)
