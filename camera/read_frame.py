from multiprocessing import Process
import cv2
import json
import requests
import numpy as np
import imutils


def read_local_cam(name, cam_id):
    cam = cv2.VideoCapture(cam_id)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False
    count = 0
    while rval:
        count += 1
        cv2.imwrite("{}_{}.jpg".format(name, count), frame)
        rval, frame = cam.read()


def read_http_cam(name, url):
    count = 0
    while True:
        count += 1
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=1000, height=1800)
        cv2.imwrite("{}_{}.jpg".format(name, count), img)


if __name__ == "__main__":
    # Read config
    with open('config_test.json') as f:
        config = json.load(f)

    # Capture frames
    procs = []
    for key_cfg, value_cfg in config.items():
        for cam_cfg in value_cfg:
            args = ("{}_{}".format(key_cfg, cam_cfg['type']), cam_cfg['host'])
            if 'http' in str(cam_cfg['host']):
                procs.append(Process(target=read_http_cam, args=args))
            else:
                procs.append(Process(target=read_local_cam, args=args))

    for proc in procs:
        proc.start()
