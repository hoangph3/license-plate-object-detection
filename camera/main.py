import cv2
import json
import requests
import numpy as np
import imutils

from util.controller import create_worker_process
from util.convert_image import array_to_b64


# Read config
with open('config.json') as f:
    configs = json.load(f)

def read_frame(config: dict):
    camera = {}
    for k, v in config.items():
        for cam in v:
            if 'http' not in str(cam['host']):
                camera["{}_{}".format(k, cam['type'])] = cv2.VideoCapture(cam['host'])
            else:
                camera["{}_{}".format(k, cam['type'])] = cam['host']

    print(camera)
    while True:
        data = {}
        for name_capture, video_capture in camera.items():
            if isinstance(video_capture, str):
                img_resp = requests.get(video_capture)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_arr, -1)
                img = imutils.resize(img, width=500, height=900)
                ret = True
            else:
                ret, img = video_capture.read()

            if ret:
                cv2.imshow(name_capture, img)
                data[name_capture] = img

        result = {}
        for task, payload in data.items():
            if 'object' in task:
                r = requests.post(
                    url=configs["object_serving"],
                    json={"images": [{"image": array_to_b64(payload)}]}
                )
            elif 'plate' in task:
                r = requests.post(
                    url=configs["plate_serving"],
                    json={"images": [{"image": array_to_b64(payload)}]}
                )
            else:
                raise ValueError("The camera type is wrong. It should be one of 'object' or 'plate'.")
            result[task] = r.json()
        print(result)

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
