from src.cam.processors.Processor import Processor
from src.image.FaceDetector import FaceDetector
import cv2


class DetectionProcessor(Processor):
    def __init__(self, frame_skip=0, daemon=True):
        super().__init__(self.__class__.__name__, frame_skip)
        self.daemon = daemon
        self.scale_factor = 0.65
        self.detector = FaceDetector(replace=True, daemon=daemon, scale_factor=self.scale_factor)

    def process(self, frame):
        if not self.should_process():
            return None

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_small_frame = frame[:, :, ::-1]
        if self.daemon:
            self.detector.detect_daemon(small_frame)
        else:
            frame = self.detector.detect(small_frame)

        self.yield_val = (
            self.detector.face_offset,
            self.detector.face_center,
            self.detector.image_center,
            self.detector.image_dim
        )

        return frame
