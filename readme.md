# ![703](docs/Phoenix2020.png) 2020 Robot

## Controls

### Standard Controls

| Action           | Control                      |
| ---------------- | ---------------------------- |
| Shoot            | Joystick Trigger             |
| Intake           | Joystick Bottom Axis Down/Up |
| Drive (Tank)     | Left And Right Joysticks     |
| Drive (Twist)    | Left Joystick, Twist Axis    |
| Drive (non-turn) | Left Joystick, X Axis        |

### Manual Controls

| Action           | Control                      |
| ---------------- | ---------------------------- |
| Manual Feed      | Joystick Button 4            |
| Reset Intake Arm | Joystick Button 7, 9, and 11 |

> The reset intake arm button should not be used in a competition unless the robot somehow loses power and the encoders get reset while the arm is down. It requires all 3 buttons to be pressed to prevent it from happening unless absolutely necessary

## Subsystems

### Drivetrain

The drivetrain uses two Rev NEOs for each side, geared together into a 10.71:1 gearbox.
We use six 6" 80A HiGrip wheels.

### Intake

The intake has a 100:1 versaplanetary attached to a Rev NEO to control the arm position. The arm is approximately 140:1 after the full gearing. This gives very high control over the exact position that the arm is in, while also allowing the entire control system for it to be placed in a small little gap.

There is a 775 pro mounted to the intake arm which consists of six 4" 35A Compliant wheels, as well as four 4" omni wheels on the edges to prevent jamming. More information about the intake control system can be found at [the intake state machine section](#Intake)

### Shooter

The shooter has a 1:3 geared flywheel attached to a Rev NEO to launch power cells.
The NEO uses a [PID loop](#Shooter-1) to maintain a constant speed to ensure accuracy between shots and varying battery levels. The flywheel for it uses two 4" 45A compliant wheels, spinning at approximately 14000 rpm.
(This will definitely be changed, the wheels will absolutely explode)

## Control System

### PID

#### Shooter

We use the built in NEO encoder and Velocity reference points to keep a constant speed on the shooter.

### State Machines

#### Intake

When the intake button is pushed, automatically move the arm down to its down position and start the wheels spinning inward at about 70 degrees.

Upon release, the wheels will stop spinning and the arm will move back to the vertical state.

#### Ball Counter

Uses the current reading from the Talon SRX that's running the intake motor to detect spikes in the current. It can be assumed that large spikes will be from the wheels grabbing the power cell.

Will most likely break when collecting more than one ball at a time. (To be fixed later)

#### Shoot

When the robot is commanded to shoot, first checks to see if there is a valid target in the vision of the limelight.
If there is a target, it will aim at it on the X axis and spin the shooter motor to the appropriate speed for the current distance.

### Vision

We're using a Limelight with the custom made [robotpy-limelight](https://github.com/FRC703/robotpy-limelight) library to make getting variables from it easier.
It integrates with the shooter, using the distance to adjust the speed that the flywheel spins.

> Note: Shooter hasn't been calibrated properly yet, will be using some measured points to generate coefficients for a (likely) cubic calibration curve to catch both ascending/descending halves of the curve.

## NetworkTables

### Drivetrain Network Tables Values

| Key                                   |         Type          | Description                                       |
| ------------------------------------- | :-------------------: | ------------------------------------------------- |
|                                       |  **SmartDashboard**   |                                                   |
| /SmartDashboard/forwardSpeed          |        Number         | The speed commanded for the robot to move forward |
| /SmartDashboard/turnSpeed             |        Number         | The speed commanded for the robot to turn         |
|                                       | **Magicbot Tunables** |                                                   |
| /components/drivetrain/vision_dist_kP |        Number         | P value of the distance PID                       |
| /components/drivetrain/vision_dist_kI |        Number         | I value of the distance PID                       |
| /components/drivetrain/vision_dist_kD |        Number         | D value of the distance PID                       |
| /components/drivetrain/vision_turn_kP |        Number         | P value of the turn PID                           |
| /components/drivetrain/vision_turn_kI |        Number         | I value of the turn PID                           |
| /components/drivetrain/vision_turn_kD |        Number         | D value of the turn PID                           |

### Intake Network Tables Values

| Key                         |        Type        | Description                                    |
| --------------------------- | :----------------: | ---------------------------------------------- |
|                             | **SmartDashboard** |                                                |
| /SmartDashboard/armPosition |       Number       | The current angle of the arm                   |
| /SmartDashboard/armPower    |       Number       | The current rpm of the arm motor               |
| /SmartDashboard/intakeIn    |      Boolean       | Whether or not the intake is currently running |
| /SmartDashboard/intakeSpeed |       Number       | The current intake motor output                |

### Shooter Network Tables Values

| Key                                     |         Type          | Description                                                                       |
| --------------------------------------- | :-------------------: | --------------------------------------------------------------------------------- |
|                                         |  **SmartDashboard**   |                                                                                   |
| /SmartDashboard/isAimed                 |        Boolean        | Whether or not the limelight target is within a certian tolerance                 |
| /SmartDashboard/shooterMotorSpeed       |        Number         | The current speed that the shooter flywheel is spinning at                        |
| /SmartDashboard/shooterOutput           |        Number         | The output percentage that the motor controller PID is outputting                 |
| /SmartDashboard/shooterReady            |        Boolean        | Whether or not the shooter is up to speed                                         |
| /SmartDashboard/shooterSpeedTarget      |        Number         | The target speed that the shooter should attempt to reach                         |
| /SmartDashboard/targetsFound            |        Boolean        | If the limelight can see a target                                                 |
|                                         | **Magicbot Tunables** |                                                                                   |
| /components/shooter/target_rpm          |        Number         | The target speed of the shooter                                                   |
| /components/shooter/feed_speed_setpoint |        Number         | The target speed of the feeder                                                    |
| /components/shooter/rpm_error           |        Number         | The amount that the shooter speed can be incorrect before it's considered invalid |
| /components/shooter/x_aim_error         |        Number         | The Limelight x aim offset                                                        |
| /components/shooter/y_aim_error         |        Number         | The Limelight y aim offset                                                        |
