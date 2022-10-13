from time import sleep
from src.i2c.i2cController import I2cController
from config import config


class ServoController:
    def __init__(self, id, address, min_pos=0, max_pos=180, starting_pos=90):
        self.i2cController = I2cController(address)
        self.id = id
        self.min = min_pos
        self.max = max_pos
        self.starting_pos = starting_pos

    def get_pos(self):
        pass

    def start_servo(self):
        pass

    def reset(self):
        self.i2cController.write(config["i2c"]["cmd"]["reset"], [])

    def move(self, angle):
        self.i2cController.write(config["i2c"]["cmd"]["move"], [self.id, angle])

    def idle(self):
        self.i2cController.write(config["i2c"]["cmd"]["idle"], [])

    def auto_idle_off(self):
        self.i2cController.write(config["i2c"]["cmd"]["autoidleoff"], [])

    def auto_idle_on(self):
        self.i2cController.write(config["i2c"]["cmd"]["autoidleon"], [])

    def step(self, direction: int):
        self.i2cController.write(config["i2c"]["cmd"]["step"], [self.id, direction])

    def toggle_idle(self, toggle_val: int):
        self.i2cController.write(config["i2c"]["cmd"]["idle_axis"], [self.id, toggle_val])

    def idle_speed(self, speed):
        self.i2cController.write(config["i2c"]["cmd"]["idle_speed"], list(divmod(speed, 10)))

    def stop(self):
        self.i2cController.write(config["i2c"]["cmd"]["stop"], [])

    def reset_device(self):
        self.i2cController.write(config["i2c"]["cmd"]["reset_dev"], [])
    
    def read_pos(self):
        return self.i2cController.read(7)

    def cleanup(self):
        pass
