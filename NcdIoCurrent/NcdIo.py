"""
Identify and read current from devices: https://store.ncd.io/
Inspiration from: https://github.com/ControlEverythingCommunity/PECMAC
"""
import os
import sys
import time
from smbus2 import SMBus


class NcdIo:
    """
    Get values from PECMAC current board

    :param address: i2c address
    :type address: int
    :param volts: single phase voltage
    :type volts: int
    """
    # Type of Sensor
    board = 0
    # Maximum Current
    max_current = 0
    # No. of Channels
    channels = 0
    # firmware revision
    firmware = 0
    # single phase volts
    volts = 0
    # i2c address
    _address = 0
    # lock read current
    _lock = False

    def __init__(self, address, volts):
        # create SMBus
        self._bus = SMBus(1)
        # i2c address (int)
        self._address = address
        # volts (EU: 230)
        self.volts = volts
        # get board parameters
        self._ident_sensors()
        #

    def read_current(self):
        """ Read all current.
            For use function in multithreading
            is protected for parallel call
            TODO: better is test checksum from read data ?
        """
        if not self._lock:
            self._lock = True
            # Command for reading current
            # 0x6A(106), 0x01(1), 0x01(1),0x0C(12), 0x00(0), 0x00(0) 0x0A(10)
            # Header byte-2, command-1, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
            cmd = [106, 1, 1, self.channels, 0, 0]
            register = 146
            cmd.append(self.__checksum(register, cmd))
            self.__write_block(self._address, register, cmd)
            time.sleep(0.5)

            # Read data back from 0x55(85), No. of Channels * 3 bytes
            # current MSB1, current MSB, current LSB
            data = self.__read_block(self._address, 85, self.channels * 3)
            self._lock = False
            return data
        raise Warning

    def print_currents(self):
        """ print readable data for all sensors """
        try:
            data = self.read_current()
            for i in range(0, self.channels):
                # Convert the data to ampere
                current = self.compute_current(i, data)

                # Output data to screen
                print("Channel no : %d " % (i + 1))
                print("Current Value : %.3f A" % current)
                print("Watt Value : %.1f W" % (current * self.volts))
        except Warning:
            print('busy')

    def get_one_current(self, channel):
        """ get one current value, first channel is 0 """
        if channel <= self.channels:
            try:
                data = self.read_current()
                return self.compute_current(channel, data)
            except Warning:
                return 'busy'

    def get_one_watt(self, channel):
        """ get one watt value, first channel is 0 """
        current = self.get_one_current(channel)
        return current * self.volts

    def read_calibration_values(self):
        # Command for reading calibration values
        # 146,106,3,1,3,0,0,3
        # Header byte-2, command-1, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
        cmd = [106, 3, 1, self.channels, 0, 0]
        register = 146
        cmd.append(self.__checksum(register, cmd))
        self.__write_block(self._address, register, cmd)
        time.sleep(0.5)

        # Read data back from 0x55(85), No. of Channels * 2 bytes
        # current MSB, current LSB
        return self.__read_block(self._address, 85, self.channels * 2)

    def print_calibration(self):
        """ print calibration data for all sensors """
        data = self.read_calibration_values()
        for i in range(0, self.channels):
            # Convert the data
            msb = data[i * 2]
            lsb = data[1 + i * 2]
            calibration = (msb * 256 + lsb)

            # Output data to screen
            print("Channel no : %d " % (i + 1))
            print("Calibration Value : %d" % calibration)

    def board_info(self):
        print("Type of Sensor : %d" % self.board)
        print("Maximum Current : %d A" % self.max_current)
        print("No. of Channels : %d" % self.channels)

    def _ident_sensors(self):
        # Command for reading device identification data
        # 0x6A(106), 0x02(2), 0x00(0),0x00(0), 0x00(0) 0x00(0), 0xFE(254)
        # Header byte-2, command-2, byte 3, 4, 5 and 6 are reserved, checksum
        cmd = [106, 2, 0, 0, 0, 0]
        register = 146
        cmd.append(self.__checksum(register, cmd))
        self.__write_block(self._address, register, cmd)
        time.sleep(0.5)

        # Read data back from 0x55(85), 3 bytes
        # Type of Sensor, Maximum Current, No. of Channels
        data = self.__read_block(self._address, 85, 4)
        self.board = data[0]
        self.max_current = data[1]
        self.channels = data[2]
        self.firmware = data[3]

    def __write_block(self, address, register, cmd):
        try:
            self._bus.write_i2c_block_data(address, register, cmd)
        except OSError as e:
            print("Write block error: %s" % e)
            sys.exit(os.EX_OSERR)

    def __read_block(self, address, register, length):
        try:
            return self._bus.read_i2c_block_data(address, register, length)
        except OSError as e:
            print("Write block error: %s" % e)
            sys.exit(os.EX_OSERR)

    @staticmethod
    def compute_current(idx, data):
        msb1 = data[idx * 3]
        msb = data[1 + idx * 3]
        lsb = data[2 + idx * 3]
        return (msb1 * 65536 + msb * 256 + lsb) / 1000.0

    @staticmethod
    def __checksum(register, cmd):
        checksum = sum(cmd)
        checksum += register
        if checksum > 255:
            checksum = checksum & 255
        return checksum
