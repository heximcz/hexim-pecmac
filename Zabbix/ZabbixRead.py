import os
import sys
from Zabbix import ZabbixFile


class ZabbixRead:
    """ Read and get values from zabbix file. """

    def __init__(self):
        zbx = ZabbixFile()
        self.data = zbx.read()
        self.sensors = len(self.data)

    def get_current(self, phase):
        self.__check_phase(phase)
        return self.data['F'+str(phase)]['ampere']

    def get_watts(self, phase):
        self.__check_phase(phase)
        return self.data['F'+str(phase)]['watt']

    def __check_phase(self, phase):
        if phase <= self.sensors:
            print('Phase number is over the range.')
            sys.exit(os.EX_DATAERR)
