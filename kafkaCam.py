import argparse
import math
from src.cam.CamLoader import CamLoader
from src.cam.processors.KafkaFrameProcessor import KafkaFrameProcessor

loaders = []

servo_distance_by_step = 100


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
