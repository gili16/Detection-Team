# #pip install ultralytics

# import cv2
# import time
# import numpy as np
# import os
# from sort.sort import Sort
# import torch

# # Object detection model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  

# def track_objects(frames_folder, bounding_box, video_name, interval=600):
#     """
#     Tracks people and vehicles in a defined area for frames in a folder.
#     """
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     result_folder = os.path.join('results_tracking_in_area', f"{video_name}_{timestamp}")
#     os.makedirs(result_folder, exist_ok=True)

#     # Create a new folder for enlarged images
#     enlarged_folder = os.path.join(result_folder, 'enlarged_objects')
#     os.makedirs(enlarged_folder, exist_ok=True)

#     start_time = time.time()
#     tracker = Sort()
#     frame_files = [f for f in os.listdir(frames_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
#     tracked_objects = {}  # Store for found objects

#     # Variables for counting people and cars
#     total_people = 0
#     total_cars = 0

#     for frame_file in frame_files:
#         frame_path = os.path.join(frames_folder, frame_file)
#         frame = cv2.imread(frame_path)
#         if frame is None or (time.time() - start_time) > interval:
#             break
        
#         # Perform object detection
#         results = model(frame)

#         current_count = 0  # Count objects in the current frame
#         detections = []

#         # Mark the bounding box of the selected area
#         cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0, 255, 0), 2)

#         for *box, conf, cls in results.xyxy[0]:
#             x1, y1, x2, y2 = map(int, box)
#             label = model.names[int(cls)]
            
#             # Check if the object is within the defined bounding box
#             if x1 >= bounding_box[0] and y1 >= bounding_box[1] and x2 <= bounding_box[2] and y2 <= bounding_box[3]:
#                 detections.append([x1, y1, x2, y2, conf])  # Add object to detections
#                 current_count += 1

#                 # Count people and cars
#                 object_id = f"{label}_{current_count}"  # Uniqueness by object type
#                 if label == "person" and object_id not in tracked_objects:
#                     total_people += 1
#                 elif label == "car" and object_id not in tracked_objects:
#                     total_cars += 1

#                 # Mark the object on the frame
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
#                 cv2.putText(frame, f"{label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#                 # Cut and save the enlarged image of the object only if it hasn’t been identified before
#                 if object_id not in tracked_objects:
#                     tracked_objects[object_id] = True  # Add the object to the set
#                     object_image = frame[y1:y2, x1:x2]
#                     cv2.putText(object_image, label, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#                     enlarged_image_path = os.path.join(enlarged_folder, f"{frame_file[:-4]}_{label}_{total_people + total_cars}.jpg")
#                     cv2.imwrite(enlarged_image_path, object_image)

#         # Update the tracker if objects were found
#         if detections:
#             detections = np.array(detections)  # [x1, y1, x2, y2, score]
#             trackers = tracker.update(detections)

#         # Save the highlighted frame in the results folder
#         result_frame_path = os.path.join(result_folder, frame_file)
#         cv2.imwrite(result_frame_path, frame)

#     # Save the number of objects in a text file
#     count_file_path = os.path.join(result_folder, 'object_counts.txt')
#     with open(count_file_path, 'w') as count_file:
#         count_file.write(f"Total unique objects tracked: {len(tracked_objects)}\n")
#         count_file.write(f"Total people tracked: {total_people}\n")
#         count_file.write(f"Total cars tracked: {total_cars}\n")

#     return len(tracked_objects), tracked_objects, total_people, total_cars


# frames_folder = 'video/M0202'  # Path to the frames folder
# video_name = 'M0202'  # Video name (for use in the results folder)
# bounding_box = (20, 20, 400, 400)  # Boundaries of the area: (x1, y1, x2, y2)
# object_count, tracked_objects, total_people, total_cars = track_objects(frames_folder, bounding_box, video_name)
# print(f"Number of unique objects tracked: {object_count}")
# print(f"Total people tracked: {total_people}")
# print(f"Total cars tracked: {total_cars}")
# print(f"Tracked Object IDs: {tracked_objects}")


