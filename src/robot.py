import math

import wpilib
import wpilib.drive
from wpilib import SmartDashboard
from rev import CANSparkMax, MotorType
import ctre

import magicbot
from limelight import limelight
from controllers.PIDSparkMax import PIDSparkMax

from components.intake import Intake
from components.shooter import Shooter
from components.drivetrain import Drivetrain

from state_machines.shoot_routine import ShootRoutine
from state_machines.intake_routine import IntakeRoutine
from state_machines.ball_counter import CounterFSM

from networktables import NetworkTables

from controls import Controls


class Robot(magicbot.MagicRobot):
    # State Machines
    intake_sm: IntakeRoutine
    shoot_sm: ShootRoutine
    ball_counter_sm: CounterFSM

    # Components
    intake: Intake
    shooter: Shooter
    drivetrain: Drivetrain

    ball_count = 0

    # Dashboard config
    tank_drive = False
    twist = True

    camera_state = 1

    def shuffleboardInit(self):
        pass

    def disabledPeriodic(self):
        self.shooter.limelight_state = 1
        self.shooter.limelight.light(1)

    def createObjects(self):
        self.intake_motor = ctre.TalonSRX(10)
        self.intake_arm_motor = PIDSparkMax(7)

        self.shooter_motor = PIDSparkMax(16)
        self.shooter_feeder_motor = ctre.TalonSRX(19)

        self.drivetrain_motorr1 = CANSparkMax(5, MotorType.kBrushless)
        self.drivetrain_motorr2 = CANSparkMax(8, MotorType.kBrushless)
        self.drivetrain_motorl1 = CANSparkMax(17, MotorType.kBrushless)
        self.drivetrain_motorl2 = CANSparkMax(13, MotorType.kBrushless)

        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        self.controls = Controls(self.joystick_left, self.joystick_right)

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("ballCount", self.ball_count)

    def teleopInit(self):
        self.intake.lift()

    def teleopPeriodic(self):
        # self.ball_counter_sm.engage()

        self.handle_drive(self.controls)
        self.handle_intake(self.controls)
        self.handle_shooter(self.controls)

    # Subsystem handlers
    def handle_drive(self, controls: Controls):
        """
        Runs the control systems 
        """
        if self.tank_drive:
            self.drivetrain.tankDrive(
                controls.tank_drive_left, controls.tank_drive_right
            )
        else:
            self.drivetrain.arcadeDrive(
                controls.arcade_drive_forward,
                controls.arcade_drive_turn,
                controls.arcade_drive_twist,
            )

    def handle_intake(self, controls: Controls):
        if controls.intake:
            self.intake_sm.engage()
        else:
            self.intake.lift()
        if controls.reset_intake_arm_to_down:
            self.intake.reset_arm_encoders()

    def handle_shooter(self, controls: Controls):
        if controls.shoot:
            # self.shoot_sm.fire()
            self.shooter.shoot()
        if controls.feed:
            self.shooter.feed()
        if controls.aim:
            self.drivetrain.vision_aim(*self.shooter.aim())

    def handle_vision(self, controls: Controls):
        if controls.toggle_camera:
            self.camera_state = 1 if self.camera_state else 0
            self.shooter.limelight.pipeline(self.camera_state)


if __name__ == "__main__":
    wpilib.run(Robot)
