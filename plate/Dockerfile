FROM paddlecloud/paddleocr:2.6-cpu-latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN mkdir -p /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/ && \
    cp serving/ocr/en_PP-OCRv3_det_infer.tar /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar && \
    mkdir -p /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/ && \
    cp serving/ocr/en_PP-OCRv3_rec_infer.tar /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar

CMD ["python", "main.py"]
