import wpilib
import wpilib.drive
import magicbot
import math
from limelight import limelight

import ctre
from controllers.PIDSparkMax import PIDSparkMax

from components.intake import Intake
from components.shooter import Shooter
from state_machines.shoot import Shoot

from networktables import NetworkTables


class Robot(magicbot.MagicRobot):

    intake: Intake
    shooter: Shooter
    shoot_procedure: Shoot

    def createObjects(self):
        self.intake_motor = ctre.TalonSRX(10)
        self.shooter_motor = PIDSparkMax(7)
        # self.shooter_motor.setOpenLoopRampRate(1)

        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        self.intake.intake(self.joystick.getRawAxis(3))
        if self.joystick.getRawButton(1):
            # self.shoot_procedure.fire()
            self.shooter.shoot()


if __name__ == "__main__":
    wpilib.run(Robot)
