import os
import sys
import time
from Zabbix import ZabbixFile


class ZabbixRead:
    """ Read and get values from zabbix file. """

    def __init__(self):
        self.zbx = ZabbixFile()
        self.__read_file()
        self.sensors = len(self.data)

    def get_current(self, phase):
        self.__check_phase(phase)
        return self.data['F'+str(phase)]['ampere']

    def get_watts(self, phase):
        self.__check_phase(phase)
        return self.data['F'+str(phase)]['watt']

    def __check_phase(self, phase):
        if phase > self.sensors:
            print('Phase number is over the range.')
            sys.exit(os.EX_DATAERR)

    def __read_file(self):
        """ primitive double check read file"""
        self.data = self.zbx.read()
        if self.data:
            return
        # if False (file may by writen by another process in this time), wait and try one more read
        time.sleep(2)
        self.data = self.zbx.read()
