from src.servo.ServoController import ServoController
from flask import Flask, Blueprint, Response, jsonify, request
from flask_cors import CORS
import argparse
from config import config

servo = {
    0: ServoController(1, config["i2c"]["address"]),
    1: ServoController(2, config["i2c"]["address"])
}

main = Blueprint('main', __name__)
CORS(main)
api = Blueprint('api', __name__)
CORS(api)


@api.route('/')
def index():
    return 'hello', 200


@api.route('/reset/<int:_servo>/')
def reset_servo(_servo: int):
    chosen_servo = servo[_servo]
    chosen_servo.reset()

    return {'status': 'ok'}, 200


@api.route('/idle/<int:_servo>/')
def idle_servo(_servo: int):
    chosen_servo = servo[_servo]
    chosen_servo.idle()

    return {'status': 'ok'}, 200


@api.route('/auto_idle_off/<int:_servo>')
def auto_idle_off(_servo: int):
    chosen_servo = servo[_servo]
    chosen_servo.auto_idle_off()

    return {'status': 'ok'}, 200


@api.route('/auto_idle_on/<int:_servo>')
def auto_idle_on(_servo: int):
    chosen_servo = servo[_servo]
    chosen_servo.auto_idle_on()

    return {'status': 'ok'}, 200


@api.route('/move/<int:_servo>/<string:move>/')
def move_servo(_servo: int, move: str):
    chosen_servo = servo[_servo]
    move = int(move)

    if move == -1:
        chosen_servo.step_back()
    elif move == 1:
        chosen_servo.step_forward()

    return {'status': 'ok'}, 200


@main.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e), url=request.url, details="Cam resource was not found"), 404


app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(main)


if __name__ in ['__main__', 'uwsgi_file_servoServer']:
    ap = argparse.ArgumentParser()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
