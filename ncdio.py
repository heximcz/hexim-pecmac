from NcdIoCurrent import NcdIo

i2c_address = 42
dev = NcdIo(i2c_address)
try:
    dev.board_info()
except IOError:
    print("No device exist on address: %d" % i2c_address)
