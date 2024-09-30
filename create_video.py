import cv2
import os

def create_video_from_frames(frame_folder, output_video_path, fps=30):
    # Get the list of image files from the folder
    images = [img for img in os.listdir(frame_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()  # Ensure images are sorted in sequence

    # Read the first image to get the dimensions (width, height)
    frame = cv2.imread(os.path.join(frame_folder, images[0]))
    height, width, _ = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for .mp4, or 'XVID' for .avi
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through the images and write them to the video file
    for image in images:
        img_path = os.path.join(frame_folder, image)
        frame = cv2.imread(img_path)
        video_writer.write(frame)  # Write the frame to the video

    # Release the VideoWriter object
    video_writer.release()
    print(f"Video saved at {output_video_path}")

# Example usage
frame_folder = '../../to_git/detection-team/training/DATA/UAV-benchmark-M/M0202'
output_video_path = 'Video/output_video.mp4'
fps = 30  # Set your desired frame rate (frames per second)
create_video_from_frames(frame_folder, output_video_path, fps)
