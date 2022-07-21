from src.cam.processors.Processor import Processor
from src.image.ObjectTracker import ObjectTracker
import cv2
import imutils


class TrackerProcessor(Processor):
    def __init__(self, frame_skip=0, daemon=False):
        super().__init__(self.__class__.__name__, frame_skip)
        self.daemon = daemon
        self.new_width = 300
        self.new_height = 300
        self.scale_factor = 0.6
        self.tracker = ObjectTracker(replace=False, daemon=daemon)

    def process(self, frame):
        if not self.should_process():
            return None

        small_frame = imutils.resize(frame, width=300)
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.daemon:
            self.tracker.run_thread(small_frame)
        else:
            frame = self.tracker.track_and_detect(small_frame)

        self.yield_val = (
            self.tracker.object_offset,
            self.tracker.object_center,
            self.tracker.image_center,
            self.tracker.image_dim
        )

        return frame
