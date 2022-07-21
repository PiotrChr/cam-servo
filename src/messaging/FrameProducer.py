from src.messaging.Producer import Producer


class FrameProducer(Producer):
    def __init__(self):
        super().__init__('StingFrames')

    def produce(self, frame):
        self.send('sting_frame', frame)
