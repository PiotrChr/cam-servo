import threading
import time
from imutils.video import VideoStream


class CamLoader:
    def __init__(self, camera_id, event=None):
        self.camera_id = camera_id
        self.event = event
        self.vs = None
        self.outputFrame = None
        self.processors = []
        self.actions = {}

        print("Created cam loader with id:" + str(camera_id))

        super().__init__()

    def add_processor(self, processor):
        self.processors.append(processor)

    def add_action(self, processor, action):
        self.actions[processor] = action

    def start(self):
        threading.Thread(
            target=self.start_read,
            daemon=False,
        ).start()

    def start_read(self):
        print("Starting thread for camera id:" + str(self.camera_id))
        self.vs = VideoStream(src=self.camera_id).start()
        time.sleep(2)
        print("Stream for:" + str(self.camera_id) + " started, writing to buffer")

        self.read()

    def read(self):
        while True:
            frame = self.vs.read()

            if frame is None:
                print('No frame')
            else:
                for processor in self.processors:
                    process = processor.process(frame)
                    if process is None:
                        continue

                    frame = process
                    processor_name = processor.__class__.__name__
                    if processor_name in self.actions:
                        self.actions[processor_name](processor.yield_val)

                # ret, buffer = cv2.imencode('.jpg', frame)
                # self.outputFrame = buffer.tobytes()

                time.sleep(0.1)

