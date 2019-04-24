from NcdIoCurrent import NcdIo

i2c_address = 42
dev = NcdIo(i2c_address)
dev.board_info()
