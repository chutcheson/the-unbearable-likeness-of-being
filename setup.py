import cv2
import numpy as np
import requests
import os

# Setup
# Download the pre-trained YOLOv3 weights and configuration files
weights_url = 'https://pjreddie.com/media/files/yolov3.weights'
config_url = 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg'

weights_path = 'yolov3.weights'
config_path = 'yolov3.cfg'

if not os.path.exists(weights_path):
    response = requests.get(weights_url)
    with open(weights_path, 'wb') as f:
        f.write(response.content)

if not os.path.exists(config_path):
    response = requests.get(config_url)
    with open(config_path, 'w') as f:
        f.write(response.text)

def get_class_names(file_path):
    with open(file_path, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
    return class_names

class_names_url = 'https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names'
class_names_path = 'coco.names'

if not os.path.exists(class_names_path):
    response = requests.get(class_names_url)
    with open(class_names_path, 'w') as f:
        f.write(response.text)

class_names = get_class_names(class_names_path)

def load_yolo_model():
    net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
    return net

net = load_yolo_model()
