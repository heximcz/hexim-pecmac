from NcdIoCurrent import NcdIo

i2c_address = 42
volts = 230
dev = NcdIo(i2c_address, volts)
dev.board_info()
dev.print_all_currents()
