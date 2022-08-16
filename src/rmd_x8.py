# RMD-X8 Python Library
# Copyright 2022 Sanjay Sunil

import can
import os
import time


class RMD_X8:
    """
    A class to read and write on the RMD-X8 motor.

    ...

    Attributes
    ----------
    bus : type
        the can bus channel used to communicate with the motor
    identifier : type
        the motor's identifier on the can bus

    Methods
    -------
    setup():
        Setup the can bus connection.
    send_cmd(data, delay):
        Send a frame data to the motor.
    read_pid():
        Read the motor's current PID parameters.
    write_pid_ram(data):
        Write PID parameters to the RAM.
    write_pid_rom(data):
        Write PID parameters to the ROM.
    read_acceleration():
        Read the motor's acceleration data.
    write_acceleration_ram(data):
        Write the acceleration to the RAM of the motor.
    read_encoder():
        Read the current position of the encoder.
    write_encoder_offset(data):
        Set the motor's encoder offset.
    write_motor_zero_rom():
        Write the current position of the motor to the ROM 
        as the motor zero position.
    read_multi_turns_angle():
        Read the multi-turn angle of the motor.
    read_single_turn_angle():
        Read the single circle angle of the motor.
    motor_off():
        Turn off the motor, while clearing the motor operating 
        status and previously received control commands.
    motor_stop():
        Stop the motor, but do not clear the operating state and 
        previously received control commands.
    motor_running():
        Resume motor operation from the motor stop command.
    read_motor_status_1():
        Reads the motor's error status, voltage, temperature and 
        other information. 
    read_motor_status_2():
        Reads the motor temperature, voltage, speed and encoder 
        position.
    read_motor_status_3():
        Reads the phase current status data of the motor.
    clear_motor_error_flag():
        Clears the error status of the currrent motor.
    torque_closed_loop(data):
        Control torque current output of the motor.
    speed_closed_loop(data):
        Control the speed of the motor.
    position_closed_loop_1(data):
        Control the position of the motor (multi-turn angle).
    position_closed_loop_2(data):
        Control the position of the motor (multi-turn angle).
    position_closed_loop_3(data):
        Control the position of the motor (single-turn angle).
    position_closed_loop_4(data):
        Control the position of the motor (single-turn angle).
    """

    def __init__(self, identifier):
        """
        Constructs all the necessary attributes for the RMDX8 object.
        """
        self.bus = None
        self.identifier = identifier

    def setup(self):
        """
        Setup the can bus connection.

        Returns
        -------
        self.bus : type
            The bus used to communicate with the motor.
        """
        try:
            os.system("sudo /sbin/ip link set can0 up type can bitrate 1000000")
            time.sleep(0.1)
        except Exception as e:
            print(e)

        try:
            bus = can.interface.Bus(bustype='socketcan_native', channel='can0')
        except OSError:
            print('err: PiCAN board was not found.')
            exit()
        except Exception as e:
            print(e)

        self.bus = bus
        return self.bus

    def send_cmd(self, data, delay):
        """
        Send frame data to the motor.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.
        delay : int/float
            The time to wait after sending data to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = can.Message(arbitration_id=self.identifier,
                              data=data, extended_id=False)
        self.bus.send(message)
        time.sleep(delay)
        received_message = self.bus.recv()
        return received_message

    def read_pid(self):
        """
        Read the motor's current PID parameters.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def write_pid_ram(self, data):
        """
        Write PID parameters to the RAM.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x31, 0x00, data[0], data[1],
                   data[2], data[3], data[4], data[5]]
        return self.send_cmd(message, 0.01)

    def write_pid_rom(self, data):
        """
        Write PID parameters to the ROM.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x32, 0x00, data[0], data[1],
                   data[2], data[3], data[4], data[5]]
        return self.send_cmd(message, 0.01)

    def read_acceleration(self):
        """
        Read the motor's acceleration data.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x33, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def write_acceleration_ram(self, data):
        """
        Write the acceleration to the RAM of the motor.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x34, 0x00, 0x00, 0x00,
                   data[0], data[1], data[2], data[3]]
        return self.send_cmd(message, 0.01)

    def read_encoder(self):
        """
        Read the current position of the encoder.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def write_encoder_offset(self, data):
        """
        Set the motor's encoder offset.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x91, 0x00, 0x00, 0x00,
                   0x00, 0x00, data[0], data[1]]
        return self.send_cmd(message, 0.01)

    def write_motor_zero_rom(self):
        """
        Write the current position of the motor to the ROM as the motor zero position.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x19, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def read_multi_turns_angle(self):
        """
        Read the multi-turn angle of the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x92, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def read_single_turn_angle(self):
        """
        Read the single circle angle of the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x94, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def motor_off(self):
        """
        Turn off the motor, while clearing the motor operating status and previously received control commands.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x80, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def motor_stop(self):
        """
        Stop the motor, but do not clear the operating state and previously received control commands.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x81, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def motor_run(self):
        """
        Resume motor operation from the motor stop command.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x88, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def read_motor_status_1(self):
        """
        Reads the motor's error status, voltage, temperature and other information.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x9A, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def read_motor_status_2(self):
        """
        Reads the motor temperature, voltage, speed and encoder position.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x9C, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def read_motor_status_3(self):
        """
        Reads the phase current status data of the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x9D, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def clear_motor_error_flag(self):
        """
        Clears the error status of the currrent motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0x9B, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def torque_closed_loop(self, data):
        """
        Control torque current output of the motor.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA1, 0x00, 0x00, 0x00,
                   data[0], data[1], 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def speed_closed_loop(self, data):
        """
        Control the speed of the motor.

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA2, 0x00, 0x00, 0x00,
                   data[0], data[1], data[2], data[3]]
        return self.send_cmd(message, 0.01)

    def position_closed_loop_1(self, data):
        """
        Control the position of the motor (multi-turn angle).

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA3, 0x00, 0x00, 0x00,
                   data[0], data[1], data[2], data[3]]
        return self.send_cmd(message, 0.01)

    def position_closed_loop_2(self, data):
        """
        Control the position of the motor (multi-turn angle).

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA4, 0x00, data[0], data[1],
                   data[2], data[3], data[4], data[5]]
        return self.send_cmd(message, 0.01)

    def position_closed_loop_3(self, data):
        """
        Control the position of the motor (single-turn angle).

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA5, data[0], 0x00, 0x00,
                   data[1], data[2], 0x00, 0x00]
        return self.send_cmd(message, 0.01)

    def position_closed_loop_4(self, data):
        """
        Control the position of the motor (single-turn angle).

        Parameters
        ----------
        data : list
            The frame data to be sent to the motor.

        Returns
        -------
        received_message : list
            Frame data received from the motor after receiving the command.
        """
        message = [0xA6, data[0], data[1], data[2],
                   data[3], data[4], 0x00, 0x00]
        return self.send_cmd(message, 0.01)
