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

    @timed_state(first=True, duration=8, next_state="reverse")
    def shoot(self):
        self.shooter.shoot()

    @timed_state(duration=2)
    def reverse(self):
        self.intake_sm.engage()
        self.drivetrain.arcadeDrive(-0.5, 0, 0)
