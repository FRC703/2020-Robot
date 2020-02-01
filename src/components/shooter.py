from limelight import limelight
from magicbot import will_reset_to, tunable
from rev import CANSparkMax

class Shooter:
    # limelight: limelight.Limelight

    limelight_state = will_reset_to(1)
    motor_rpm = will_reset_to(0)
    target_rpm = tunable(-.75)
    motor: CANSparkMax

    def setup(self):
        self.limelight = limelight.Limelight()

    def aim(self):
        # print("LIMELIGHT DOING THINGS")
        self.limelight_state = 3

    def shoot(self):
        self.motor_rpm = self.target_rpm
    
    def execute(self):
        # print(f'Execute limelight {self.limelight_state}')
        self.limelight.light(self.limelight_state)
        self.motor.set(self.motor_rpm)