from magicbot.state_machine import StateMachine, timed_state, default_state, state

from components.intake import Intake


class IntakeLiftRoutine(StateMachine):
    intake: Intake

    @state(first=True)
    def arm_down(self):
        self.intake.run_wheels()
        self.intake.lift()
        if self.intake.arm_motor.motor.getEncoder().getPosition() < 10:
            self.next_state("wheels_off")

    @state()
    def wheels_off(self):
        self.intake.lift()
