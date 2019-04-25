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
    Initialize i2c address and get board information.

    :param address: i2c address
    :type address: int
    """

    def __init__(self, address, volts):
        # create SMBus
        self._bus = SMBus(1)
        # i2c address (int)
        self._address = address
        # volts (EU: 230)
        self._volts = volts
        # get board parameters
        self._ident_sensors()

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
        data = self.__read_block(self._address, 85, 3)
        # Type of Sensor
        self.board = data[0]
        # Maximum Current
        self.max_current = data[1]
        # No. of Channels
        self.channels = data[2]

    def read_current(self):
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
        return self.__read_block(self._address, 85, self.channels * 3)

    def print_all_currents(self):
        """ print readable data for all sensors """
        data = self.read_current()
        for i in range(0, self.channels):
            # Convert the data to ampere
            current = self.__compute_current(i, data)

            # Output data to screen
            print("Channel no : %d " % (i + 1))
            print("Current Value : %.3f A" % current)
            print("Watt Value : %.3f W" % current * self._volts)

    def get_one_current(self, number):
        """ get one current in single value first channel is 0 """
        if number <= self.channels:
            data = self.read_current()
            return self.__compute_current(number, data)

    def board_info(self):
        print("Type of Sensor : %d" % self.board)
        print("Maximum Current : %d A" % self.max_current)
        print("No. of Channels : %d" % self.channels)

    @staticmethod
    def __compute_current(idx, data):
        msb1 = data[idx * 3]
        msb = data[1 + idx * 3]
        lsb = data[2 + idx * 3]
        return (msb1 * 65536 + msb * 256 + lsb) / 1000.0

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
    def __checksum(register, cmd):
        checksum = sum(cmd)
        checksum += register
        if checksum > 255:
            checksum = checksum & 255
        return checksum
