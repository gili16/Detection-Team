import time
import cv2
from pymongo import MongoClient
# import queue
from multiprocessing import Process, Queue
import subprocess
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
from Thread.create_fake_queue import read_images_from_directory
from Thread.functions import *
from Thread.utils import *
from Functions.detect_cross import delete_images_from_directory
from Registration.server import stereo_vehicle_pb2, stereo_vehicle_pb2_grpc
# from ..Server import allert_server_pb2, allert_server_pb2_grpc

import grpc

def process_image(image_queue,image_object, alert_service,is_thread_running,thread:Process,log_file):
    # print(alert_service)
    # return
    # print(os.path.join(frames_directory,filename))
    # cv2.imwrite(os.path.join(frames_directory,filename),image)
    image,frame_id=image_object
    """
    Process a single image based on active alerts.

    Args:
        image: The OpenCV image to process.
        alert_service: The alert service instance to call functions from.
    """
    # Check alerts and call corresponding functions
    if (alert_service['CountAllert']['IsOn'] or alert_service['OddEventAllert']['IsOn'] or alert_service['AccidentAllert']['IsOn']) and not is_thread_running:
        print("tracking")
        is_thread_running=True
        thread=Process(target=track,args=(image_queue,))
        thread.start()
    elif not alert_service['CountAllert']['IsOn'] and not alert_service['AccidentAllert']['IsOn'] and not alert_service['OddEventAllert']['IsOn'] and is_thread_running:
        thread.terminate()
        thread.join()
        thread=None
        is_thread_running=False
            
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
    original_image=image
    if alert_service['IsCrossAlert']['IsOn']:
        print("is cross")
        x1=alert_service['IsCrossAlert']['IsOn']['coordinate1'][0]
        y1=alert_service['IsCrossAlert']['IsOn']['coordinate1'][1]
        x2=alert_service['IsCrossAlert']['IsOn']['coordinate2'][0]
        y2=alert_service['IsCrossAlert']['IsOn']['coordinate2'][1]
        line_start=(x1,y1)
        line_end=(x2,y2)
        # first_frame=alert_service['IsCrossAlert']['IsOn']['image']
        image=draw_line(image,line_start,line_end)
        result=is_cross(line_start,line_end,image)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.SetIsCrossResult(allert_server_pb2.SetIsCrossResultRequest(
                is_cross=result
            ))
            with open(log_file, 'a') as file:
                # Write some text to the file
                file.write("SetIsCrossResultResonse::"+ response.message+str(result)+'\n')
    if alert_service['SendImageAllert']['IsOn']:
        print("send")
        result=send_image(image)
        original_result=send_image(original_image)

        is_success, buffer = cv2.imencode(".jpg", original_result) 
        if is_success:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                response = stub.SetSendImageResult(allert_server_pb2.SetSendImageResultRequest(
                    image=buffer.tobytes()
                ))
        # print("image: ",type(image))
        # print("result: ",type(result))
        is_success, buffer = cv2.imencode(".jpg", result) 
        if is_thread_running:
            # is_success, buffer = cv2.imencode(".jpg", result) 
            if is_success:
                print("buffer: ",type(buffer.tobytes()))
                image_queue.put((result,frame_id))

            else:
                print("saving image failed")
                image_queue.put(image_object)
        elif not is_thread_running and is_success:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = allert_server_pb2_grpc.AlertServiceStub(channel)
                response = stub.SetOverallImageResult(allert_server_pb2.SetOverallImageResultRequest(
                    image=buffer.tobytes()
                ))
                image_queue.put((result,frame_id))

    else:
        image_queue.put(image_object)

    return is_thread_running,thread

def process_queue( db,output_directory,log_file):
    """
    Continuously process images from the queue and activate alert functions based on the database.

    Args:
        image_queue (queue.Queue): A queue containing OpenCV images.
        db: The MongoDB database connection.
    """
   
    is_thread_running=False
    thread=None
    
    i=1
    image_queue=Queue()
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
                
                    
                    image_object = (frame,i)
                    # cv2.imwrite(os.path.join(output_directory,"image"+str(i)+".jpg"),image)
                    is_thread_running,thread=process_image(image_queue,image_object, alert_service,is_thread_running,thread,log_file)
                    print("analyzing frame: "+str(i))
                    i+=1
                    
                    time.sleep(3)  # Wait before checking again
                    
                        
            except grpc.RpcError as e:
                print(f"gRPC error: {e.code()} - {e.details()}")
                if thread:
                    thread.terminate()
                    thread.join()
                print("good night",sep="")
                time.sleep(1)
                print(".",sep="")
                time.sleep(1)
                print(".",sep="")
                time.sleep(1)
                print(".",sep="")
                time.sleep(1)

            except KeyboardInterrupt:
                if thread:
                    thread.terminate()
                    thread.join()
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
