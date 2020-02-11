import ctre
from controllers.PIDSparkMax import PIDSparkMax
import wpilib

import rev
from magicbot import will_reset_to, tunable


class Intake:

    motor: ctre.TalonSRX
    arm_motor: PIDSparkMax
    intake_speed = 0
    intake_speed_in = tunable(-.6)
    intake_speed_out = tunable(.1)
    intake_up = True
    intake_arm_down_position = 25 * 1.4 # Temporary to figure out the direction

    intake_arm_position_setpoint = will_reset_to(0)

    def setup(self):
        self.arm_motor.control_mode = rev.ControlType.kPosition
        self.arm_motor.motor.getEncoder().setPosition(0)
        self.arm_motor.motor.setSmartCurrentLimit(10)
        self.arm_motor._motor_pid.setP(.035)
        self.arm_motor._motor_pid.setI(.01)
        self.arm_motor._motor_pid.setD(.001)
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
    
    def execute(self):
        if self.intake_up:
            self.arm_motor.set(0)
        else:
            self.arm_motor.set(self.intake_arm_down_position)
        self.motor.set(ctre.ControlMode.PercentOutput, self.intake_speed)
        wpilib.SmartDashboard.putNumber("intakeSpeed", self.intake_speed)
        wpilib.SmartDashboard.putBoolean("intakeIn", self.intake_speed < -.1)
        wpilib.SmartDashboard.putNumber("armPosition", self.arm_motor.motor.getEncoder().getPosition())
        wpilib.SmartDashboard.putNumber("armPower", self.arm_motor.rpm)
        self.intake_speed = 0