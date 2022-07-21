import numpy as np
import dlib
import cv2
import src.image.utils as utils
import threading


class ObjectTracker:
    def __init__(self, replace=None, daemon=False, scale_factor=1):
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.prototxt = 'resources/object_tracker/model2/deploy.prototxt'
        self.model = 'resources/object_tracker/model2/mobilenet_iter_73000.caffemodel'

        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        print("Model loading finished")
        self.confidence = 0.4
        self.labels_to_find = ['person']
        self.image_dim = None
        self.image_center = None
        self.tracker = None
        self.label = None
        self.scale_factor = scale_factor
        self.replace = replace
        self.daemon = daemon
        self.object_center = None
        self.object_offset = None
        self.reset_tracker_limit = 20
        self.tracker_count = 0
        self.current_frame = None
        self.current_cropped_frame = None
        self.detection = None

    def run_thread(self, frame):
        t = threading.Thread(
            target=self.track_and_detect,
            daemon=True,
            args=(frame,)
        )
        t.start()

    def track_and_detect(self, frame):
        if not self.image_center:
            (self.image_dim, self.image_center) = utils.get_frame_center(frame)

        w, h = self.image_dim

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.tracker is None:
            print('trying to track')
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)
            print('got blob')
            # pass the blob through the network and obtain the detections
            # and predictions
            self.net.setInput(blob)

            try:
                detections = self.net.forward()
            except:
                print('error')
                detections = []

            print('forwarded')
            print('detections', len(detections))

            if len(detections) > 0:
                # find the index of the detection with the largest
                # probability -- out of convenience we are only going
                # to track the first object we find with the largest
                # probability; future examples will demonstrate how to
                # detect and extract *specific* objects
                i = np.argmax(detections[0, 0, :, 2])
                # grab the probability associated with the object along
                # with its class label
                conf = detections[0, 0, i, 2]
                self.label = self.CLASSES[int(detections[0, 0, i, 1])]
                if self.label in self.labels_to_find:
                    print('confidence', conf)

                if conf > self.confidence and self.label in self.labels_to_find:
                    # compute the (x, y)-coordinates of the bounding box
                    # for the object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # construct a dlib rectangle object from the bounding
                    # box coordinates and then start the dlib correlation
                    # tracker
                    self.tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    self.tracker.start_track(rgb, rect)
                    # if self.replace:
                    #     cv2.rectangle(frame, (startX, startY), (endX, endY),
                    #                   (0, 255, 0), 1)
                    #     cv2.putText(frame, self.label, (startX, startY - 15),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        else:
            self.tracker.update(rgb)
            pos = self.tracker.get_position()

            start_x = int(pos.left())
            start_y = int(pos.top())
            end_x = int(pos.right())
            end_y = int(pos.bottom())

            self.object_center = utils.get_object_center((start_y, end_x, end_y, start_x))
            self.object_offset = utils.get_center_offset(self.object_center, self.image_center)

            cropped_start_x = 0 if start_x < 0 else start_x
            cropped_start_y = 0 if end_y < 0 else start_y
            cropped_end_x = w if end_x > w else end_x
            cropped_end_y = h if start_y > w else end_y

            self.current_cropped_frame = frame[cropped_start_y: cropped_end_y, cropped_start_x: cropped_end_x]

            if self.replace:
                cv2.line(frame, self.object_center, self.image_center, (0, 255, 0), 2)
                # draw the bounding box from the correlation object tracker
                # cv2.rectangle(frame, (start_x, start_y), (end_x, end_y),
                #               (0, 255, 0), 1)
                # cv2.putText(frame, self.label, (startX, startY - 15),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

            self.handle_tracker_reset()

        self.current_frame = frame

        if self.current_cropped_frame is not None:
            return self.current_cropped_frame

        return frame

    def handle_tracker_reset(self):
        if self.tracker_count >= self.reset_tracker_limit:
            self.tracker = None

        self.tracker_count = self.tracker_count + 1
