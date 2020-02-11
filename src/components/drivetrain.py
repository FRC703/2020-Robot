import wpilib
import wpilib.drive
import rev

class Drivetrain:
    motorr1: rev.CANSparkMax
    motorr2: rev.CANSparkMax
    motorl1: rev.CANSparkMax
    motorl2: rev.CANSparkMax
    
    def setup(self):
        self.drive = wpilib.drive.DifferentialDrive(self.motorl1, self.motorr1)

    def arcadeDrive(self, forward, turn):
        self.forward = forward
        self.turn = turn

    def execute(self):
        self.drive.arcadeDrive(self.forward, self.turn)