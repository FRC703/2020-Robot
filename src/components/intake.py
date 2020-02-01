import ctre

from magicbot import will_reset_to

class Intake:

    motor: ctre.TalonSRX
    intake_speed = will_reset_to(0)

    def intake(self, speed):
        self.intake_speed = speed

    def execute(self):
        self.motor.set(ctre.ControlMode.PercentOutput, self.intake_speed)