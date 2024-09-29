from datetime import datetime
from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grpc
from Server import allert_server_pb2,allert_server_pb2_grpc
from Server.allert_server_pb2 import Event
# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['AllertDB']  # Database name
collection = db['Results']  # Collection name

class UnusualEvent:
    """Class representing an unusual event."""
    def __init__(self, event, image):
        self.event = event
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.image = image

    def save_to_db(self):
        """Save the event to the MongoDB database."""
        event_data = Event(
            date= str(self.time),
            description= self.event
        )
        print("hello")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = allert_server_pb2_grpc.AlertServiceStub(channel)
            
            response = stub.SetOddEventResult(allert_server_pb2.SetOddEventResultRequest(
                odd_event=event_data
            ))
        print(f"Event saved to MongoDB: {event_data}")
