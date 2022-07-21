import dlib


def create_detector(detector_svn):
    return dlib.fhog_object_detector(detector_svn)
