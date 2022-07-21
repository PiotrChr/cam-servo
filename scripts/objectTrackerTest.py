from imutils.video import FPS
import numpy as np
import imutils
import dlib
import cv2
from os.path import exists


model_path = '../resources/object_tracker/model2/mobilenet_iter_73000.caffemodel'
proto_txt = '../resources/object_tracker/model2/deploy.prototxt'
confidence = 0.6
find_label = 'person'
image_center = None
image_dim = None

if not exists(model_path):
    print("Model path doesn't exist")

if not exists(proto_txt):
    print("Proto path doesn't exist")


# initialize the list of class labels MobileNet SSD was trained to
# detect
# CLASSES = ["background", "cat", "dog", "person"]
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(proto_txt, model_path)

# initialize the video stream, dlib correlation tracker, output video
# writer, and predicted class label
print("[INFO] starting video stream...")


def get_face_center(face_location):
    (top, right, bottom, left) = face_location

    x = right - int((right - left)/2)
    y = top - int((top - bottom)/2)

    return x, y


def get_face_offset(_face_center, _image_center):
    # print(face_location)
    x, y = _face_center
    ic_x, ic_y = _image_center

    return ic_x - x, ic_y - y


vs = cv2.VideoCapture(0)
tracker = None
writer = None
label = ""
# start the frames per second throughput estimator
fps = FPS().start()

# loop over frames from the video file stream
while True:
    # grab the next frame from the video file
    (grabbed, frame) = vs.read()
    # check to see if we have reached the end of the video file
    if frame is None:
        break

    # resize the frame for faster processing and then convert the
    # frame from BGR to RGB ordering (dlib needs RGB ordering)
    frame = imutils.resize(frame, width=600)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # if we are supposed to be writing a video to disk, initialize
    # the writer
    if not image_center:
        (h, w) = frame.shape[:2]
        image_dim = (w, h)
        image_center = (int(w/2), int(h/2))
    # if our correlation object tracker is None we first need to
    # apply an object detector to seed the tracker with something
    # to actually track
    if tracker is None:
        # grab the frame dimensions and convert the frame to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (w, h), 127.5)
        # pass the blob through the network and obtain the detections
        # and predictions
        net.setInput(blob)
        detections = net.forward()

        # ensure at least one detection is made
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
            print('detection', detections[0, 0, i, 1])
            label = CLASSES[int(detections[0, 0, i, 1])]
            print(label)
            # filter out weak detections by requiring a minimum
            # confidence
            print('confidence', conf)
            if conf > confidence and label == find_label:
                # compute the (x, y)-coordinates of the bounding box
                # for the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # construct a dlib rectangle object from the bounding
                # box coordinates and then start the dlib correlation
                # tracker

                if (label == 'cat'):
                    label = "Niuszka"

                tracker = dlib.correlation_tracker()
                rect = dlib.rectangle(startX, startY, endX, endY)
                tracker.start_track(rgb, rect)
                # draw the bounding box and text for the object
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 1)
                cv2.putText(frame, label, (startX, startY - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

    else:
        # update the tracker and grab the position of the tracked
        # object
        print('tracking: ', label)
        tracker.update(rgb)
        pos = tracker.get_position()
        # unpack the position object
        startX = abs(int(pos.left()))
        startY = abs(int(pos.top()))
        endX = abs(int(pos.right()))
        endY = abs(int(pos.bottom()))

        face_center = get_face_center((endY, endX, startY, startX))
        face_offset = get_face_offset(face_center, image_center)

        cv2.line(frame, face_center, image_center, (0, 255, 0), 3)

        # print((startX, startY), (endX, endY))
        # draw the bounding box from the correlation object tracker
        cv2.rectangle(frame, (startX, startY), (endX, endY),
                      (0, 255, 0), 4)
        cv2.putText(frame, label, (startX, startY - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    # update the FPS counter
    fps.update()
