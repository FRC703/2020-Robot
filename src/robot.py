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


from networktables import NetworkTables


class Robot(magicbot.MagicRobot):

    intake: Intake
    # shooter: Shooter
    drivetrain: Drivetrain
    # shoot_procedure: Shoot
    intake_sm: IntakeRoutine

    def createObjects(self):
        self.intake_motor = ctre.TalonSRX(10)
        # self.shooter_motor = PIDSparkMax(9)
        self.intake_arm_motor = PIDSparkMax(8)
        # self.shooter_motor.setOpenLoopRampRate(1)
        self.drivetrain_motorr1 = rev.CANSparkMax(5, rev.MotorType.kBrushless)
        self.drivetrain_motorr2 = rev.CANSparkMax(13, rev.MotorType.kBrushless)
        self.drivetrain_motorl1 = rev.CANSparkMax(7, rev.MotorType.kBrushless)
        self.drivetrain_motorl2 = rev.CANSparkMax(17, rev.MotorType.kBrushless)
        self.drivetrain_motorr2.follow(self.drivetrain_motorr1)
        self.drivetrain_motorl2.follow(self.drivetrain_motorl1)


        self.joystick = wpilib.Joystick(0)


    def teleopPeriodic(self):
        self.drivetrain.arcadeDrive(-self.joystick.getRawAxis(1), self.joystick.getRawAxis(0))
        if self.joystick.getRawButton(1):
            self.intake_sm.engage()
        else:
            self.intake.lift()
        if self.joystick.getRawButton(11):
            self.intake.reset_arm_encoders()


if __name__ == "__main__":
    wpilib.run(Robot)
