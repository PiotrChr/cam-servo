import cv2
import sys


cascPath = "../resources/opencv/haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

vs = cv2.VideoCapture(0)


def find_faces(image):
    _gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        _gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)


while True:
    ret, frame = vs.read()

    if frame is None:
        print('No frame')
    else:
        cv2.imshow('faces', frame)
        # ret, buffer = cv2.imencode('.jpg', frame)
        find_faces(frame)
