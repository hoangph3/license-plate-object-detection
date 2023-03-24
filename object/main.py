from core.util import load_model
from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import os


if __name__ == "__main__":
    # load model
    predictor, class_names = load_model(
        net_type="mb2-ssd-lite",
        model_path="serving/mb2-ssd-lite-mp-0_686.pth",
        label_path="serving/voc-model-labels-orig.txt"
    ) 

    # load image
    for image_path in sorted(Path("images").glob("**/*.jpg")):
        image_path = str(image_path)
        if 'object' in image_path:
            continue
        orig_image = cv2.imread(image_path)
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)

        boxes, labels, probs = predictor.predict(image, 10, 0.4)
        print(os.path.basename(image_path), boxes, labels, probs)
        for i in range(boxes.size(0)):
            box = boxes[i, :].numpy().astype(int)
            label = "{}: {:.2f}".format(class_names[labels[i]], probs[i])
            cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 2)
            cv2.putText(
                orig_image, label,
                (box[0] - 10, box[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 0), 2
            )
            object_image_path = "images/object_{}".format(os.path.basename(image_path))
            plt.imsave(object_image_path, orig_image)
