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
        self.i2cController.write(config["i2c"]["cmd"]["move"], [])

    def move(self, angle):
        self.i2cController.write(config["i2c"]["cmd"]["move"], [self.id, angle])

    def idle(self):
        self.i2cController.write(config["i2c"]["cmd"]["move"], [])

    def step_back(self):
        pass

    def step_forward(self):
        pass

    def cleanup(self):
        pass
