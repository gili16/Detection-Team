import grpc
from concurrent import futures
from pymongo import MongoClient
import allert_server_pb2
import allert_server_pb2_grpc
import time  # Import time module
from pymongo import MongoClient

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')  # Adjust your connection string as needed
# db = client['AllertDB']  # Replace with your database name
class AlertService(allert_server_pb2_grpc.AlertServiceServicer):
    def __init__(self, db):
        self.collection_count_alert = db['CountAllert']
        self.collection_send_image_alert = db['SendImageAllert']
        self.collection_accident_alert = db['AccidentAllert']
        self.collection_odd_event_alert = db['OddEventAllert']
        self.collection_is_empty_alert = db['IsEmptyAllert']

    def CountAllertOn(self, request, context):
        image_data = request.image  # This will be bytes

        # Store image data directly in MongoDB
        self.collection_count_alert.update_one(
            {'IsOn': True},
            {
                '$set': {
                    'IsOn': True,
                    'coordinate1': (request.coordinate1_x, request.coordinate1_y),
                    'coordinate2': (request.coordinate2_x, request.coordinate2_y),
                    'image': image_data
                },                
                '$inc': {
                    'Count': 1  # Increment Count by 1
                }
            },
            upsert=True
        )
        return allert_server_pb2.CountAlertResponse(message="Count Alert is ON")

    def CountAllertOff(self, request, context):
        self.collection_count_alert.update_one(
            {},  # No filter, update the first document
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.CountAlertResponse(message="Count Alert is OFF")

    def SendImageAlertOn(self, request, context):
        self.collection_send_image_alert.update_one(
            {'IsOn': True},
            {
                '$set': {'IsOn': True},
                '$inc': {
                    'Count': 1  # Increment Count by 1
                }
            },
            upsert=True
        )
        return allert_server_pb2.SendImageAlertResponse(message="Send Image Alert is ON")

    def SendImageAlertOff(self, request, context):
        self.collection_send_image_alert.update_one(
            {},  # No filter
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.SendImageAlertResponse(message="Send Image Alert is OFF")

    def AccidentAlertOn(self, request, context):
        self.collection_accident_alert.update_one(
            {'IsOn': True},
            {
                '$set': {'IsOn': True},
                '$inc': {
                    'Count': 1  # Increment Count by 1
                }
            },
            upsert=True
        )
        return allert_server_pb2.AccidentAlertResponse(message="Accident Alert is ON")

    def AccidentAlertOff(self, request, context):
        self.collection_accident_alert.update_one(
            {},  # No filter
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.AccidentAlertResponse(message="Accident Alert is OFF")

    def OddEventAlertOn(self, request, context):
        self.collection_odd_event_alert.update_one(
            {'IsOn': True},
            {
                '$set': {'IsOn': True},
                '$inc': {
                    'Count': 1  # Increment Count by 1
                }
            },
            upsert=True
        )
        return allert_server_pb2.OddEventAlertResponse(message="Odd Event Alert is ON")

    def OddEventAlertOff(self, request, context):
        self.collection_odd_event_alert.update_one(
            {},  # No filter
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.OddEventAlertResponse(message="Odd Event Alert is OFF")

    def IsEmptyAlertOn(self, request, context):
        self.collection_is_empty_alert.update_one(
            {'IsOn': True},
            {
                '$set': {'IsOn': True},  
                '$inc': {
                    'Count': 1  # Increment Count by 1
                }
            },
            upsert=True
        )
        return allert_server_pb2.IsEmptyAlertResponse(message="Is Empty Alert is ON")

    def IsEmptyAlertOff(self, request, context):
        self.collection_is_empty_alert.update_one(
            {},  # No filter
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.IsEmptyAlertResponse(message="Is Empty Alert is OFF")

def serve():
    client = MongoClient('mongodb://localhost:27017/')  # Change this to your MongoDB connection string
    db = client['AllertDB']  # Replace with your database name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    allert_server_pb2_grpc.add_AlertServiceServicer_to_server(AlertService(db), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
