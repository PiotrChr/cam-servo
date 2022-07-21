import time

from flask import Flask, Blueprint, Response, jsonify, request
import threading
import argparse
import math
from src.cam.CamLoader import CamLoader
# from src.cam.processors.DetectionProcessor import DetectionProcessor
from src.cam.processors.TrackerProcessor import TrackerProcessor

outputFrame = None
lock = threading.Lock()

loaders = []

safe_distance = None

cam = Blueprint('cam', __name__)
main = Blueprint('main', __name__)

servo_distance_by_step = 100


def should_handle():
    return True


def handle_face_offset(yield_val):
    global safe_distance

    if not should_handle():
        return

    if not yield_val:
        return

    face_offset, face_center, image_center, image_dim = yield_val

    if not face_offset or not image_dim:
        return

    if not safe_distance:
        (_, h) = image_dim
        safe_distance = h/3

    x_offset, y_offset = face_offset

    distance = math.sqrt(x_offset ** 2 + y_offset ** 2)

    if distance > safe_distance:
        move_y = 0
        move_x = 0
        print(x_offset, y_offset)
        print('out')

    print('distance', distance)


def get_loader(camera_id):
    for _loader in loaders:
        if _loader.camera_id == camera_id:
            return _loader

    return None


def generate_frames(camera_id):
    _loader = get_loader(camera_id)
    print("Camera: " + str(camera_id) + " is generating frames")
    if _loader is None:
        raise Exception("No loader with id: " + str(camera_id) + " found")

    while True:
        if _loader.outputFrame is None:
            print("No output for camera: " + str(camera_id))
            time.sleep(1)
            continue

        time.sleep(0.1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + _loader.outputFrame + b'\r\n')


@cam.route('/video_feed/<int:camera_id>/', methods=["GET"])
def video_feed(camera_id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@main.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e), url=request.url, details="Cam resource was not found"), 404


app = Flask(__name__)
app.register_blueprint(cam, url_prefix="/cam")
app.register_blueprint(main)


if __name__ in ['__main__', 'uwsgi_file_ipCam']:
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--cameras', nargs='+', type=int, required=True)
    for _, value in ap.parse_args()._get_kwargs():
        if _ == "cameras":
            for cam in value:
                loader = CamLoader(cam)
                # loader.add_processor(TrackerProcessor(0, daemon=False))
                # loader.add_action(TrackerProcessor.__name__, handle_face_offset)
                loader.start()
                loaders.append(loader)

    if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True, use_reloader=False, port=5001)