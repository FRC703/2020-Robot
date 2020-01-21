import wpilib
import magicbot

import rev

from components.drivetrain import Drivetrain

class Robot(magicbot.MagicRobot):

    train: Drivetrain

    def setupComponents(self):
        motorl1 = rev.CANSparkMax(5, rev.MotorType.kBrushless)
        motorl2 = rev.CANSparkMax(6, rev.MotorType.kBrushless)
        motorr1 = rev.CANSparkMax(7, rev.MotorType.kBrushless)
        motorr2 = rev.CANSparkMax(8, rev.MotorType.kBrushless)

        motorl2.follow(motorl1)
        motorr2.follow(motorr1)
        self.train_dt = wpilib.DifferentialDrive(motorl1, motorr1)

        self.joystick = wpilib.Joystick(0)


    def teleopPeriodic(self):
        self.train.drive(self.joystick.getRawInput(0), self.joystick.getRawInput(1))

if __name__ == "__main__":
    wpilib.run(Robot)
