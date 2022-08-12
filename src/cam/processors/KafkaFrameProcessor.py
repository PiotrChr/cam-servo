from src.cam.processors.Processor import Processor
from src.messaging.FrameProducer import FrameProducer
import threading
import numpy as np
import pickle
import timeit
import imutils
import cv2


class KafkaFrameProcessor(Processor):
    def __init__(self, frame_skip=0):
        super().__init__(self.__class__.__name__, frame_skip)
        self.producer = FrameProducer()

        self.iterations = 0
        self.average = None
        # self.max_time = 0
        # self.min_time = 999
        # self.start_time = timeit.default_timer()

    def process_run(self, frame):
        # start_time = timeit.default_timer()
        frame = imutils.resize(frame, width=300)
        ret, buffer = cv2.imencode('.jpg', frame)

        self.producer.produce(buffer.tobytes())

        # operating_time = timeit.default_timer() - start_time
        #
        # self.iterations = self.iterations + 1
        # if not self.average:
        #     self.average = operating_time
        #
        # if operating_time > self.max_time:
        #     self.max_time = operating_time
        #
        # if operating_time < self.min_time:
        #     self.min_time = operating_time
        #
        # self.average = self.average + (operating_time - self.average)/self.iterations
        #
        # if np.mod(self.iterations, 20) == 0:
        #     print(frame.shape)
        #     print('\n')
        #     print('average time: ', self.average)
        #     print('iters: ', self.iterations)
        #     print('max time: ', self.max_time)
        #     print('min time: ', self.min_time)

        return frame

    def process(self, frame):
        self.process_run(frame)
        # threading.Thread(
        #     target=self.process_run,
        #     daemon=True,
        #     args=(frame,)
        # ).start()
