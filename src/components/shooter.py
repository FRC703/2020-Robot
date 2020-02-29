from limelight import limelight
from magicbot import will_reset_to, tunable, feedback
from controllers.PIDSparkMax import PIDSparkMax

import wpilib
from ctre import TalonSRX, ControlMode


from typing import Tuple


class Shooter:
    limelight_state = will_reset_to(1)
    motor_rpm = will_reset_to(0)
    feeder_motor_speed = will_reset_to(0)

    # target_rpm = tunable(-3500)
    feed_speed_setpoint = tunable(-1)
    rpm_error = tunable(300)
    x_aim_error = tunable(1.2)
    y_aim_error = tunable(2)

    motor: PIDSparkMax
    feeder_motor: TalonSRX

    camera_state: int

    @property
    def target_rpm(self):
        _, y = self.aim()
        return -1 * (5.232 * pow(y, 2) - 70.76 * y + 3300)

    def setup(self):
        """
        Runs right after the createObjects method is run.
        Sets up all the networktables values and configures
        the shooter motor PID values
        """
        self.limelight = limelight.Limelight()

        self.log()

        # Shooter motor configuration
        self.motor.fromKu(0.0008, 0.6)  # P = 0.03, I = 0.05, D = 0.125
        self.motor.setFF(1 / 5880)
        # self.motor.setFF(0)
        # self.motor.setPID(.0008, 0, 0)
        # self.motor.setPID(0.0015, 0.008, 0.005)
        self.motor._motor_pid.setIZone(0.5)
        self.motor.motor.setSmartCurrentLimit(100)

    @feedback
    def aim(self) -> Tuple[float, float]:
        """
        Will return the distances from the crosshair
        """
        # self.limelight_state = 3
        self.camera_state = 0
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

    def backdrive(self):
        """
        Start the feeder to move the power cells towards the flywheel
        """
        self.feeder_motor_speed = 1

    def execute(self):
        self.limelight.light(self.limelight_state)
        # self.limelight.pipeline(self.limelight_state)
        if abs(self.motor_rpm) < 200:
            self.motor.stop()
        else:
            self.motor.set(self.motor_rpm)
        if (
            abs(self.motor_rpm) > 500
            and abs(self.motor.rpm) > abs(self.motor_rpm) - self.rpm_error
        ) or self.feeder_motor_speed:
            if not self.feeder_motor_speed:
                self.feed()
            self.feeder_motor.set(ControlMode.PercentOutput, self.feeder_motor_speed)
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
        # wpilib.SmartDashboard.putBoolean("isAimed", self.is_aimed)
        wpilib.SmartDashboard.putBoolean("targetsFound", self.limelight.valid_targets)
        wpilib.SmartDashboard.putNumber("shooterSpeedTarget", abs(self.motor_rpm))
        wpilib.SmartDashboard.putNumber("shooterMotorSpeed", abs(self.motor.rpm))
        wpilib.SmartDashboard.putNumber(
            "shooterOutput", self.motor.motor.getAppliedOutput()
        )
