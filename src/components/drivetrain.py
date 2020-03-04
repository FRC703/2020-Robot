import wpilib
import wpilib.drive
import wpilib.controller
import rev

from magicbot import tunable, will_reset_to


class Drivetrain:
    motorr1: rev.CANSparkMax
    motorr2: rev.CANSparkMax
    motorl1: rev.CANSparkMax
    motorl2: rev.CANSparkMax

    using_vision = will_reset_to(False)

    vision_dist_kP = tunable(0.15)
    vision_dist_kI = tunable(0)
    vision_dist_kD = tunable(0)

    vision_turn_kP = tunable(0.055)
    vision_turn_kI = tunable(0.0003)
    vision_turn_kD = tunable(0)

    vision_turn_integral_range = tunable(0.1)

    forward = will_reset_to(0)
    turn = will_reset_to(0)
    twist_power = will_reset_to(0)

    tank_drive: bool
    twist: bool

    vision_integral = 0

    intake_is_front = True

    turn_multiplier = tunable(0.7)

    def vision_aim(self, x: float, y: float, aim_x=True, aim_y=True):
        self.using_vision = True
        # out = self.vision_pid.calculate(x)
        # print(out)
        self.vision_integral += x
        p = self.vision_turn_kP * x
        i = self.vision_turn_kI * self.vision_integral
        out = min(.25, max(p + i, -.25))
        self.turn = out
        self.twist_power = self.turn
        if abs(x) < self.vision_turn_integral_range:
            self.vision_integral = 0
        # self.forward = min(.5, max(self.vision_dist_kP * y, -.5))

    def reset_integral(self):
        self.vision_integral = 0

    def setup(self):
        self.motorr1.restoreFactoryDefaults()
        self.motorr2.restoreFactoryDefaults()
        self.motorl1.restoreFactoryDefaults()
        self.motorl2.restoreFactoryDefaults()
        self.motorr2.follow(self.motorr1)
        self.motorl2.follow(self.motorl1)
        self.drive = wpilib.drive.DifferentialDrive(self.motorl1, self.motorr1)
        # self.vision_pid = wpilib.controller.PIDController(0.006, 0.001, 0.0009)
        # self.vision_pid.setSetpoint(0)
        # self.vision_pid.calculate(0)
        # self.vision_pid.setTolerance(0.1)

    def arcadeDrive(self, forward, turn, twist):
        self.forward = forward * (-1 if self.intake_is_front else 1)
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
        if not self.using_vision:
            self.reset_integral()
        if self.tank_drive:
            # Reusing forward and turn as left and right to reduce memory usage
            self.drive.tankDrive(self.forward, self.turn)
        else:
            if self.twist:
                self.drive.arcadeDrive(self.forward, self.twist_power, True)
                wpilib.SmartDashboard.putNumber("turnSpeed", self.twist_power)
            else:
                self.drive.arcadeDrive(self.forward, self.turn, True)
                wpilib.SmartDashboard.putNumber("turnSpeed", self.turn)

            wpilib.SmartDashboard.putNumber("forwardSpeed", self.forward)
