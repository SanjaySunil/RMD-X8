# RMD-X8 Python Library

> Python library for complete control over RMD-X8 and RMD-X8 Pro motors.

## Install
```sh
pip install rmd_x8
```

## Usage
```py
from rmd_x8 import RMD_X8

# Setup a new RMD_X8 motor (motor identifier`]() 0x141)
robot = RMD_X8(0x141)

# Read the motor's current PID parameters.
robot.read_pid()
```

## API
### Contents

- [`setup()`]()
- [`send_cmd()`]()
- [`read_pid()`]()
- [`write_pid_ram()`]()
- [`write_pid_rom()`]()
- [`read_acceleration()`]()
- [`write_acceleration_ram()`]()
- [`read_encoder()`]()
- [`write_encoder_offset()`]()
- [`write_motor_zero_rom()`]()
- [`read_multi_turns_angle()`]()
- [`read_single_turn_angle()`]()
- [`motor_off()`]()
- [`motor_stop()`]()
- [`motor_running()`]()
- [`read_motor_status_1()`]()
- [`read_motor_status_2()`]()
- [`read_motor_status_3()`]()
- [`clear_motor_error_flag()`]()
- [`torque_closed_loop()`]()
- [`speed_closed_loop()`]()
- [`position_closed_loop_1()`]()
- [`position_closed_loop_2()`]()
- [`position_closed_loop_3()`]()
- [`position_closed_loop_4()`]()

## API