# ![703](docs/703.png) 2020 Robot

## Controls

## Subsystems

### Intake

The intake has a 100:1 versaplanetary attached to a Rev NEO to control the arm position. The arm is approximately 140:1 after the full gearing. This gives very high control over the exact position that the arm is in, while also allowing the entire control system for it to be placed in a small little gap.

There is a 775 pro mounted to the intake arm which consists of six 4" 35A Compliant wheels, as well as four 4" omni wheels on the edges to prevent jamming. More information about the intake control system can be found at [the intake state machine section](Intake) 

## Control System

### State Machines

#### Intake

When the intake button is pushed, automatically move the arm down to its down position and start the wheels spinning inward at about 70 degrees.

Upon release, the wheels will stop spinning and the arm will move back to the vertical state.

#### Ball Counter

Uses the current reading from the Talon SRX that's running the intake motor to detect spikes in the current. It can be assumed that large spikes will be from the wheels grabbing the power cell.

Will most likely break when collecting more than one ball at a time. (To be fixed later)