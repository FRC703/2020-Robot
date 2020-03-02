from magicbot import AutonomousStateMachine
from magicbot.state_machine import timed_state

from components.drivetrain import Drivetrain
from components.shooter import Shooter

from state_machines.intake_routine import IntakeRoutine


class Basic(AutonomousStateMachine):

    MODE_NAME = "ShootReverse"
    DEFAULT = True

    drivetrain: Drivetrain
    shooter: Shooter
    intake_sm: IntakeRoutine

    @timed_state(first=True, duration=2, next_state="shoot")
    def aim(self):
        self.shooter.limelight_state = 3
        limelight_data = self.shooter.aim()
        self.drivetrain.vision_aim(*limelight_data)

    @timed_state(duration=8, next_state="reverse")
    def shoot(self):
        self.shooter.shoot()

    @timed_state(duration=2, next_state="stop")
    def reverse(self):
        self.shooter.limelight_state = 1
        # self.intake_sm.engage()
        self.drivetrain.arcadeDrive(-0.5, 0, 0)

    @state
    def stop(self):
        self.drivetrain.arcadeDrive(0, 0, 0)
        

