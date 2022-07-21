import argparse
import math
from src.cam.CamLoader import CamLoader
from src.cam.processors.KafkaFrameProcessor import KafkaFrameProcessor

loaders = []

servo_distance_by_step = 100


def should_handle():
    return True

#
# def handle_face_offset(yield_val):
#     global safe_distance
#
#     if not should_handle():
#         return
#
#     if not yield_val:
#         return
#
#     face_offset, face_center, image_center, image_dim = yield_val
#
#     if not face_offset or not image_dim:
#         return
#
#     if not safe_distance:
#         (_, h) = image_dim
#         safe_distance = h/3
#
#     x_offset, y_offset = face_offset
#
#     distance = math.sqrt(x_offset ** 2 + y_offset ** 2)
#
#     if distance > safe_distance:
#         move_y = 0
#         move_x = 0
#         print(x_offset, y_offset)
#         print('out')
#
#     print('distance', distance)
#
#
# def get_loader(camera_id):
#     for _loader in loaders:
#         if _loader.camera_id == camera_id:
#             return _loader
#
#     return None


if __name__ in ['__main__']:
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--cameras', nargs='+', type=int, required=True)
    for _, value in ap.parse_args()._get_kwargs():
        if _ == "cameras":
            for cam in value:
                loader = CamLoader(cam)
                loader.add_processor(KafkaFrameProcessor(0))
                loader.start()
                loaders.append(loader)
