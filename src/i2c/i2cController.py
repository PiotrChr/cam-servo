import smbus


class I2cController:
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def write(self, command, value):
        self.bus.write_i2c_block_data(self.address, command, value)

    def read(self, _bytes):
        return self.bus.read_i2c_block_data(self.address, 0, _bytes)

