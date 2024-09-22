import os
import queue
from PIL import Image
import cv2

def is_image_file(filename):
    """
    Check if the file is a valid image based on its extension.
    
    Args:
        filename (str): The name of the file.
        
    Returns:
        bool: True if the file is an image, False otherwise.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    _, ext = os.path.splitext(filename)
    return ext.lower() in image_extensions

def read_images_from_directory(directory_path):
    """
    Reads images from the specified directory and adds their file paths to a queue.

    Args:
        directory_path (str): The path to the directory containing images.

    Returns:
        queue.Queue: A queue containing paths to the images.
    """
    # Create a FIFO queue
    image_queue = queue.Queue()

    # List of image file extensions to look for
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    for filename in os.listdir(directory_path):
        if is_image_file(filename):
            # Create the full file path
            file_path = os.path.join(directory_path, filename)
            # Read the image using OpenCV
            image = cv2.imread(file_path)
            if image is not None:
                # Put only the image in the queue
                image_queue.put(image)
                print(f"Added image to queue: {filename}")

    return image_queue

def show_images_from_queue(image_queue):
    """
    Displays images from the queue.

    Args:
        image_queue (queue.Queue): A queue containing paths to the images.
    """
    while not image_queue.empty():
        image_path = image_queue.get()
        try:
            # Open and show the image
            with Image.open(image_path) as img:
                img.show()  # This will open the image in the default image viewer
                print(f"Displayed image: {image_path}")
        except Exception as e:
            print(f"Error displaying image {image_path}: {e}")

# Example usage
if __name__ == "__main__":
    directory = "../../to_git/detection-team/training/DATA/UAV-benchmark-M/M0202"  # Change this to your directory path
    image_queue = read_images_from_directory(directory)

    # Example of processing images from the queue
    while not image_queue.empty():
        image_path = image_queue.get()
        print(f"Processing image: {image_path}")
        # Add your image processing code here

    show_images_from_queue(image_queue)
