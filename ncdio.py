from NcdIoCurrent import NcdIo

i2c_address = 42
volts = 230
dev = NcdIo(i2c_address, volts)
dev.board_info()
dev.print_currents()
dev.print_calibration()
print()
dev.get_one_current(0)
print()
dev.get_one_watt(0)
