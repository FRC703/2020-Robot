from limelight import limelight
from magicbot import will_reset_to, tunable
from controllers.PIDSparkMax import PIDSparkMax
import wpilib


class Shooter:
    # limelight: limelight.Limelight

    limelight_state = will_reset_to(1)
    motor_rpm = will_reset_to(0)
    target_rpm = tunable(-4350)
    motor: PIDSparkMax

    def setup(self):
        self.limelight = limelight.Limelight()
        wpilib.SmartDashboard.putBoolean("limelightLightState", False)
        wpilib.SmartDashboard.putNumber("shooterMotorSpeed", 0)

    def aim(self):
        # print("LIMELIGHT DOING THINGS")
        self.limelight_state = 3

    def shoot(self):
        self.motor_rpm = self.target_rpm

    def execute(self):
        # print(f'Execute limelight {self.limelight_state}')
        wpilib.SmartDashboard.putBoolean("limelightLightState", True if self.limelight_state == 3 else False)
        self.limelight.light(self.limelight_state)
        wpilib.SmartDashboard.putNumber("shooterMotorSpeed", self.motor.rpm)
        self.motor.set(self.motor_rpm)
