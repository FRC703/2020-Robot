from magicbot.state_machine import StateMachine, timed_state, default_state, state

from components.intake import Intake


class IntakeRoutine(StateMachine):
    intake: Intake

    @state(first=True)
    def arm_down(self):
        """
        Puts the arm down without running the wheels.
        After the arm is at 70 degrees, the wheels_on state will run
        """
        self.intake.lower()
        if self.intake.arm_position > self.intake.intake_arm_motor_on_position:
            self.next_state("wheels_on")

    @state()
    def wheels_on(self):
        """
        Puts the arm down and runs the wheels
        """
        self.intake.run_wheels()
        self.intake.lower()
