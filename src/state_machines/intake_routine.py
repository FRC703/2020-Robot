from magicbot.state_machine import StateMachine, timed_state, default_state, state

from components.intake import Intake

class IntakeRoutine(StateMachine):
    intake: Intake

    @state(first=True)
    def arm_down(self):
        self.intake.lower()
        if(self.intake.arm_motor.motor.getEncoder().getPosition() > 20):
            self.next_state("wheels_on")
    
    @state()
    def wheels_on(self):
        self.intake.run_wheels()
        self.intake.lower()