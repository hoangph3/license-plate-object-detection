FROM jjanzic/docker-python3-opencv:opencv-4.0.0

WORKDIR /app

COPY . .

RUN apt-get update -y && \
    apt-get install nano telnet curl -y && \
    pip install -U pip && \
    pip install -r requirements.txt && \
    pip install torch==1.13.0 torchaudio==0.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cpu

CMD ["python", "main.py"]
