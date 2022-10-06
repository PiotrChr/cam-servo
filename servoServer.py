from src.servo.ServoController import ServoController
from flask import Flask, Blueprint, Response, jsonify, request
from flask_cors import CORS
import argparse
from config import config
import os


servo = {
    0: ServoController(1, config["i2c"]["address"]["servoController"], 70, 115),
    1: ServoController(2, config["i2c"]["address"]["servoController"], 0, 180)
}

main = Blueprint('main', __name__)
CORS(main)
api = Blueprint('api', __name__)
CORS(api)


@api.route('/')
def index():
    return 'hello', 200


@api.route('/reset/')
def reset_servo():
    chosen_servo = servo[0]
    chosen_servo.reset()

    return {'status': 'ok'}, 200


@api.route('/idle/')
def idle_servo():
    chosen_servo = servo[0]
    chosen_servo.idle()

    return {'status': 'ok'}, 200


@api.route('/auto_idle_off/')
def auto_idle_off():
    chosen_servo = servo[0]
    chosen_servo.auto_idle_off()

    return {'status': 'ok'}, 200


@api.route('/auto_idle_on/')
def auto_idle_on():
    chosen_servo = servo[0]
    chosen_servo.auto_idle_on()

    return {'status': 'ok'}, 200


@api.route('/move/<int:_servo>/<int:move>/')
def move_servo(_servo: int, move: int):
    servo[_servo].move(int(move))

    return {'status': 'ok'}, 200


@api.route('/step/<int:_servo>/<string:step>/')
def step_servo(_servo: int, step: str):
    servo[_servo].step(int(step))

    return {'status': 'ok'}, 200


@api.route('/readpos/')
def position():
    h, v, idle, idle_move_right, idle_move_up, auto_idle, idle_speed = servo[0].read_pos()

    return {
        'position': {'v': v, 'h': h},
        'idle': bool(idle),
        'idleMoveRight': bool(idle_move_right),
        'idleMoveUp': bool(idle_move_up),
        'autoIdle': bool(auto_idle),
        'idleSpeed': idle_speed
        }, 200


@api.route('/toggle_idle/<int:_servo>/<int:toggle_val>/')
def toggle_idle(_servo: int, toggle_val: int):
    servo[_servo].toggle_idle(toggle_val)

    return {'status': 'ok'}, 200


@api.route('/idle_speed/<int:idle_speed>/')
def set_idle_speed(idle_speed: int):
    servo[0].idle_speed(idle_speed)

    return {'status': 'ok'}, 200


@api.route('/stop/')
def stop():
    servo[0].stop()

    return {'status': 'ok'}, 200


@api.route('/restart/')
def restart():
    os.system("sudo reboot")

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
