import smbus
import time

bus = smbus.SMBus(1)
address = 0x08

move = 0x01
setIdle = 0x02
reset = 0x03
autoIdleOne = 0x04
autoIdleOff = 0x05
step = 0x06
idle_axis = 0x07
idle_speed = 0x08

bus.write_i2c_block_data(address, move, [1, 90])
print(bus.read_i2c_block_data(address, 0, 2))
print(bus.read_byte(address))
print(bus.read_byte(address))
print(bus.read_byte(address))
print(bus.read_byte(address))
print(bus.read_byte(address))

for i in range(0, 10):
    print(bus.read_byte(address))

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
