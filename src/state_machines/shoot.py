from magicbot.state_machine import StateMachine, timed_state, default_state, state

from components.shooter import Shooter

class Shoot(StateMachine):
    shooter: Shooter

    def fire(self):
        self.engage()

    @timed_state(first=True, duration=.5, next_state="shoot")
    def track(self):
        print('Shooting')
        self.shooter.aim()

    @timed_state(duration=4)
    def shoot(self):
        self.shooter.shoot()
