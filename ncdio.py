from NcdIoCurrent import NcdIo
from LCD1602 import LCD1602


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

"""
for share data with zabbix, write data to the ramdisk
"""