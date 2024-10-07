
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta  # Import necessary modules
# from Functions.object_tracking import (track_frames)


def is_bbox_overlapping(bounding_box, bbox_obj):
    """
    Check if the bounding box of an object overlaps with the specified bounding box.

    Parameters:
    - bounding_box: Tuple containing (x_min, y_min, width, height) for the outer bounding box.
    - bbox_obj: Tuple containing (x_min, y_min, width, height) for the inner bounding box.

    Returns:
    - True if there is an overlap, False otherwise.
    """
    x_min, y_min, w, h = bounding_box #10 10 100 100
    x_max = x_min + w # 110
    y_max = y_min + h #110
    
    obj_x_min, obj_y_min, obj_w, obj_h = bbox_obj #110 110 50 50
    obj_x_max = obj_x_min + obj_w #160
    obj_y_max = obj_y_min + obj_h #160

    # Check for any overlap
    return not (obj_x_max <= x_min or obj_x_min >= x_max or 
                obj_y_max <=y_min or obj_y_min >= y_max)

def in_last_seconds(timestamp, last_seconds):
    """
    Check if the given timestamp is within the last specified seconds.

    Parameters:
    - timestamp: The datetime of the object.
    - last_seconds: The threshold datetime to compare against.

    Returns:
    - True if the timestamp is more recent than last_seconds, False otherwise.
    """
    # cutoff_time = datetime.now() - timedelta(seconds=last_seconds)
    return True


def count_cars_and_people(tracked_objects, last_seconds, bounding_box):
    """
    Count distinct cars and people that are in the specified bounding box within the last seconds.

    Parameters:
    - tracked_objects: List of tracked objects with bounding boxes and timestamps.
    - last_seconds: The cutoff time to consider for counting objects.
    - bounding_box: The bounding box to check against.

    Returns:
    - A dictionary with counts of distinct 'car' and 'person' detected.
    """
    objects_detected = {"car": [], "person": []}
    for obj in tracked_objects:
        id_object = obj["Object"]
        cls = obj["Label"]
        bounding_boxes = obj["Bounding Boxes"]
        
        for bbox_info in bounding_boxes:  # Iterate through bounding boxes
            bbox_obj = bbox_info["bbox"]  # Get the bbox
            timestamp = bbox_info["datetime"]  # Get the timestamp directly
            
            # Ensure timestamp is a datetime object (optional check)
            if isinstance(timestamp, str):
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")  # Convert if it's a string
            
            if in_last_seconds(timestamp, last_seconds):
                if is_bbox_overlapping(bounding_box, bbox_obj):
                    objects_detected[cls].append(id_object)
                    break
            else:
                break
    return objects_detected  # Return the detected objects

# def count_in_area(frames_folder, bounding_box, seconds=10):
#     """
#     Count the number of distinct cars and people in a specified area over the last 'seconds'.

#     Parameters:
#     - frames_folder: Path to the folder containing video frames.
#     - bounding_box: The bounding box area to analyze.
#     - seconds: The number of seconds to look back for counting (default is 30 seconds).

#     Returns:
#     - A dictionary with counts of 'people' and 'cars'.
#     """
#     # Track frames and get start and end times
#     tracked_objects, start, end = track_frames(frames_folder)

#     # Convert 'end' to datetime if it is a string
#     if isinstance(end, str):
#         end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

#     # Calculate the time for the last specified seconds
#     last_seconds = end - timedelta(seconds=seconds)  # Use 'end' as a datetime object now

#     # Count detected cars and people
#     objects_detected = count_cars_and_people(tracked_objects, last_seconds, bounding_box)
    
#     # Prepare the result dictionary
#     result = {'people': len(objects_detected["person"]), 'cars': len(objects_detected["car"])}
#     return result
# if __name__ == "__main__":
#     frames_folder = 'video/M0202'  # Path to the video frames
#     bounding_box = (20, 20, 400, 400)  # Define the bounding box area
#     results = count_in_area(frames_folder, bounding_box, 50)  # Count objects in the area
    
#     # Print the total number of detected people and cars
#     print(f"Total - People: {results['people']}, Cars: {results['cars']}")
