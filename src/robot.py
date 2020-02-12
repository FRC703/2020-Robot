import wpilib
import wpilib.drive
import magicbot
import math
from limelight import limelight

import ctre
import rev
from controllers.PIDSparkMax import PIDSparkMax

from components.intake import Intake
from components.shooter import Shooter
from components.drivetrain import Drivetrain

from state_machines.shoot import Shoot
from state_machines.intake_routine import IntakeRoutine
from state_machines.intake_lift_routine import IntakeLiftRoutine

from wpilib import SmartDashboard
from networktables import NetworkTables


class Robot(magicbot.MagicRobot):
    # State Machines
    intake_sm: IntakeRoutine
    # intake_lift_sm: IntakeLiftRoutine
    shoot_sm: Shoot

    # Components
    intake: Intake
    shooter: Shooter
    drivetrain: Drivetrain


    # Dashboard config
    tank_drive = magicbot.tunable(False)
    twist = magicbot.tunable(True)

    def shuffleboardInit(self):
        pass

    def createObjects(self):
        self.intake_motor = ctre.TalonSRX(10)
        self.shooter_motor = PIDSparkMax(16)
        self.intake_arm_motor = PIDSparkMax(8)
        self.shooter_motor.motor.setOpenLoopRampRate(1)
        self.drivetrain_motorr1 = rev.CANSparkMax(5, rev.MotorType.kBrushless)
        self.drivetrain_motorr2 = rev.CANSparkMax(13, rev.MotorType.kBrushless)
        self.drivetrain_motorl1 = rev.CANSparkMax(7, rev.MotorType.kBrushless)
        self.drivetrain_motorl2 = rev.CANSparkMax(17, rev.MotorType.kBrushless)
        self.drivetrain_motorr2.follow(self.drivetrain_motorr1)
        self.drivetrain_motorl2.follow(self.drivetrain_motorl1)


        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)


    def teleopPeriodic(self):
        if self.tank_drive:
            self.drivetrain.tankDrive(self.joystick_left.getRawAxis(1), self.joystick_right.getRawAxis(2))
        else:
            self.drivetrain.arcadeDrive(-self.joystick_left.getRawAxis(1), self.joystick_left.getRawAxis(0), self.joystick_left.getRawAxis(2))
        if self.joystick_left.getRawButton(1):
            self.intake_sm.engage()
        else:
            # self.intake_lift_sm.engage()
            self.intake.lift()
        if self.joystick_left.getRawButton(11):
            self.intake.reset_arm_encoders()
        if self.joystick_left.getRawButton(3):
            # self.shoot_sm.engage()
            self.shooter.shoot()


if __name__ == "__main__":
    wpilib.run(Robot)
