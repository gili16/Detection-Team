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
        self.collection_results=db['Results']
    def CountAllertOn(self, request, context):
        image_data = request.image  # This will be bytes
        print(self.collection_count_alert.find_one({'IsOn':True}))
        obj=self.collection_count_alert.find_one({'IsOn':True})
        if not obj or obj and obj['image']!=image_data:
            # Store image data directly in MongoDB
            self.collection_count_alert.update_one(
                {},
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
        if not self.collection_send_image_alert.find_one({'IsOn':True}):
            self.collection_send_image_alert.update_one(
                {},
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
        if not self.collection_accident_alert.find_one({'IsOn':True}):
            self.collection_accident_alert.update_one(
                {},
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
        if not self.collection_odd_event_alert.find_one({'IsOn':True}):
            self.collection_odd_event_alert.update_one(
                {},
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
        if not self.collection_is_empty_alert.find_one({'IsOn':True}):
            self.collection_is_empty_alert.update_one(
                {},
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
    def SetCountResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'Count':request.count}
            },
            upsert=True
        )
        return allert_server_pb2.SetCountResultResponse(message="Count set")
    def SetAccidentResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'Accident':request.accident}
            },
            upsert=True
        )
        return allert_server_pb2.SetAccidentResultResponse(message="Accident set")
    def SetIsEmptyResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'IsEmpty':request.is_empty}
            },
            upsert=True
        )
        return allert_server_pb2.SetIsEmptyResultResponse(message="IsEmpty set")
    def SetOddEventResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'OddEvent':request.odd_event}
            },
            upsert=True
        )
        return allert_server_pb2.SetOddEventResultResponse(message="Odd Event set")
    def SetSendImageResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'Image':request.image}
            },
            upsert=True
        )
        return allert_server_pb2.SetSendImageResultResponse(message="Image set")
    def GetAccidentResult(self, request, context):
        accident=self.collection_results.find_one({})['Accident']
        return allert_server_pb2.GetAccidentResultResponse(accident=accident)
    def GetCountResult(self, request, context):
        count=self.collection_results.find_one({})['Count']
        return allert_server_pb2.GetCountResultResponse(count=count)
    def GetIsEmptyResult(self, request, context):
        is_empty=self.collection_results.find_one({})['IsEmpty']
        return allert_server_pb2.GetIsEmptyResultResponse(is_empty=is_empty)
    def GetOddEventResult(self, request, context):
        odd_event=self.collection_results.find_one({})['OddEvent']
        return allert_server_pb2.GetOddEventResultResponse(odd_event=odd_event)
    def GetSendImageResult(self, request, context):
        image=self.collection_results.find_one({})['Image']
        return allert_server_pb2.GetSendImageResultResponse(image=image)
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
