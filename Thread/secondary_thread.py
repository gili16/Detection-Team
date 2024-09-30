import time
import cv2
from pymongo import MongoClient
import queue
from multiprocessing import Process
import subprocess
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
from Thread.create_fake_queue import read_images_from_directory
from Thread.functions import *
from Functions.detect_cross import delete_images_from_directory
from Registration.server import stereo_vehicle_pb2, stereo_vehicle_pb2_grpc
# from ..Server import allert_server_pb2, allert_server_pb2_grpc

import grpc

def process_image(image, alert_service,frames_directory,filename,is_thread_running,thread:Process,log_file,is_thread_odd_running, thread_odd:Process):
    # print(alert_service)
    # return
    # print(os.path.join(frames_directory,filename))
    cv2.imwrite(os.path.join(frames_directory,filename),image)
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
    if alert_service['CountAllert']['IsOn'] and not is_thread_running:
        print("count")
        is_thread_running=True
        x1=alert_service['CountAllert']['IsOn']['coordinate1'][0]
        y1=alert_service['CountAllert']['IsOn']['coordinate1'][1]
        x2=alert_service['CountAllert']['IsOn']['coordinate2'][0]
        y2=alert_service['CountAllert']['IsOn']['coordinate2'][1]        
        thread=Process(target=count,args=(x1,y1,x2,y2,frames_directory))
        thread.start()
    elif not alert_service['CountAllert']['IsOn'] and is_thread_running:
        thread.terminate()
        thread.join()
        thread=None
        is_thread_running=False
        
    
    if alert_service['SendImageAllert']['IsOn']:
        print("send")
        result=send_image(image)
        is_success, buffer = cv2.imencode(".jpg", result) 
        if is_success:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                response = stub.SetSendImageResult(allert_server_pb2.SetSendImageResultRequest(
                    image=buffer.tobytes()
                ))
                with open(log_file, 'a') as file:
                    # Write some text to the file

                    file.write("SetSendImageResultResonse:"+ response.message+'\n')

        else:
            print("saving image failed")
    
    if alert_service['AccidentAllert']['IsOn']:
        print("accident")
        result=accident()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetAccidentResult(allert_server_pb2.SetAccidentResultRequest(
                accident=result
            ))
            with open(log_file, 'a') as file:
                # Write some text to the file
                file.write("SetAccidentResultResonse::"+ response.message+'\n')
    
    if alert_service['OddEventAllert']['IsOn']: 
        print("odd event")
        if not is_thread_odd_running:
            thread_odd=Process(target=odd_event,args=(frames_directory,'Functions/output'))
            thread_odd.start()
            is_thread_odd_running=True
    else:
        if not alert_service['OddEventAllert']['IsOn'] and is_thread_odd_running:
            thread_odd.terminate()
            thread_odd.join()
            thread_odd=None
            is_thread_odd_running=False
    
    if alert_service['IsEmptyAlert']['IsOn']:
        print("is empty")
        result=is_empty(image)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetIsEmptyResult(allert_server_pb2.SetIsEmptyResultRequest(
                is_empty=result
            ))
            with open(log_file, 'a') as file:
                # Write some text to the file
                file.write("SetIsEmptyResultResonse::"+ response.message+'\n')

    if alert_service['IsCrossAlert']['IsOn']:
        print("is cross")
        x1=alert_service['IsCrossAlert']['IsOn']['coordinate1'][0]
        y1=alert_service['IsCrossAlert']['IsOn']['coordinate1'][1]
        x2=alert_service['IsCrossAlert']['IsOn']['coordinate2'][0]
        y2=alert_service['IsCrossAlert']['IsOn']['coordinate2'][1]
        line_start=(x1,y1)
        line_end=(x2,y2)
        # first_frame=alert_service['IsCrossAlert']['IsOn']['image']
        
        result=is_cross(line_start,line_end,image,filename)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetIsCrossResult(allert_server_pb2.SetIsCrossResultRequest(
                is_cross=result
            ))
            with open(log_file, 'a') as file:
                # Write some text to the file
                file.write("SetIsCrossResultResonse::"+ response.message+str(result)+'\n')
    return is_thread_running,thread,is_thread_odd_running,thread_odd

def process_queue( db,output_directory,log_file):
    """
    Continuously process images from the queue and activate alert functions based on the database.

    Args:
        image_queue (queue.Queue): A queue containing OpenCV images.
        db: The MongoDB database connection.
    """
   
    is_thread_running=False
    thread=None
    is_thread_odd_running=False
    thread_odd=None
    i=0
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = stereo_vehicle_pb2_grpc.ImageProcessingStub(channel)
        while True :
            try:
                frame_request = stereo_vehicle_pb2.Empty()
                response = stub.GetStabilizedFrame(frame_request)

                if response.frame:
                    nparr = np.frombuffer(response.frame, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
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
                        },
                        'IsCrossAlert': {
                            'IsOn': db['IsCrossAllert'].find_one({'IsOn': True}),
                            'function': lambda: print("Is Cross Alert Activated")
                        }

                    }
                
                    
                    image = frame
                    cv2.imwrite(os.path.join(output_directory,"image"+str(i)+".jpg"),image)
                    is_thread_running,thread,is_thread_odd_running,thread_odd=process_image(image, alert_service,output_directory,os.path.join(output_directory,"image"+str(i)),is_thread_running,thread,log_file,is_thread_odd_running,thread_odd)
                    i+=1
                    print("analyzing frame: "+str(i))
                    time.sleep(3)  # Wait before checking again
                    
                        
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                if thread:
                    thread.terminate()
                    thread.join()
                if thread_odd:
                    thread_odd.terminate()
                    thread_odd.join()
                break

# Example usage
if __name__ == "__main__":
    directory="../../to_git/detection-team/training/DATA/UAV-benchmark-M/M0202"
    client = MongoClient('mongodb://localhost:27017/')  # MongoDB connection
    db = client['AllertDB']  # Replace with your database name
    output_directory="Thread\\frames"
    log_file=('Thread\output.txt')

    # Start processing the queue
    with open(log_file, 'a') as file:
            # Write some text to the file
            file.write("\nsecondary thread is running:")
    process_queue( db,output_directory,log_file)
    with open(log_file, 'a') as file:
            # Write some text to the file
            file.write("\nsecondary thread finished:")
