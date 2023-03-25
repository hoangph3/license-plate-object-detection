from paddleocr import PaddleOCR
import numpy as np


def get_ocr(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
    result = ocr.ocr(image_path, cls=True)
    output = []
    for res in result:
        text = []
        score = []
        for line in res:
            if line[-1][0]:
                text.append(line[-1][0])
                score.append(line[-1][-1])
        if len(text):
            text = " ".join(text)
            score = float(np.mean(score))

        output.append({
            "text": text,
            "score": round(score, 4)
        })

    return output
