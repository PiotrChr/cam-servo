from src.cam.processors.Processor import Processor
from src.messaging.FrameProducer import FrameProducer
import cv2
import threading
import gc


class KafkaFrameProcessor(Processor):
    def __init__(self, frame_skip=0):
        super().__init__(self.__class__.__name__, frame_skip)
        self.producer = FrameProducer()

    def process_run(self, frame):
        # frame = imutils.resize(frame, width=300)
        ret, buffer = cv2.imencode('.jpg', frame)
        self.producer.produce(buffer.tobytes())

        # del ret, buffer
        # gc.collect()

        return frame

    def process(self, frame):
        threading.Thread(
            target=self.process_run,
            daemon=True,
            args=(frame,)
        ).start()
