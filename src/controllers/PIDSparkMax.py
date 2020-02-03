from rev import CANSparkMax, ControlType, MotorType


class PIDSparkMax:

    kP = .2 # 6e-2
    kI = 0 # 1e-3
    kD = 0 # 0.2
    kIz = 0
    kFF = 0.000015
    kMinOutput = -1
    kMaxOutput = 1

    def __init__(self, canid):
        self.motor = CANSparkMax(canid, MotorType.kBrushless)
        self.motor.setClosedLoopRampRate(1)
        self._motor_pid = self.motor.getPIDController()
        self._motor_pid.setP(self.kP)
        self._motor_pid.setI(self.kI)
        self._motor_pid.setD(self.kD)
        self._motor_pid.setIZone(self.kIz)
        self._motor_pid.setFF(self.kFF)
        self._motor_pid.setOutputRange(self.kMinOutput, self.kMaxOutput)

    def set(self, rpm):
        self._motor_pid.setReference(rpm, ControlType.kVelocity)

    @property
    def rpm(self):
        return self.motor.getEncoder().getVelocity()

    def stop(self):
        self._motor_pid.setReference(0, ControlType.kVelocity)
