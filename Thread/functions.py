import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Functions.detect_blur import process_image
from Functions.detect_cross import *
from Functions.people_alert import track_objects
from Functions.tracking_in_area import track_objects as count_objects
from Functions.detect_unusual_events import process_all_frames
def send_image(image):
    return process_image(image,threshold=750)

def odd_event(frames_directory,output_folder):
    process_all_frames(frames_directory,output_folder)

def count(x1, y1, x2, y2,frames_directory):
    count_objects(frames_directory,(x1,y1,x2,y2))

def accident():
    return True

def is_empty(image):
    x1,y1=0,0
    y2,x2=image.shape[:2]
    bounding_box=(x1,y1,x2,y2)
    return track_objects(image,bounding_box)

def is_cross(frames_directory,line_start,line_end,frame,filename):
    frames_folder = frames_directory  # Path to folder containing all video frames
    # first_frame_path = './M0802/img000826.jpg'  # Path to the first frame image
    # marked_frame_output = './marked_frame.jpg'  # Path to save the marked first frame image
    
    # mark_objects_on_first_frame(frame, marked_frame_output)
    # line_start = (50, 0)  # Coordinates of the line start
    # line_end = (1450, 1000)    # Coordinates of the line end
    output_folder = './frames'  # Folder to save processed frames
    if os.path.exists(output_folder):
        delete_images_from_directory(output_folder)
    # Process all frames in the folder
    return process_frame(frame, line_start, line_end, output_folder,filename)
