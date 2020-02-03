import ctre
import wpilib

from magicbot import will_reset_to


class Intake:

    motor: ctre.TalonSRX
    intake_speed = will_reset_to(0)

    def setup(self):
        wpilib.SmartDashboard.putNumber("intakeSpeed", 0)

    def intake(self, speed):
        self.intake_speed = speed

    def execute(self):
        wpilib.SmartDashboard.putNumber("intakeSpeed", self.intake_speed)
        self.motor.set(ctre.ControlMode.PercentOutput, self.intake_speed)
