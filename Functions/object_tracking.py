from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os
from datetime import datetime, timedelta
import time
from multiprocessing import Queue
import sys
import os
from pymongo import MongoClient
import grpc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Functions.tracking_in_area import count_cars_and_people
from Functions.unusual_event import detect_unusual_events
from Server import allert_server_pb2, allert_server_pb2_grpc
from Server.allert_server_pb2 import Event
from Functions.check_accidents import check_for_accidents
from Thread.utils import draw_bbox_with_text, draw_line,put_text_top_center
client = MongoClient('mongodb://localhost:27017/')  # MongoDB connection
db = client['AllertDB']
def track_frames(image_queue):
    start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Load the YOLO model
    model = YOLO("yolov8n.pt")
    
    # Initialize variables
    track_history = defaultdict(lambda: [])  # To store the object's tracking history
    object_data = defaultdict(lambda: {"label": None, "bboxes": []})  # Store label and bounding boxes with datetime
    last_save_time=time.time()
    is_count_allert_On=False
    is_unusual_allert_On=False
    is_accident_allert_On=False
    last_count_time=time.time()
    # Loop until a termination condition (e.g., queue is empty for too long)
    while True:
        if image_queue.empty():
            time.sleep(1)  # Wait for 1 second before checking the queue again
            continue
        
        try:
            if db['CountAllert'].find_one({'IsOn': True}):
                is_count_allert_On=True
                # last_count_time=time.time()
            else:
                is_count_allert_On=False
            if db['OddEventAllert'].find_one({'IsOn': True}):
                is_unusual_allert_On=True
            else:
                is_unusual_allert_On=False
            if db['AccidentAllert'].find_one({'IsOn': True}):
                is_accident_allert_On=True
            else:
                is_accident_allert_On=False
            # Get the frame (image data) from the queue
            frame,frame_id = image_queue.get(timeout=1)  # Waits for 1 second if the queue is empty

            if frame is None:
                print(f"Received empty frame from the queue.")
                continue

            # Perform object detection and tracking on the frame
            results = model.track(frame, persist=True)
            boxes = results[0].boxes.xywh.cpu()  # Get bounding boxes (x_center, y_center, width, height)
            class_ids = results[0].boxes.cls.int().cpu().tolist()  # Get class IDs for labeling
            track_ids = (
                results[0].boxes.id.int().cpu().tolist()
                if results[0].boxes.id is not None
                else None
            )
            
            # Get current datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save bounding boxes and track object paths
            if track_ids:
                for box, class_id, track_id in zip(boxes, class_ids, track_ids):
                    x, y, w, h = box
                    label = model.names[class_id]  # Get object label from YOLO model names
                    # Initialize the object data for a new track ID if it doesn't exist
                    if track_id not in object_data:
                        object_data[track_id] = {
                            "label": None,  # Placeholder for label
                            "bboxes": []    # List to hold bounding boxes
                        }
                    # Set the label once if not already set
                    if object_data[track_id]["label"] is None:
                        object_data[track_id]["label"] = label

                    # Append bbox and datetime to the object data
                    object_data[track_id]["bboxes"].append({
                        "bbox": (int(x - w / 2), int(y - h / 2), int(w), int(h)), 
                        "datetime": current_time,
                        "frame_id":frame_id
                    })
            if time.time()-last_save_time>2:
                tracked_objects = []
                for track_id, data in object_data.items():
                    tracked_objects.append({
                        "Object": track_id,
                        "Label": data["label"],
                        "Bounding Boxes": data["bboxes"]
                    })
                if is_count_allert_On:
                    x1=(db['CountAllert'].find_one({'IsOn': True}))['coordinate1'][0]
                    y1=(db['CountAllert'].find_one({'IsOn': True}))['coordinate1'][1]
                    x2=(db['CountAllert'].find_one({'IsOn': True}))['coordinate2'][0]
                    y2=(db['CountAllert'].find_one({'IsOn': True}))['coordinate2'][1] 
                    txt="object detected: 0"
                    if (time.time()-last_count_time>4):                         
                        counted_object=count_cars_and_people(tracked_objects,timedelta(seconds=30),(x1,y1,x2,y2))
                        # print(counted_object)
                        with grpc.insecure_channel('localhost:50051') as channel:
                                stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                                
                                response = stub.SetCountResult(allert_server_pb2.SetCountResultRequest(
                                    count=len(counted_object['person'])+len(counted_object['car'])
                                ))
                        last_count_time=time.time()
                        txt="object detected: "+str(len(counted_object['person'])+len(counted_object['car']))
                    
                    frame=draw_bbox_with_text(frame,(x1,y1,x2,y2),txt)
                if is_accident_allert_On:
                    is_accident_occured=False
                    try:
                        is_accident_occured,_=check_for_accidents(tracked_objects)
                    except:
                        is_accident_occured=False
                    with grpc.insecure_channel('localhost:50051') as channel:
                            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                            
                            response = stub.SetAccidentResult(allert_server_pb2.SetAccidentResultRequest(
                                accident=is_accident_occured
                            ))
                    print("accident? ",is_accident_occured)

                if is_unusual_allert_On:
                    unusual_events=detect_unusual_events(tracked_objects)
                    for event in unusual_events:
                        event_data = Event(
                            date= str(event['time']),
                            description= event['event']
                        )
                        with grpc.insecure_channel('localhost:50051') as channel:
                            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                            
                            response = stub.SetOddEventResult(allert_server_pb2.SetOddEventResultRequest(
                                odd_event=event_data
                            ))
                        try:
                            frame=draw_bbox_with_text(frame,event['bbox'],event['event'])
                        except:
                            print("")

                is_success, buffer = cv2.imencode(".jpg", frame) 
                if is_success:
                    with grpc.insecure_channel('localhost:50051') as channel:
                        stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                        response = stub.SetOverallImageResult(allert_server_pb2.SetOverallImageResultRequest(
                            image=buffer.tobytes()
                        ))
                        print("overall saved")
                # Remove the oldest quarter of entries if the list exceeds a certain length
            if time.time()-last_save_time>10:
                print('object data removal')
                object_data = {key: value for key, value in object_data.items() if value['bboxes']}

                total_length = 0

                for track_id, data in object_data.items():
                    total_length += len(data["bboxes"])
                if total_length>300:
                    for track_id,_ in object_data.items():
                        if len(object_data[track_id]["bboxes"]) > 4:
                            quarter_length = len(object_data[track_id]["bboxes"]) // 2
                            object_data[track_id]["bboxes"] = object_data[track_id]["bboxes"][quarter_length:]
                last_save_time=time.time()
                # print('object data:',object_data)

        # except image_queue.empty():
        #     # In case the queue remains empty after the timeout, we can break the loop or continue waiting
        #     print("Queue is empty, waiting for new frames...")
        #     time.sleep(1)  # Wait before the next check
        except KeyboardInterrupt:
            break

        # Optionally, you could add a condition to break the loop (e.g., based on time or frame count)
        # e.g., break when certain conditions are met or external signal to stop processing

    # Convert object data to a structured format with label and bboxes
    tracked_objects = []
    for track_id, data in object_data.items():
        tracked_objects.append({
            "Object": track_id,
            "Label": data["label"],
            "Bounding Boxes": data["bboxes"]
        })
    
    end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return tracked_objects, start, end

# if __name__=='__main__':
#     # Example usage:
#     input_folder = './input/M0202'  # Path to your input frames
#     output_bboxes,start,end = track_frames(input_folder)

#     # Print the bounding boxes array for each tracked object
#     for obj in output_bboxes:
#         print(f"Object {obj['Object']} Label: {obj['Label']}, Bounding Boxes: {obj['Bounding Boxes']}")
#     print(f"start: {start},end:{end}")