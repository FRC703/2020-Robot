import ctre
from controllers.PIDSparkMax import PIDSparkMax
import wpilib

import rev
from magicbot import will_reset_to, tunable


class Intake:

    motor: ctre.TalonSRX
    arm_motor: PIDSparkMax
    intake_speed = 0
    intake_speed_in = -0.6
    intake_speed_out = 0.1
    intake_up = True
    _intake_arm_down_position = 90  # Temporary to figure out the direction
    _intake_arm_motor_on_position = 70
    _gear_ratio = 1.4

    intake_arm_position_setpoint = will_reset_to(0)

    @property
    def intake_arm_down_position(self) -> float:
        """
        Returns the angle that the arm should drop down to.
        """
        return self._arm_angle_convert(self._intake_arm_down_position)

    @property
    def intake_arm_motor_on_position(self) -> float:
        """
        Returns the angle that the motor for the intake will be turned on when lowering
        """
        return self._arm_angle_convert(self._intake_arm_motor_on_position)

    @property
    def arm_position(self):
        return self.arm_motor.motor.getEncoder().getPosition()

    def _arm_angle_convert(self, angle: float) -> float:
        return angle / 3.6 * self._gear_ratio

    def setup(self):
        """
        Initialize the motors for the intake.
        """
        self.arm_motor.control_mode = rev.ControlType.kPosition
        self.arm_motor.motor.getEncoder().setPosition(0)
        self.arm_motor.motor.setSmartCurrentLimit(10)
        self.arm_motor.setP(0.035)
        self.arm_motor.setI(0.01)
        self.arm_motor.setD(0.001)
        wpilib.SmartDashboard.putNumber("intakeSpeed", 0)

    def lower(self):
        self.intake_up = False

    def lift(self):
        self.intake_up = True

    def run_wheels(self):
        self.intake_speed = self.intake_speed_in

    def stop_wheels(self):
        self.intake_speed = self.intake_speed_out

    def reset_arm_encoders(self):
        self.arm_motor.motor.getEncoder().setPosition(self.intake_arm_down_position)

    @property
    def arm_position(self):
        self.arm_motor.motor.getEncoder().getPosition() / 36

    def execute(self):
        if self.intake_up:
            self.arm_motor.set(0)
        else:
            self.arm_motor.set(self.intake_arm_down_position)
        self.motor.set(ctre.ControlMode.PercentOutput, self.intake_speed)
        wpilib.SmartDashboard.putNumber("intakeSpeed", self.intake_speed)
        wpilib.SmartDashboard.putBoolean("intakeIn", self.intake_speed < -0.1)
        wpilib.SmartDashboard.putNumber(
            "armPosition", self.arm_motor.motor.getEncoder().getPosition()
        )
        wpilib.SmartDashboard.putNumber("armPower", self.arm_motor.rpm)
        self.intake_speed = 0
