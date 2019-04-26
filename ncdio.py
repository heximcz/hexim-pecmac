import fire
from NcdIoCurrent import NcdIo
from LCD1602 import LCD1602
from Zabbix import ZabbixRead


class CurrentAndWatt:

    @staticmethod
    def run():
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        # dev.board_info()
        # dev.print_currents()
        # dev.print_calibration()
        # print()
        # dev.get_one_current(0)
        # print()
        # dev.get_one_watt(0)
        lcd = LCD1602(dev)
        # lcd.run() is multithreading process, be carefully
        lcd.run()

    @staticmethod
    def board_info():
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        dev.board_info()

    @staticmethod
    def get_currents():
        i2c_address = 42
        volts = 230
        dev = NcdIo(i2c_address, volts)
        dev.print_currents()

    @staticmethod
    def zbx_get_current(phase):
        zabbix = ZabbixRead()
        print(zabbix.get_current(phase))

    @staticmethod
    def zbx_get_watt(phase):
        zabbix = ZabbixRead()
        print(zabbix.get_watts(phase))


if __name__ == '__main__':
    fire.Fire(CurrentAndWatt)
