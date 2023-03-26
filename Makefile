SHELL := /bin/bash

TAG = 1.0.0
CAMERA_IMG = hoangph3/alpr-camera:$(TAG)
OBJECT_IMG = hoangph3/alpr-object:$(TAG)
OCR_IMG = hoangph3/alpr-ocr:$(TAG)

build_camera:
	docker build -f camera/Dockerfile -t $(CAMERA_IMG) camera
build_object:
	docker build -f object/Dockerfile -t $(OBJECT_IMG) object
build_ocr:
	docker build -f plate/Dockerfile -t $(OCR_IMG) plate

push_camera:
	docker push $(CAMERA_IMG)
push_object:
	docker push $(OBJECT_IMG)
push_ocr:
	docker push $(OCR_IMG)
