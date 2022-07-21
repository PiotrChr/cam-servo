import smbus
import time

bus = smbus.SMBus(1)
address = 0x08

moveCmd = 0x01
setIdleCmd = 0x02
resetCmd = 0x03

bus.write_i2c_block_data(address, setIdleCmd, [2, 125])
time.sleep(1)
#
# for i in range(1, 180):
#     bus.write_i2c_block_data(address, 0x01, [1, i])
#     time.sleep(0.5)


# class I2cController:
#     def __init__(self, address):
#         self.bus = smbus.SMBus(0)
#         self.address = address
#
#     def write(self, value):
#         self.bus.write_byte_data(self.address, 0, value)
#         return -1
