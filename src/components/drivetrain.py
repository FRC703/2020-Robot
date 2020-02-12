import wpilib
import wpilib.drive
import rev

from magicbot import tunable

class Drivetrain:
    motorr1: rev.CANSparkMax
    motorr2: rev.CANSparkMax
    motorl1: rev.CANSparkMax
    motorl2: rev.CANSparkMax

    tank_drive: bool
    twist: bool

    turn_multiplier = tunable(0.7)
    
    def setup(self):
        self.drive = wpilib.drive.DifferentialDrive(self.motorl1, self.motorr1)

    def arcadeDrive(self, forward, turn, twist):
        self.forward = forward
        self.turn = turn
        self.twist_power = twist

    def tankDrive(self, left, right):
        self.forward = left
        self.turn = right

    def execute(self):
        if self.tank_drive:
            # Reusing forward and turn as left and right to reduce memory usage
            self.drive.tankDrive(self.forward, self.turn)
        else:
            if self.twist:
                self.drive.arcadeDrive(self.forward, self.twist_power, True)
            else:
                self.drive.arcadeDrive(self.forward, self.turn, True)