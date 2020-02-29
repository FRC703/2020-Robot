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
            y = limelight_data[1]
            y_target = y
            if y - 10 > y + 3.5:
                if abs(y + 3.5) < 3:
                    y_target = -3.5
            else:
                if abs(y - 10) < 3:
                    y_target = 10
                
            self.drivetrain.vision_aim(*limelight_data)
            if self.shooter.is_aimed:
                self.next_state("shoot")
        else:
            self.next_state("no_targets")

    @state
    def shoot(self):
        if not self.shooter.is_aimed:
            self.next_state("track")
        else:
            self.shooter.shoot()
