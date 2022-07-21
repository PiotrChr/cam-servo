import abc


class Processor:
    def __init__(self, name, frame_skip):
        self.name = name
        self.frame_skip = frame_skip
        self.counter = 0
        self.yield_val = None

    def should_process(self):
        if self.counter >= self.frame_skip:
            self.counter = 0
            return True

        self.counter = self.counter + 1
        return False

    @abc.abstractmethod
    def process(self, image):
        """Method documentation"""
        return image
