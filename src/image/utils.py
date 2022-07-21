def get_object_center(object_location):
    (top, right, bottom, left) = object_location

    x = right - int((right - left)/2)
    y = top - int((top - bottom)/2)

    return x, y


def get_center_offset(object_center, image_center):
    # print(face_location)
    x, y = object_center
    ic_x, ic_y = image_center

    return ic_x - x, ic_y - y


def get_frame_center(frame):
    (h, w) = frame.shape[:2]
    image_dim = (w, h)
    image_center = (int(w/2), int(h/2))

    return image_dim, image_center