#pip install opencv-python
# import cv2
# import time
# import numpy as np
# import os
# from sort.sort import Sort
# import torch

# # Object detection model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# def track_objects(frames_folder, bounding_box, video_name, interval=600, process_interval=1):
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     result_folder = os.path.join('results_tracking_in_area', f"{video_name}_{timestamp}")
#     os.makedirs(result_folder, exist_ok=True)

#     enlarged_folder = os.path.join(result_folder, 'enlarged_objects')
#     os.makedirs(enlarged_folder, exist_ok=True)

#     start_time = time.time()
#     tracker = Sort()
#     frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(('.jpg', '.png', '.jpeg'))])
#     tracked_objects = {}

#     total_people = 0
#     total_cars = 0
#     last_process_time = time.time()
#     summary = []

#     for frame_file in frame_files:
#         frame_path = os.path.join(frames_folder, frame_file)
#         frame = cv2.imread(frame_path)
#         if frame is None or (time.time() - start_time) > interval:
#             break
        
#         current_time = time.time()

#         if current_time - last_process_time >= process_interval:
#             results = model(frame)
#             print(f"Results for {frame_file}: {results.xyxy[0].shape[0]} detections")
#             last_process_time = current_time
#             detections = []
            
#             # Draw the bounding box around the selected area
#             cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0, 255, 0), 2)

#             if results is not None:
#                 for *box, conf, cls in results.xyxy[0]:
#                     x1, y1, x2, y2 = map(int, box)
#                     label = model.names[int(cls)]

#                     # Check if the object is within the defined bounding box and is either a person or a car
#                     if label in ["person", "car"] and x1 >= bounding_box[0] and y1 >= bounding_box[1] and x2 <= bounding_box[2] and y2 <= bounding_box[3]:
#                         detections.append([x1, y1, x2, y2, conf])
#                         object_id = f"{label}_{len(detections)}"

#                         if label == "person" and object_id not in tracked_objects:
#                             total_people += 1
#                         elif label == "car" and object_id not in tracked_objects:
#                             total_cars += 1

#                         # Draw the object on the frame
#                         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
#                         cv2.putText(frame, f"{label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#                         if object_id not in tracked_objects:
#                             tracked_objects[object_id] = True
#                             object_image = frame[y1:y2, x1:x2]
#                             enlarged_image_path = os.path.join(enlarged_folder, f"{frame_file[:-4]}_{label}_{total_people + total_cars}.jpg")
#                             cv2.imwrite(enlarged_image_path, object_image)

#             if detections:
#                 detections = np.array(detections)
#                 trackers = tracker.update(detections)

#             result_frame_path = os.path.join(result_folder, f"{int(current_time)}_{frame_file}")
#             cv2.imwrite(result_frame_path, frame)

#             # Save summary of detections
#             summary.append({"timestamp": int(current_time), "people": total_people, "cars": total_cars})

#     # Save counts to text file
#     count_file_path = os.path.join(result_folder, 'object_counts.txt')
#     with open(count_file_path, 'w') as count_file:
#         count_file.write(f"Total unique objects tracked: {len(tracked_objects)}\n")
#         count_file.write(f"Total people tracked: {total_people}\n")
#         count_file.write(f"Total cars tracked: {total_cars}\n")

#     # Save summary counts to a separate text file
#     summary_file_path = os.path.join(result_folder, 'summary_counts.txt')
#     with open(summary_file_path, 'w') as summary_file:
#         for entry in summary:
#             summary_file.write(f"Timestamp: {entry['timestamp']}, People: {entry['people']}, Cars: {entry['cars']}\n")

#     return summary

# # Define parameters
# frames_folder = 'video/M0202'  # Path to the frames folder
# video_name = 'M0202'  # Video name (for use in the results folder)
# bounding_box = (20, 20, 400, 400)  # Boundaries of the area: (x1, y1, x2, y2)

# # Track objects and get summary
# summary = track_objects(frames_folder, bounding_box, video_name)

# # Print summary
# for entry in summary:
#     print(f"Timestamp: {entry['timestamp']}, People: {entry['people']}, Cars: {entry['cars']}")


