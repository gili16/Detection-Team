import cv2
import numpy as np
import os
from ultralytics import YOLO
import glob
# Load a pre-trained YOLOv8 model
model = YOLO('yolov8n.pt')

# Classes corresponding to people and vehicles in YOLOv8
TARGET_CLASSES = ['person', 'car', 'bus', 'truck', 'motorcycle', 'bicycle']

def detect_objects(frame):
    """
    Detect people and vehicles in a frame using YOLOv8 and apply non-max suppression.
    """
    results = model(frame)
    detected_objects = []
    
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
        confs = result.boxes.conf.cpu().numpy()  # Confidence scores
        clss = result.boxes.cls.cpu().numpy()    # Class IDs
        
        # Filter detected objects based on target classes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(clss[i])]
            
            if label in TARGET_CLASSES:
                detected_objects.append({
                    'label': label,
                    'bbox': (x1, y1, x2, y2),
                    'confidence': confs[i]
                })
    
    # Apply non-max suppression to remove duplicate/overlapping detections
    detected_objects = apply_nms(detected_objects)
    
    return detected_objects

def apply_nms(objects, iou_threshold=0.5):
    """
    Apply Non-Maximum Suppression (NMS) to avoid detecting the same object multiple times.
    """
    if len(objects) == 0:
        return []

    boxes = np.array([obj['bbox'] for obj in objects])
    scores = np.array([obj['confidence'] for obj in objects])

    # Apply OpenCV NMS
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), score_threshold=0.4, nms_threshold=iou_threshold)

    filtered_objects = []
    if len(indices) > 0:
        for i in indices.flatten():
            filtered_objects.append(objects[i])
    
    return filtered_objects

def draw_line_on_image(image, coord1, coord2):
    """
    Draw a line on the image between two coordinates.
    """
    image_with_line = image.copy()
    cv2.line(image_with_line, coord1, coord2, color=(0, 255, 0), thickness=2)
    return image_with_line

def point_on_line_segment(point, line_start, line_end):
    """
    Check if a point lies on the finite line segment between line_start and line_end.
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # Check if the point is within the bounding box defined by the line segment
    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
        # Calculate the area of the triangle formed by the point and the line segment
        area = abs((x2 - x1) * (py - y1) - (y2 - y1) * (px - x1))
        line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distance = area / line_length
        
        # If the perpendicular distance is small enough, the point is on the line segment
        return distance < 5  # Small threshold for precision
    return False

def check_if_on_line_segment(bbox, line_coord1, line_coord2):
    """
    Check if the center of the bounding box of an object is on the finite line segment.
    """
    x1, y1, x2, y2 = bbox
    box_center = ((x1 + x2) // 2, (y1 + y2) // 2)
    
    # Check if the box center is on the line segment
    return point_on_line_segment(box_center, line_coord1, line_coord2)

def annotate_frame(image, bbox, label, color=(0, 0, 255)):
    """
    Draw bounding box and label on the frame.
    """
    x1, y1, x2, y2 = bbox
    # Draw the rectangle around the object
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    # Put the label text above the rectangle
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

def process_frame(image, coord1, coord2, output_path, filename):
    """
    Process a frame to:
    - Draw a line
    - Detect objects
    - Check if any object is on the line segment and mark it
    - Save the frame if an object is on the line segment
    """
    # Draw the line on the image
    image_with_line = draw_line_on_image(image, coord1, coord2)
    
    # Detect objects
    detected_objects = detect_objects(image_with_line)
    
    object_on_line = False  # To track if any object is exactly on the line segment
    
    # Check if any object is on the line segment
    for obj in detected_objects:
        bbox = obj['bbox']
        if check_if_on_line_segment(bbox, coord1, coord2):
            object_on_line = True
            # Annotate the object that is on the line segment
            annotate_frame(image_with_line, bbox, obj['label'], color=(0, 0, 255))
    
    # If an object is on the line segment, save the frame
    if object_on_line:
        output_frame_path = os.path.join(output_path, filename)
        cv2.imwrite(output_frame_path, image_with_line)
        print(f"Object found on the line in frame {filename}. Saved with annotation.")
    return object_on_line

def process_all_frames_cross(folder_path, coord1, coord2, output_folder):
    """
    Process all frames in the folder and check for objects on the line segment.
    """
    
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    is_cross=False
    # Loop through all image files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            # Read each image frame
            frame_path = os.path.join(folder_path, filename)
            frame = cv2.imread(frame_path)
            
            if frame is None:
                print(f"Failed to load {filename}")
                continue

            # Process the frame
            is_cross=is_cross or process_frame(frame, coord1, coord2, output_folder, filename)
            
    return is_cross

def delete_images_from_directory(directory_path):
    # Supported image file extensions
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff']
    
    # Loop through each file extension and delete the images
    for extension in image_extensions:
        images = glob.glob(os.path.join(directory_path, extension))
        for image in images:
            try:
                os.remove(image)
                print(f"Deleted: {image}")
            except Exception as e:
                print(f"Error deleting {image}: {e}")

def mark_objects_on_first_frame(frame, output_path):
    """
    Detect objects in the first frame, mark them, and save the marked frame in a separate directory.
    """
    # frame = cv2.imread(frame_path)
    
    if frame is None:
        print(f"Failed to load the frame at ")
        return
    
    # Detect objects in the frame
    detected_objects = detect_objects(frame)
    
    # Annotate each detected object on the frame
    for obj in detected_objects:
        bbox = obj['bbox']
        label = obj['label']
        annotate_frame(frame, bbox, label, color=(0, 0, 255))
    
    # Save the marked frame in the output directory
    cv2.imwrite(output_path, frame)
    print(f"Marked objects on the first frame saved at {output_path}")


# Example usage
if __name__ == "__main__":
    frames_folder = './M0802'  # Path to folder containing all video frames
    first_frame_path = './M0802/img000826.jpg'  # Path to the first frame image
    marked_frame_output = './marked_frame.jpg'  # Path to save the marked first frame image
    
    mark_objects_on_first_frame(first_frame_path, marked_frame_output)
    line_start = (50, 0)  # Coordinates of the line start
    line_end = (1450, 1000)    # Coordinates of the line end
    output_folder = './processed_frames'  # Folder to save processed frames
    if os.path.exists(output_folder):
        delete_images_from_directory(output_folder)
    # Process all frames in the folder
    process_all_frames_cross(frames_folder, line_start, line_end, output_folder)
