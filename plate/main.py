import os
from pathlib import Path
import matplotlib.pyplot as plt

from core.detection import get_plate
from core.ocr import get_ocr
from core.util import load_model


if __name__ == "__main__":
    # load model
    wpod_net_path = "serving/wpod-net.json"
    wpod_net = load_model(wpod_net_path)

    # load image
    for image_path in sorted(Path("images").glob("**/*.jpg")):
        image_path = str(image_path)
        if 'plate' in image_path:
            continue
        try:
            LpImg, cor = get_plate(wpod_net, image_path)
            plate_image_path = "images/plate_{}".format(os.path.basename(image_path))
            plt.imsave(plate_image_path, LpImg[0])
            LpText = get_ocr(plate_image_path)
            print(os.path.basename(plate_image_path), LpText)
        except Exception as e:
            print(e)
