
#pip install ultralytics
import numpy as np
import cv2
import time
import os
import torch
import winsound

# Object detection model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')


def track_objects(frame, bounding_box, interval=600):
    """
    Tracks people in a defined area for frames in a folder and sends an alert when a person enters.
    """

    start_time = time.time()

    # Perform object detection
    results = model(frame)

    # Mark the bounding box of the selected area
    cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0, 255, 0), 2)

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        

        # Check if the object is a person and is within the defined bounding box
        if label == "person" and x1 >= bounding_box[0] and y1 >= bounding_box[1] and x2 <= bounding_box[2] and y2 <= bounding_box[3]:
            return True
    return False

