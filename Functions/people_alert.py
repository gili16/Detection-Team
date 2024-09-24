
#pip install ultralytics
import numpy as np
import cv2
import time
import os
import torch
import winsound

# Object detection model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')

def play_alert_sound():
    # Play a system alert sound
    winsound.Beep(1000, 500)  # You can adjust the frequency and duration as needed

def track_objects(frame, bounding_box, interval=600):
    """
    Tracks people in a defined area for frames in a folder and sends an alert when a person enters.
    """
    # timestamp = time.strftime("%Y%m%d-%H%M%S")
    # result_folder = os.path.join('results_tracking_in_area', f"{video_name}_{timestamp}")
    # os.makedirs(result_folder, exist_ok=True)

    start_time = time.time()
    # frame_files = [f for f in os.listdir(frames_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # for frame_file in frame_files:
    #     frame_path = os.path.join(frames_folder, frame_file)
    #     frame = cv2.imread(frame_path)
    # if frame is None or (time.time() - start_time) > interval:
    #     return False

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
            # play_alert_sound()  # Trigger an alert when a person enters the bounding box
            # print("Alert: Person detected in the specified area!")
            # cv2.rectangle(frame, (x1,y1), (x2,y2), (255, 0, 0), 2)
            # cv2.putText(frame, label, (x1+1,y1-1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                # Break out of the loop after the first person is detected

                # Save the frame with the bounding box in the results folder
            # result_frame_path = os.path.join(result_folder, frame_file)
            # cv2.imwrite(result_frame_path, frame)
            # cv2.imshow(mat=frame,winname="found person")
            # break
    return False

# frames_folder = 'video/M0202'  # Path to the frames folder
# video_name = 'M0202'  # Video name (for use in the results folder)
# bounding_box = (20, 20, 400, 400)  # Boundaries of the area: (x1, y1, x2, y2)
# track_objects(frames_folder, bounding_box, video_name)
