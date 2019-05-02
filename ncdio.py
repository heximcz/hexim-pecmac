import fire
from NcdIoCurrent import NcdIo
from LCD1602 import LCD1602
from Zabbix import ZabbixRead
from Exceptions import NcdIoException


class CurrentAndWatt:

    @staticmethod
    def run():
        """ run thread """
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        # dev.board_info()
        # dev.print_currents()
        # dev.print_calibration()
        # dev.get_one_current(0)
        # dev.get_one_watt(0)
        try:
            lcd = LCD1602(dev)
        except NcdIoException as e:
            print(e)
            return
        # lcd.run() is multithreading process
        lcd.run()

    @staticmethod
    def board_info():
        """ get board information """
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        dev.board_info()

    @staticmethod
    def get_currents():
        """ get and print all currents """
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        dev.print_currents()

    @staticmethod
    def zbx_get_current(phase):
        """ get current for one phase, zabbix agent call """
        zabbix = ZabbixRead()
        print(zabbix.get_current(phase))

    @staticmethod
    def zbx_get_watt(phase):
        """ get wats for one phase, zabbix agent call """
        zabbix = ZabbixRead()
        print(zabbix.get_watts(phase))


if __name__ == '__main__':
    fire.Fire(CurrentAndWatt)
