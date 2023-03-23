import os
import cv2
from pathlib import Path
from keras.models import model_from_json
import matplotlib.pyplot as plt

from local_utils import detect_lp


def load_model(path):
    try:
        path = os.path.splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)


def preprocess_image(image_path,resize=False):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img


def get_plate(image_path, Dmax=1024, Dmin=128):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return LpImg, cor


if __name__ == "__main__":
    # load model
    wpod_net_path = "serving/wpod-net.json"
    wpod_net = load_model(wpod_net_path)

    # load image
    for img_path in Path("images").glob("**/*.jpg"):
        img_path = str(img_path)
        if 'plate' in img_path:
            continue
        try:
            LpImg, cor = get_plate(img_path)
            plt.imsave("images/plate_{}".format(os.path.basename(img_path)), LpImg[0])
        except AssertionError:
            pass
