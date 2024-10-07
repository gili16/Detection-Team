import subprocess
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2, allert_server_pb2_grpc
import grpc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Functions.detect_cross import delete_images_from_directory
def run_process():
    subprocess.run(['python', 'Thread/secondary_thread.py'])  # Specify the script path

def run_server():
    subprocess.run(['python', 'Server/allert_server.py'])  # Specify the script path

if __name__ == "__main__":
    delete_images_from_directory('Thread/frames')
    try:
        thread2 = threading.Thread(target=run_server)
        thread2.start()
        thread = threading.Thread(target=run_process)
        thread.start()
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            response = stub.NewDay(allert_server_pb2.NewDayRequest(
                
            ))
        
        thread.join()  # Wait for the thread to finish
        
        thread2.join()  # Wait for the thread to finish
    except KeyboardInterrupt:
        thread._stop()
        thread2._stop()