import warnings
import cv2
import os
import torch
from datetime import datetime
import sys
import os
import grpc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
warnings.filterwarnings("ignore", category=FutureWarning)

# Load the model for object detection
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)

# def track_objects(frames_folder, bounding_box, video_name):
#     frame_rate = 30  # Assume 30 FPS
#     object_count_per_second = {}

#     # Create a timestamp for the results folder
#     timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
#     results_folder = f'results_tracking_in_area/{video_name}_{timestamp}'
#     os.makedirs(results_folder, exist_ok=True)

#     # Set to track cars seen in the current 2-second interval
#     seen_cars = set()

#     # Read images from the folder
#     for frame_name in sorted(os.listdir(frames_folder)):
#         frame_path = os.path.join(frames_folder, frame_name)

#         if not frame_name.endswith('.jpg'):
#             continue

#         frame = cv2.imread(frame_path)

#         if frame is None:
#             continue  # Skip images that failed to load

#         # Extract frame index
#         try:
#             frame_index = int(frame_name.split('.')[0].replace('img', ''))  # Assuming 'img000001' format
#         except ValueError:
#             continue  # Skip files that cannot be converted to an integer

#         # Calculate the current second
#         current_second = frame_index // frame_rate

#         # Crop to the bounding box area
#         x1, y1, x2, y2 = bounding_box
#         cropped_frame = frame[y1:y2, x1:x2]

#         # Object detection in the selected area
#         results = model(cropped_frame)

#         # Track unique cars and people for this specific second
#         current_cars = set()
#         current_people = 0

#         for box in results.xyxy[0]:
#             x1_box, y1_box, x2_box, y2_box, conf, cls = box.tolist()
#             label = model.names[int(cls)]

#             if label == "person":
#                 current_people += 1
#             elif label == "car":
#                 car_id = f"{int(x1_box)}_{int(y1_box)}"  # Unique ID for the car
#                 current_cars.add(car_id)

#         # Update seen cars only if we are at a 2-second interval
#         if current_second % 2 == 0:
#             new_cars = current_cars - seen_cars  # Cars seen for the first time
#             seen_cars.update(current_cars)  # Update the seen cars set
#             object_count_per_second[current_second] = {
#                 'people': current_people,
#                 'cars': len(new_cars)  # Count only new cars
#             }
#         else:
#             # For non-2-second intervals, do not count
#             continue

#         # Draw bounding boxes on the original frame
#         for box in results.xyxy[0]:
#             x1_box, y1_box, x2_box, y2_box, conf, cls = box.tolist()
#             label = model.names[int(cls)]
#             if label in ["person", "car"]:
#                 x1_box += x1
#                 y1_box += y1
#                 x2_box += x1
#                 y2_box += y1
#                 color = (0, 255, 0) if label == "person" else (255, 0, 0)
#                 cv2.rectangle(frame, (int(x1_box), int(y1_box)), (int(x2_box), int(y2_box)), color, 2)
#                 cv2.putText(frame, label, (int(x1_box), int(y1_box) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

#         # Draw a frame around the bounding box area
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red frame for selected area

#         # Save the processed frame every 2 seconds
#         if current_second % 2 == 0:
#             result_frame_path = os.path.join(results_folder, f"result_{current_second:02d}.jpg")
#             cv2.imwrite(result_frame_path, frame)

#     # Print results in the desired format
#     for second, counts in object_count_per_second.items():
#         time_str = f"00:00:{second:02d}"
#         print(f"{time_str} - People: {counts['people']}, Cars: {counts['cars']}")
#         with grpc.insecure_channel('localhost:50051') as channel:
#             stub = allert_server_pb2_grpc.AlertServiceStub(channel)
#             response = stub.SetCountResult(allert_server_pb2.SetCountResultRequest(
#                 count=counts['people']+counts['cars']
#             ))
#             print("SetCountResultResonse:", response.message)

import time
# git clone https://github.com/ultralytics/yolov5.git
# cd yolov5
# pip install -r requirements.txt

