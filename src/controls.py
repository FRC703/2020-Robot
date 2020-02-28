from wpilib import Joystick


class Controls:
    def __init__(self, joystick: Joystick, joystick2: Joystick):
        self.joystick = joystick
        self.joystick2 = joystick2

    @property
    def shoot(self):
        """
        State machine based shoot
        """
        return self.joystick.getRawButton(1)

    @property
    def manual_shoot(self):
        """
        Just shoot and feed, no state machine
        """
        return self.joystick.getRawButton(2)

    @property
    def toggle_camera(self):
        return self.joystick.getRawButtonPressed(12)

    @property
    def feed(self):
        return self.joystick.getRawButton(9)

    @property
    def intake(self):
        return self.joystick.getRawButton(10)

    @property
    def aim(self):
        return self.joystick.getRawButton(4)

    @property
    def reset_intake_arm_to_down(self):
        return (
            self.joystick.getRawButtonPressed(7)
            and self.joystick.getRawButtonPressed(9)
            and self.joystick.getRawButtonPressed(11)
        )

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
        return pow(self.joystick.getRawAxis(2), 3) * 0.5

    @property
    def arcade_drive_forward(self):
        return -pow(self.joystick.getRawAxis(1), 3)
