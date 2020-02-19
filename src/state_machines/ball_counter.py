from magicbot.state_machine import StateMachine, state, timed_state
from magicbot import tunable

from components.intake import Intake


class CounterFSM(StateMachine):
    """
    This state machine will continuously watch the current of the
    intake motor, watching to see if any power cells are being
    loaded, based off the spikes in current draw. If multiple cells
    are grabbed, it will likely only count it as one.
    If the intake is not running, the current will not be watched.
    """

    intake: Intake
    ball_count: int

    balanced_zone = tunable(1)
    spike_zone = tunable(2)

    @state(first=True)
    def watch_intake_state(self):
        """
        Watch the intake to wait for it to become enabled.
        Once enabled, wait for the motor controller to read
        a current deadzone that can be detected as the motor
        being at the correct speed.
        """
        if abs(self.intake.intake_speed) > 0.2:
            self.next_state("intake_running_ignore_current")

    @state()
    def intake_running_ignore_current(self):
        """
        Wait for the motor controller to read a current deadzone
        that can be detected as the motor being at the correct speed.
        
        If the intake is stopped partway through this, move back to
        the main state.
        """
        if abs(self.intake.intake_speed) < 0.2:
            self.next_state("watch_intake_state")
        if self.intake.motor.getOutputCurrent() < self.balanced_zone:
            self.next_state("intake_running")

    @state()
    def intake_running(self):
        """
        Increment the ball count if a spike in current is detected.
        It is very likely that when the motor spikes in current,
        a ball has touched the motors, causing the motor to slightly
        torque itself, drawing more current.

        If the intake is stopped partway through this, move back to
        the main state.
        """
        if abs(self.intake.intake_speed) < 0.2:
            self.next_state("watch_intake_state")
        if self.intake.motor.getOutputCurrent() > self.spike_zone:
            ball_count += 1
            self.next_state("intake_running_ingore_current")
