import wpilib
import rev
from magicbot import will_reset_to, tunable

class Drivetrain:
    forward_speed = will_reset_to(0)
    turn_speed = will_reset_to(0)

    dt: wpilib.DifferentialDrive

    def drive(self, forward, turn):
        self.forward_speed = forward
        self.turn_speed = turn

    def execute(self):
        self.dt.arcadeDrive(self.forward_speed, self.turn_speed)