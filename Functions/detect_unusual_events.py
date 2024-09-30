import os
import cv2
import numpy as np
import pygame
import glob
from ultralytics import YOLO
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Server import allert_server_pb2 as allert__server__pb2
from Functions.event import UnusualEvent
# Initialize pygame mixer for sound playback
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
import torch
# Define thresholds for unusual events
SPEED_THRESHOLD = 700
GATHERING_THRESHOLD = 2
PARKING_THRESHOLD = 30
CLOSE_DISTANCE_THRESHOLD = 50

# Classes to track for unusual events
TARGET_CLASSES = ['car', 'truck', 'bus', 'person']

# Initialize object tracker
object_tracker = {label: [] for label in TARGET_CLASSES}

# Load pre-trained YOLOv8 model
model = YOLO('yolov8n.pt')
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')

def track_object_movement(frame_idx, detected_objects):
    global object_tracker
    unusual_events = []
    people_count = 0
    
    for obj in detected_objects:
        bbox = obj['bbox']
        label = obj['label']
        box_center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
        
        if label in TARGET_CLASSES:
            object_tracker[label].append((frame_idx, box_center))
            
            if label == 'person':
                people_count += 1
            
            if len(object_tracker[label]) > 1:
                prev_frame_idx, prev_center = object_tracker[label][-2]
                
                if frame_idx != prev_frame_idx:
                    distance = np.sqrt((box_center[0] - prev_center[0]) ** 2 + (box_center[1] - prev_center[1]) ** 2)
                    speed = distance / (frame_idx - prev_frame_idx)
                    
                    if speed > SPEED_THRESHOLD:
                        unusual_events.append({
                            'label': label,
                            'bbox': bbox,
                            'speed': speed,
                            'event': 'Speeding'
                        })

            if label in ['car', 'truck', 'bus'] and len(object_tracker[label]) > 1:
                prev_frame_idx, prev_center = object_tracker[label][-2]
                if frame_idx != prev_frame_idx:
                    distance = np.sqrt((box_center[0] - prev_center[0]) ** 2 + (box_center[1] - prev_center[1]) ** 2)
                    speed = distance / (frame_idx - prev_frame_idx)
                    if speed < PARKING_THRESHOLD:
                        unusual_events.append({
                            'label': label,
                            'bbox': bbox,
                            'speed': speed,
                            'event': 'Car Parked'
                        })

    if people_count > GATHERING_THRESHOLD:
        people_positions = [obj['bbox'] for obj in detected_objects if obj['label'] == 'person']
        for i, person_1 in enumerate(people_positions):
            for j, person_2 in enumerate(people_positions):
                if i != j:
                    dist = np.sqrt((person_1[0] - person_2[0]) ** 2 + (person_1[1] - person_2[1]) ** 2)
                    if dist < CLOSE_DISTANCE_THRESHOLD:
                        unusual_events.append({
                            'label': 'people',
                            'bbox': None,
                            'speed': 0,
                            'event': 'Gathering of People'
                        })
                        # play_alert_sound()
                        break

    return unusual_events

def process_frame(frame, frame_idx, output_folder, filename):
    """
    Process a single frame: detect objects, track movements, and save output if unusual events are found.
    """
    results = model(frame)
    detected_objects = []
    for result in results:
        for obj in result.boxes.data:
            x1, y1, x2, y2, score, class_id = obj.tolist()
            label = model.names[int(class_id)]
            if label in TARGET_CLASSES:
                detected_objects.append({'bbox': [int(x1), int(y1), int(x2), int(y2)], 'label': label})

    # Track object movement and detect unusual events
    unusual_events = track_object_movement(frame_idx, detected_objects)

    # Annotate the frame and save the output if unusual events are detected
    if unusual_events:
        for event in unusual_events:
            event_type = event['event']
            
            if event_type == 'Gathering of People':
                # Handle gathering of people (no bounding box, just mark all people)
                for obj in detected_objects:
                    if obj['label'] == 'person':
                        x1, y1, x2, y2 = obj['bbox']
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for gathering
                        cv2.putText(frame, 'Gathering', (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                # For other events (speeding, parked car), draw bounding box
                if event['bbox'] is not None:
                    x1, y1, x2, y2 = event['bbox']
                    label = event['label']
                    speed = event['speed']
                    
                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red for other events
                    cv2.putText(frame, f'{label} {event_type} ({speed:.2f})', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        event_obj = UnusualEvent(event=event_type, image=frame)
        event_obj.save_to_db()
        return event_obj
    else:
        print('No unusual events detected in this frame.')
        return None




def process_all_frames(frames_folder, output_folder):
    while True:  # Infinite loop to keep checking for new frames
        frame_files = sorted(os.listdir(frames_folder))
        result=False
        for frame_idx, frame_file in enumerate(frame_files):
            
            frame_path = os.path.join(frames_folder, frame_file)
            frame = cv2.imread(frame_path)
            
            if frame is not None:
                result_obj=process_frame(frame, frame_idx, output_folder, frame_file)
            if result_obj!=None:
                result=result_obj  
                with open('Functions/output.txt', 'a') as file:
                    # Write some text to the file
                    file.write("unusual event:"+ str(result)+'\n')
            else:
                with open('Functions/output.txt', 'a') as file:
                    # Write some text to the file

                    file.write("no unusual events found"+'\n')
            time.sleep(1)

def delete_images_from_directory(directory_path):
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff']
    
    for extension in image_extensions:
        images = glob.glob(os.path.join(directory_path, extension))
        for image in images:
            try:
                os.remove(image)
                print(f"Deleted: {image}")
            except Exception as e:
                print(f"Error deleting {image}: {e}")

