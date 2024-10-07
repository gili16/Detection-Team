import os
import cv2
import numpy as np
import pygame
# from object_tracking import track_frames

# Initialize pygame mixer for sound playback
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
from datetime import datetime
# Define thresholds for unusual events
SPEED_THRESHOLD = 8
GATHERING_THRESHOLD = 1
PARKING_THRESHOLD = 0.01
CLOSE_DISTANCE_THRESHOLD = 400

def generate_beep_sound(duration=1.0, frequency=440):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)

    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    stereo_wave = np.column_stack((wave, wave))

    sound_array = np.int16(stereo_wave * 32767)
    sound = pygame.sndarray.make_sound(sound_array)
    return sound

def play_alert_sound():
    """ Play an alert sound. """
    try:
        pygame.mixer.init()  # Ensure Pygame mixer is initialized
        beep = generate_beep_sound(duration=1.0, frequency=440)  # Use the generated sound
        beep.play()  # Play the sound
        pygame.time.wait(500)  # Wait for 0.5 seconds to ensure the sound finishes
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def detect_unusual_events(tracked_objects):
    unusual_events = []
    people_count = sum(1 for obj in tracked_objects if obj['Label'] == 'person')

    # Detect speeding and parked cars
    for obj in tracked_objects:
        if obj['Label'] != 'person':  # Handle non-person objects
            bboxes = obj['Bounding Boxes']
            for i in range(1, len(bboxes)):
                prev_bbox = bboxes[i-1]['bbox']
                current_bbox = bboxes[i]['bbox']
                
                prev_center = ((prev_bbox[0] + prev_bbox[2]) // 2, (prev_bbox[1] + prev_bbox[3]) // 2)
                current_center = ((current_bbox[0] + current_bbox[2]) // 2, (current_bbox[1] + current_bbox[3]) // 2)
                
                distance = np.sqrt((current_center[0] - prev_center[0]) ** 2 + (current_center[1] - prev_center[1]) ** 2)
                speed =distance
                if speed > SPEED_THRESHOLD:
                    unusual_events.append({
                        'label': obj['Label'],
                        'bbox': current_bbox,
                        'speed': speed,
                        'event': 'Speeding',
                        'time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    # play_alert_sound()
                    break
                if speed < PARKING_THRESHOLD:
                    unusual_events.append({
                        'label': obj['Label'],
                        'bbox': current_bbox,
                        'speed': speed,
                        'event': 'Car Parked',
                        'time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    # play_alert_sound()
                    break
    # Detect gathering of people
    if people_count > GATHERING_THRESHOLD:
        people_positions = [obj['Bounding Boxes'] for obj in tracked_objects if obj['Label'] == 'person']
        i=0
        for i, person_1 in enumerate(people_positions):
            j=0
            for j, person_2 in enumerate(people_positions):
                if i != j:
                    dist = np.sqrt((person_1[0]['bbox'][0] - person_2[0]['bbox'][0]) ** 2 + (person_1[0]['bbox'][1] - person_2[0]['bbox'][1]) ** 2)
                    if dist < CLOSE_DISTANCE_THRESHOLD:
                        unusual_events.append({
                            'label': 'people',
                            'bbox': None,
                            'speed': 0,
                            'event': 'Gathering of People',
                            'time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        # play_alert_sound()
                        break
            #     if j<len(people_positions):
            #         break
            # if i<len(people_positions):
            #     break

    return unusual_events

# def process_all_frames(frames_folder, output_folder):
    """
    Process all frames for unusual event detection.
    """
    # Track objects and get their bounding boxes
    # tracked_objects, start, end = track_frames(frames_folder)

    # # Annotate the frames with unusual events
    # frame_files = sorted(os.listdir(frames_folder))
    # for frame_idx, frame_file in enumerate(frame_files):
    #     frame_path = os.path.join(frames_folder, frame_file)
    #     frame = cv2.imread(frame_path)
        
    #     if frame is None:
    #         print(f"Failed to read frame: {frame_path}, skipping.")
    #         continue

        # Detect unusual events for the current frame
    # unusual_events = detect_unusual_events(tracked_objects)

    # Annotate only the current frame with detected events
    # if unusual_events:
    #     for event in unusual_events:
    #         event_type = event['event']

    #         if event_type == 'Gathering of People':
    #             for obj in tracked_objects:
    #                 if obj['Label'] == 'person':
    #                     for bbox_info in obj['Bounding Boxes']:
    #                         x1, y1, w, h = bbox_info['bbox']
    #                         cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 2)
    #                         cv2.putText(frame, 'Gathering', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    #             break  # Break after marking gathering of people

    #         else:
    #             # Draw only the bbox related to the unusual event
    #             if event['bbox'] is not None:
    #                 x1, y1, w, h = event['bbox']
    #                 label = event['label']
    #                 speed = event['speed']
    #                 cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
    #                 cv2.putText(frame, f'{label} {event_type} ({speed:.2f})', (x1, y1 - 10),
    #                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    #     # Save the annotated frame
    #     output_path = os.path.join(output_folder, frame_file)
    #     cv2.imwrite(output_path, frame)
    #     print(f'Saved frame: {output_path}')
    # else:
    #     print('No unusual events detected in this frame.')
    # return unusual_events

# Example usage
# if __name__=='__main__':
#     frames_folder = './input/M0202'  # Path to your input frames
#     output_folder = './output/unusual_event'  # Path to save output frames
#     unusual_events=process_all_frames(frames_folder, output_folder)
#     speed=park=gather=0
#     for i in unusual_events:
#         if i['event']=='Speeding':
#             speed+=1
#         elif i['event']=='Car Parked':
#             park+=1
#         elif i['event']=='Gathering of People':
#             gather+=1
#     print(len(unusual_events),"speed:",speed," park:",park," gather:",gather)
