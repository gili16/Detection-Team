import sys
import os
import grpc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
import warnings
import cv2
import os
import torch
import numpy as np
from datetime import datetime

warnings.filterwarnings("ignore", category=FutureWarning)

# Load the YOLOv5 model for object detection
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', force_reload=True)

def calculate_color_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

def is_same_object(new_hist, existing_hists, new_bbox, existing_bboxes, color_threshold=0.5, distance_threshold=50):
    for existing_hist, existing_bbox in zip(existing_hists, existing_bboxes):
        if cv2.compareHist(new_hist, existing_hist, cv2.HISTCMP_CORREL) > color_threshold:
            new_center = get_center(new_bbox)
            existing_center = get_center(existing_bbox)
            if np.linalg.norm(np.array(new_center) - np.array(existing_center)) < distance_threshold:
                return True
    return False

def get_center(bbox):
    return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)

def process_detections(cropped_frame, current_second, tracked_objects, current_id):
    results = model(cropped_frame)
    for box in results.xyxy[0]:
        x1_box, y1_box, x2_box, y2_box, _, cls = box.tolist()
        label = model.names[int(cls)]
        if label in ["person", "car"]:
            # Check if the entire object is within the bounding box
            if is_object_fully_within_bbox((x1_box, y1_box, x2_box, y2_box)):
                obj_image = cropped_frame[int(y1_box):int(y2_box), int(x1_box):int(x2_box)]
                if obj_image.size > 0:
                    new_hist = calculate_color_histogram(obj_image)
                    new_bbox = (x1_box, y1_box, x2_box, y2_box)
                    current_id = update_tracked_objects(new_hist, new_bbox, label, tracked_objects, current_second, current_id, obj_image)
    return tracked_objects, current_id

def is_object_fully_within_bbox(bbox):
    # Implement logic to check if the bbox is fully within the specified area
    return True  # Adjust this logic based on your needs

def update_tracked_objects(new_hist, new_bbox, label, tracked_objects, current_second, current_id, obj_image):
    matched = False
    for obj_id, obj_info in tracked_objects.items():
        if is_same_object(new_hist, obj_info['histograms'], new_bbox, obj_info['bboxes']):
            obj_info['last_seen'] = current_second
            obj_info['histograms'].append(new_hist)
            obj_info['bboxes'].append(new_bbox)
            matched = True
            break
    if not matched:
        tracked_objects[current_id] = {
            'label': label,
            'histograms': [new_hist],
            'bboxes': [new_bbox],
            'last_seen': current_second
        }
        save_detected_object(obj_image, label, current_id, current_second)
        current_id += 1
    return current_id

def save_detected_object(obj_image, label, current_id, current_second):
    detected_objects_folder = f'results_tracking_in_area/{current_second}/detected_objects'
    os.makedirs(detected_objects_folder, exist_ok=True)

    object_image_path = os.path.join(detected_objects_folder, f"{label}_{current_id}.jpg")
    cv2.putText(obj_image, label, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.imwrite(object_image_path, obj_image)

def track_objects(frames_folder, bounding_box):
    frame_rate = 30
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    results_folder = f'results_tracking_in_area/{timestamp}'
    os.makedirs(results_folder, exist_ok=True)

    tracked_objects = {}
    current_id = 0
    processed_frames=set()

    while True:        
        for frame_index, frame_name in enumerate(sorted(os.listdir(frames_folder))):
            print("hello count")
            frame_path = os.path.join(frames_folder, frame_name)
            if not frame_name.endswith('.jpg') and frame_name not in processed_frames:
                continue
            processed_frames.add(frame_name)
            frame = cv2.imread(frame_path)
            if frame is None:
                continue

            current_second = frame_index // frame_rate
            x1, y1, x2, y2 = bounding_box
            cropped_frame = frame[y1:y2, x1:x2]

            tracked_objects, current_id = process_detections(cropped_frame, current_second, tracked_objects, current_id)

            # Remove objects not seen in the last 30 seconds
            tracked_objects = {k: v for k, v in tracked_objects.items() if current_second - v['last_seen'] < 30}

            # Save a frame every 10 seconds with bounding boxes
            if current_second % 4 == 0:
                results=summarize_results(tracked_objects)
                with open('Functions/output.txt', 'a') as file:
                        # Write some text to the file
                        file.write(f"{current_second} - {results}\n")
                # print(f"{time_str} - Total People: {total_people}, Total Cars: {total_cars}")
                print("count"+str(results))
                with grpc.insecure_channel('localhost:50051') as channel:
                    stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                    response = stub.SetCountResult(allert_server_pb2.SetCountResultRequest(
                        count=results['people']+results['cars']
                    ))
                    
                # save_frame_with_bboxes(frame, bounding_box, tracked_objects, results_folder, current_second)


def save_frame_with_bboxes(frame, bounding_box, tracked_objects, results_folder, current_second):
    cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0, 255, 0), 2)
    for obj_id, obj_info in tracked_objects.items():
        if obj_info['bboxes']: 
            color = (0, 0, 255)  # Red color for tracked objects
            bbox = obj_info['bboxes'][-1]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.putText(frame, f"{obj_info['label']}", (int(bbox[0]), int(bbox[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    result_frame_path = os.path.join(results_folder, f"result_{current_second:02d}.jpg")
    cv2.imwrite(result_frame_path, frame)

def summarize_results(tracked_objects):
    total_people = len([v for v in tracked_objects.values() if v['label'] == "person"])
    total_cars = len([v for v in tracked_objects.values() if v['label'] == "car"])
    return {"people": total_people, "cars": total_cars}

# if __name__ == "__main__":
#     frames_folder = '../../../to_git/detection-team/training/DATA/UAV-benchmark-M/M0202'  
#     bounding_box = (20, 20, 400, 400) 
#     results = track_objects(frames_folder, bounding_box)
    
#     print(f"Total - People: {results['people']}, Cars: {results['cars']}")