def track_objects(frames_folder, bounding_box):
    # Load the model for object detection
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')

    frame_rate = 30  # Assume 30 FPS
    object_count_per_second = {}
    
    # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # results_folder = f'results_tracking_in_area/{video_name}_{timestamp}'
    # os.makedirs(results_folder, exist_ok=True)

    seen_cars = set()
    processed_frames = set()  # To track processed frames
    last_save_time = time.time()  # To track last save time

    while True:  # Infinite loop to keep checking for new frames
        new_frames = sorted(os.listdir(frames_folder))

        for frame_name in new_frames:
            frame_path = os.path.join(frames_folder, frame_name)

            if not frame_name.endswith('.jpg') or frame_name in processed_frames:
                continue

            frame = cv2.imread(frame_path)

            if frame is None:
                continue  # Skip images that failed to load

            try:
                frame_index = int(frame_name.split('.')[0].replace('img', ''))  # Assuming 'img000001' format
            except ValueError:
                continue  # Skip files that cannot be converted to an integer

            current_second = frame_index // frame_rate
            x1, y1, x2, y2 = bounding_box
            cropped_frame = frame[y1:y2, x1:x2]
            results = model(cropped_frame)

            current_cars = set()
            current_people = 0

            for box in results.xyxy[0]:
                x1_box, y1_box, x2_box, y2_box, conf, cls = box.tolist()
                label = model.names[int(cls)]

                if label == "person":
                    current_people += 1
                elif label == "car":
                    car_id = f"{int(x1_box)}_{int(y1_box)}"
                    current_cars.add(car_id)

            if current_second % 2 == 0:
                new_cars = current_cars - seen_cars
                seen_cars.update(current_cars)
                object_count_per_second[current_second] = {
                    'people': current_people,
                    'cars': len(new_cars)
                }

            # Draw bounding boxes and save the frame as before
            # for box in results.xyxy[0]:
            #     x1_box, y1_box, x2_box, y2_box, conf, cls = box.tolist()
            #     label = model.names[int(cls)]
            #     if label in ["person", "car"]:
            #         x1_box += x1
            #         y1_box += y1
            #         x2_box += x1
            #         y2_box += y1
            #         color = (0, 255, 0) if label == "person" else (255, 0, 0)
            #         cv2.rectangle(frame, (int(x1_box), int(y1_box)), (int(x2_box), int(y2_box)), color, 2)
            #         cv2.putText(frame, label, (int(x1_box), int(y1_box) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # if current_second % 2 == 0:
            #     result_frame_path = os.path.join(results_folder, f"result_{current_second:02d}.jpg")
            #     cv2.imwrite(result_frame_path, frame)

            processed_frames.add(frame_name)  # Mark this frame as processed

        # Check if 10 seconds have passed since last save
        if time.time() - last_save_time >= 10:
            total_people = sum(counts['people'] for counts in object_count_per_second.values())
            total_cars = sum(counts['cars'] for counts in object_count_per_second.values())
            total_count = total_people + total_cars
            
            time_str = datetime.now().strftime("%H:%M:%S")
            with open('Functions/output.txt', 'a') as file:
                    # Write some text to the file
                    file.write(f"{time_str} - Total People: {total_people}, Total Cars: {total_cars}")
            # print(f"{time_str} - Total People: {total_people}, Total Cars: {total_cars}")
            
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                response = stub.SetCountResult(allert_server_pb2.SetCountResultRequest(
                    count=total_count
                ))
                with open('Functions/output.txt', 'a') as file:
                    # Write some text to the file
                    file.write("count:"+ str(total_count)+'\n')

            last_save_time = time.time()  # Update last save time
            object_count_per_second.clear()  # Clear counts for the next 10 seconds

        time.sleep(0.1)  # Sleep for a short time before checking for new frames again


# Call the function
if __name__ == "__main__":
    frames_folder = 'video/M0202'  # Path to the frames folder
    video_name = 'M0202'  # Video name
    bounding_box = (20, 20, 400, 400) 
    track_objects(frames_folder, bounding_box, video_name)
