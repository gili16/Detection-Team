import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Functions.detect_blur import process_image
from Functions.detect_cross import *
from Functions.people_alert import track_objects
# from Functions.tracking_in_area import track_objects as count_objects
from Functions.object_tracking import track_frames
# from Functions.detect_unusual_events import process_all_frames
def send_image(image):
    return process_image(image,threshold=750)


def track(image_queue):
    track_frames(image_queue)
# def odd_event(frames_directory,output_folder):
#     pass
    # process_all_frames(frames_directory,output_folder)

# def count(x1, y1, x2, y2,frames_directory):
#     count_objects(frames_directory,(x1,y1,x2,y2))

def accident():
    return True

def is_empty(image):
    x1,y1=0,0
    y2,x2=image.shape[:2]
    bounding_box=(x1,y1,x2,y2)
    return not track_objects(image,bounding_box)

def is_cross(line_start,line_end,frame):
    # output_folder = './frames'  # Folder to save processed frames
    # if os.path.exists(output_folder):
    #     delete_images_from_directory(output_folder)
    # Process all frames in the folder
    return process_frame(frame, line_start, line_end)



