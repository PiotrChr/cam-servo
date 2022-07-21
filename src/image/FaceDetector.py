from src.image import face_detector_api
from src.image import shape_detector_api
import cv2
import numpy as np
from os.path import isfile, join, exists, splitext
from os import listdir
import threading


class FaceDetector:
    def __init__(self, replace=True, daemon=False, scale_factor=1):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.shape_locations = []
        self.face_encodings = []
        self.face_names = []
        self.replace = replace
        self.face_offset = None
        self.daemon = daemon
        self.face_center = None
        self.image_center = None
        self.image_dim = None
        self.scale_factor = scale_factor
        self.shape_detector = None
        self.init()

    def init(self):
        actors = ['piotrc']

        for actor in actors:
            self.get_faces(actor)

        self.shape_detector = shape_detector_api.create_detector('resources/detector/detector.svm')

    def get_faces(self, actor: str):
        faces_dir = 'resources/imgs/faces/' + actor

        if not exists(faces_dir):
            return None

        for f in listdir(faces_dir):
            _, ext = splitext(f)
            full_path = join(faces_dir, f)

            if isfile(full_path) and (ext == '.jpeg' or ext == '.jpg'):
                image = face_detector_api.load_image_file(full_path)
                encoding = face_detector_api.face_encodings(image)

                if len(encoding) > 0:
                    self.known_face_encodings.append(encoding[0])
                    self.known_face_names.append(actor)
                else:
                    print('Couldn\'t recognize face in file: ' + full_path)

    def get_face_center(self, face_location):
        (top, right, bottom, left) = face_location

        x = right - int((right - left)/2)
        y = top - int((top - bottom)/2)

        return x, y

    def get_face_offset(self, face_center):
        # print(face_location)
        x, y = face_center
        ic_x, ic_y = self.image_center

        return ic_x - x, ic_y - y

    def detect_daemon(self, frame):
        t = threading.Thread(
            target=self.detect,
            daemon=True,
            args=(frame,)
        )
        t.start()

    def detect(self, frame):
        if not self.image_center:
            (h, w) = frame.shape[:2]
            self.image_dim = (w, h)
            self.image_center = (int(w/2), int(h/2))

        # self.face_locations = face_detector_api.face_locations(frame, 1, 'cnn')
        # self.face_encodings = face_detector_api.face_encodings(frame, self.face_locations)
        self.shape_locations = self.shape_detector(frame, 1)

        self.face_names = []
        self.face_center = None
        self.face_offset = None
        # for face_encoding in self.face_encodings:
        #     # See if the face is a match for the known face(s)
        #     matches = face_detector_api.compare_faces(self.known_face_encodings, face_encoding)
        #     name = "Unknown"
        #
        #     # # If a match was found in known_face_encodings, just use the first one.
        #     # if True in matches:
        #     #     first_match_index = matches.index(True)
        #     #     name = known_face_names[first_match_index]
        #
        #     # Or instead, use the known face with the smallest distance to the new face
        #     face_distances = face_detector_api.face_distance(self.known_face_encodings, face_encoding)
        #     best_match_index = np.argmin(face_distances)
        #     if matches[best_match_index]:
        #         name = self.known_face_names[best_match_index]
        #
        #     self.face_names.append(name)

        print(self.shape_locations)

        if len(self.face_locations) == 1 or len(self.face_locations) == 1:
            if len(self.shape_locations) == 1:
                object_location = self.shape_locations[0]
            else:
                object_location = self.face_locations[0]

            self.face_center = self.get_face_center(object_location)
            self.face_offset = self.get_face_offset(self.face_center)

            cv2.line(frame, self.face_center, self.image_center, (0, 255, 0), 3)

        if self.replace:
            for (top, right, bottom, left) in self.face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                # top *= 4
                # right *= 4
                # bottom *= 4
                # left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame
