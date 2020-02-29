from magicbot.state_machine import StateMachine, timed_state, default_state, state

from components.shooter import Shooter
from components.drivetrain import Drivetrain


class ShootRoutine(StateMachine):
    shooter: Shooter
    drivetrain: Drivetrain

    def fire(self):
        self.engage()

    @state(first=True)
    def no_targets(self):
        """
        Test for a valid target, but don't try aiming
        """
        self.shooter.aim()
        if self.shooter.limelight.valid_targets:
            self.next_state("track")

    @state
    def track(self):
        if self.shooter.limelight.valid_targets:
            limelight_data = self.shooter.aim()
            self.drivetrain.vision_aim(*limelight_data)
            if self.shooter.is_aimed:
                self.next_state("backdrive")
        else:
            self.next_state("no_targets")

    @timed_state(duration=.5, next_state="shoot")
    def backdrive(self):
        self.shooter.backdrive()

    @state
    def shoot(self):
        if not self.shooter.is_aimed:
            self.next_state("track")
        else:
            self.shooter.shoot()
