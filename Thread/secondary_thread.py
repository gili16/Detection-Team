import time
import cv2
from pymongo import MongoClient
import queue


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
from Thread.create_fake_queue import read_images_from_directory
from Thread.functions import *
# from ..Server import allert_server_pb2, allert_server_pb2_grpc

import grpc

def process_image(image, alert_service):
    # print(alert_service)
    # return
    """
    Process a single image based on active alerts.

    Args:
        image: The OpenCV image to process.
        alert_service: The alert service instance to call functions from.
    """
    # Example: Here you could process the image if needed, e.g., display or analyze it
    # cv2.imshow('Processing Image', image)
    # cv2.waitKey(1)  # Display for a short period

    # Check alerts and call corresponding functions
    if alert_service['CountAllert']['IsOn']:
        # print((alert_service['SendImageAllert']['IsOn'])['Count'])
        # print('count')
        # print(alert_service['CountAllert'])
        x1=alert_service['CountAllert']['IsOn']['coordinate1'][0]
        y1=alert_service['CountAllert']['IsOn']['coordinate1'][1]
        x2=alert_service['CountAllert']['IsOn']['coordinate2'][0]
        y2=alert_service['CountAllert']['IsOn']['coordinate2'][1]
        result=count(alert_service['CountAllert']['IsOn']['image'],x1,y1,x2,y2)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetCountResult(allert_server_pb2.SetCountResultRequest(
                count=result
            ))
            print("SetCountResultResonse:", response.message)
    
    if alert_service['SendImageAllert']['IsOn']:
        result=send_image()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetSendImageResult(allert_server_pb2.SetSendImageResultRequest(
                image=result
            ))
            print("SetSendImageResultResonse:", response.message)
    
    if alert_service['AccidentAllert']['IsOn']:
        result=accident()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetAccidentResult(allert_server_pb2.SetAccidentResultRequest(
                accident=result
            ))
            print("SetAccidentResultResonse:", response.message)
    
    if alert_service['OddEventAllert']['IsOn']:
        result=odd_event()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetOddEventResult(allert_server_pb2.SetOddEventResultRequest(
                odd_event=result
            ))
            print("SetCountResultResonse:", response.message)
    
    if alert_service['IsEmptyAlert']['IsOn']:
        result=is_empty()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetIsEmptyResult(allert_server_pb2.SetIsEmptyResultRequest(
                is_empty=result
            ))
            print("SetIsEmptyResultResonse:", response.message)

def process_queue(image_queue, db):
    """
    Continuously process images from the queue and activate alert functions based on the database.

    Args:
        image_queue (queue.Queue): A queue containing OpenCV images.
        db: The MongoDB database connection.
    """
    alert_service = {
        'CountAllert': {
            'IsOn': db['CountAllert'].find_one({'IsOn': True}),
            'function': lambda: print("Count Alert Activated")
        },
        'SendImageAllert': {
            'IsOn': db['SendImageAllert'].find_one({'IsOn': True}),
            'function': lambda: print("Send Image Alert Activated")
        },
        'AccidentAllert': {
            'IsOn': db['AccidentAllert'].find_one({'IsOn': True}),
            'function': lambda: print("Accident Alert Activated")
        },
        'OddEventAllert': {
            'IsOn': db['OddEventAllert'].find_one({'IsOn': True}),
            'function': lambda: print("Odd Event Alert Activated")
        },
        'IsEmptyAlert': {
            'IsOn': db['IsEmptyAllert'].find_one({'IsOn': True}),
            'function': lambda: print("Is Empty Alert Activated")
        }
    }
    i=0
    while True and i<10:
        if not image_queue.empty():
            image = image_queue.get()  # Get the next image from the queue
            process_image(image, alert_service)
            i+=1
        else:
            print("Queue is empty, waiting for images...")
            time.sleep(1)  # Wait before checking again

# Example usage
if __name__ == "__main__":
    directory="../../to_git/detection-team/training/DATA/UAV-benchmark-M/M0202"
    client = MongoClient('mongodb://localhost:27017/')  # MongoDB connection
    db = client['AllertDB']  # Replace with your database name
    image_queue = queue.Queue()  # Assuming this queue is populated elsewhere
    image_queue=read_images_from_directory(directory)
    # Start processing the queue
    process_queue(image_queue, db)
