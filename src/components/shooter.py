from limelight import limelight
from magicbot import will_reset_to, tunable
from controllers.PIDSparkMax import PIDSparkMax

import wpilib
from ctre import TalonSRX, ControlMode


from typing import Tuple


class Shooter:
    limelight_state = will_reset_to(1)
    motor_rpm = will_reset_to(0)
    feeder_motor_speed = will_reset_to(0)

    target_rpm = tunable(-4200)
    feed_speed_setpoint = tunable(-0.85)
    rpm_error = tunable(100)
    x_aim_error = tunable(1)
    y_aim_error = tunable(2)

    motor: PIDSparkMax
    feeder_motor: TalonSRX

    def setup(self):
        """
        Runs right after the createObjects method is run.
        Sets up all the networktables values and configures
        the shooter motor PID values
        """
        self.limelight = limelight.Limelight()

        self.log()

        # Shooter motor configuration
        self.motor.fromKu(0.05, 1)  # P = 0.03, I = 0.06, D = 0.00375
        self.motor.setFF(1 / 5880)
        # self.motor._motor_pid.setP(0.0015)
        # self.motor._motor_pid.setD(.008)
        # self.motor._motor_pid.setI(0.005)
        self.motor._motor_pid.setIZone(0.5)
        self.motor.motor.setSmartCurrentLimit(100)

    def aim(self) -> Tuple[float, float]:
        """
        Will return the distances from the crosshair
        """
        self.limelight_state = 3
        x = self.limelight.horizontal_offset
        y = self.limelight.vertical_offset
        return (x, y)

    @property
    def is_aimed(self):
        """
        Test whether the target is within a tolerance
        """
        x, y = self.aim()
        if abs(x) > self.x_aim_error:
            return False
        # if abs(y) > self.y_aim_error:
        #     return False
        return True

    @property
    def is_ready(self):
        """
        Returns whether the current rpm of the motor is within
        a certain range, specified by the `rpm_error` property
        """
        return (
            self.rpm_error + self.motor_rpm
            > self.motor.rpm
            > -self.rpm_error + self.motor_rpm
        )

    def shoot(self):
        """
        Sets the shooter to start moving toward the setpoint
        """
        self.motor_rpm = self.target_rpm

    def feed(self):
        """
        Start the feeder to move the power cells towards the flywheel
        """
        self.feeder_motor_speed = self.feed_speed_setpoint

    def execute(self):
        self.limelight.light(self.limelight_state)
        if abs(self.motor_rpm) < 200:
            self.motor.stop()
        else:
            self.motor.set(self.motor_rpm)
        if abs(self.motor.rpm) > 3500 or self.feeder_motor_speed:
            self.feeder_motor.set(ControlMode.PercentOutput, -1)
        else:
            self.feeder_motor.set(ControlMode.PercentOutput, 0)
        # self.feeder_motor.set(ControlMode.PercentOutput, self.feeder_motor_speed)
        self.log()

    def log(self):
        """
        Get values relating to the shooter and post them
        to the dashboard for logging reasons.
        """
        wpilib.SmartDashboard.putBoolean(
            "limelightLightState", True if self.limelight_state == 3 else False
        )
        wpilib.SmartDashboard.putBoolean("shooterReady", self.is_ready)
        wpilib.SmartDashboard.putBoolean("isAimed", self.is_aimed)
        wpilib.SmartDashboard.putBoolean("targetsFound", self.limelight.valid_targets)
        wpilib.SmartDashboard.putNumber("shooterSpeedTarget", abs(self.motor_rpm))
        wpilib.SmartDashboard.putNumber("shooterMotorSpeed", abs(self.motor.rpm))
        wpilib.SmartDashboard.putNumber(
            "shooterOutput", self.motor.motor.getAppliedOutput()
        )
