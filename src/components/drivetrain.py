import wpilib
import wpilib.drive
import rev

from magicbot import tunable


class Drivetrain:
    motorr1: rev.CANSparkMax
    motorr2: rev.CANSparkMax
    motorl1: rev.CANSparkMax
    motorl2: rev.CANSparkMax

    vision_dist_kP = tunable(0.3)
    vision_dist_kI = tunable(0)
    vision_dist_kD = tunable(0)

    vision_turn_kP = tunable(0.3)
    vision_turn_kI = tunable(0)
    vision_turn_kD = tunable(0)

    tank_drive: bool
    twist: bool

    intake_is_front = True

    turn_multiplier = tunable(0.7)

    def vision_aim(self, x: float, y: float, aim_x=True, aim_y=True):
        self.turn = self.vision_turn_kP * x
        self.forward = self.vision_dist_kP * y

    def setup(self):
        self.motorr2.follow(self.motorr1)
        self.motorl2.follow(self.motorl1)
        self.drive = wpilib.drive.DifferentialDrive(self.motorl1, self.motorr1)

    def arcadeDrive(self, forward, turn, twist):
        self.forward = forward * 1 if self.intake_is_front else -1
        self.turn = turn
        self.twist_power = twist

    def tankDrive(self, left, right):
        if self.intake_is_front:
            self.forward = left
            self.turn = right
        else:
            self.forward = right
            self.turn = left

    def execute(self):
        if self.tank_drive:
            # Reusing forward and turn as left and right to reduce memory usage
            self.drive.tankDrive(self.forward, self.turn)
        else:
            if self.twist:
                self.drive.arcadeDrive(self.forward, self.twist_power, True)
            else:
                self.drive.arcadeDrive(self.forward, self.turn, True)
