import cv2
import base64
import numpy as np


def b64_to_array(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def array_to_b64(img=None, img_path=None):
    if img_path and img is None:
        img = cv2.imread(img_path)
        _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    elif img and img_path is None:
        im_arr = img
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64
