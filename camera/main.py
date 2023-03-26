import cv2
import json
import requests
import numpy as np
import imutils
from loguru import logger
import redis
import os

from util.controller import create_worker_process
from util.convert_image import array_to_b64

os.environ['DISPLAY'] = ':0'

# Read config
with open('config.json') as f:
    configs = json.load(f)

# Log
logger.add('app.log', rotation="500 MB")

def read_frame(config: dict):
    r = redis.Redis(host="127.0.0.1", port=6379, db=0)

    camera = {}
    for k, v in config.items():
        for cam in v:
            if 'http' not in str(cam['host']):
                camera["{}_{}".format(k, cam['type'])] = cv2.VideoCapture(cam['host'])
            else:
                camera["{}_{}".format(k, cam['type'])] = cam['host']

    logger.info("Camera: {}".format(camera))
    while True:
        data = {}
        for name_capture, video_capture in camera.items():
            if isinstance(video_capture, str):
                try:
                    img_resp = requests.get(video_capture)
                    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    img = cv2.imdecode(img_arr, -1)
                    img = imutils.resize(img, width=500, height=900)
                    # cv2.imshow(name_capture, img)  # not working with docker because it not have GUI
                    data[name_capture] = img
                except Exception as e:
                    pass
            else:
                ret, img = video_capture.read()
                if ret:
                    # cv2.imshow(name_capture, img)  # not working with docker because it not have GUI
                    data[name_capture] = img

        response = {}
        connected = {}
        for task, payload in data.items():
            connected[task] = True
            if 'object' in task:
                try:
                    r = requests.post(
                        url=configs["object_serving"],
                        json={"images": [{"image": array_to_b64(payload)}]}
                    )
                    response[task] = r.json()
                except:
                    connected[task] = False
            elif 'plate' in task:
                try:
                    r = requests.post(
                        url=configs["plate_serving"],
                        json={"images": [{"image": array_to_b64(payload)}]}
                    )
                    response[task] = r.json()
                except:
                    connected[task] = False
            else:
                raise ValueError("The camera type is wrong. It should be one of 'object' or 'plate'.")
        # push result into queue
        result = {'connected': connected, 'response': response}
        logger.info(json.dumps(result))
        try:
            r.lpop("alpr")
            r.rpush("alpr", json.dumps(result))
        except Exception as e:
            pass

        # Press Esc key to exit
        if cv2.waitKey(1) == 27:
            break

    for name_capture, video_capture in camera.items():
        if isinstance(video_capture, str):
            continue
        video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Capture frames
    for config in configs['camera']:
        for k, v in config.items():
            create_worker_process(k, read_frame, (config, ))
