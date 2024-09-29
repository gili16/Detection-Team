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
        self.collection_is_cross_alert = db['IsCrossAllert']
        self.collection_results=db['Results']
    def CountAlertOn(self, request, context):
        # image_data = request.image  # This will be bytes
        # print(self.collection_count_alert.find_one({'IsOn':True}))
        obj=self.collection_count_alert.find_one({'IsOn':True})
        if not obj :
            # Store image data directly in MongoDB
            self.collection_count_alert.update_one(
                {},
                {
                    '$set': {
                        'IsOn': True,
                        'coordinate1': (request.coordinate1_x, request.coordinate1_y),
                        'coordinate2': (request.coordinate2_x, request.coordinate2_y),
                        
                    },                
                    '$inc': {
                        'Count': 1  # Increment Count by 1
                    }
                },
                upsert=True
            )
        return allert_server_pb2.CountAlertResponse(message="Count Alert is ON")

    def CountAlertOff(self, request, context):
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
    def IsCrossAlertOn(self, request, context):
        image_data = request.image  # This will be bytes
        # print(self.collection_is_cross_alert.find_one({'IsOn':True}))
        obj=self.collection_is_cross_alert.find_one({'IsOn':True})
        if not obj or obj and obj['image']!=image_data:
            # Store image data directly in MongoDB
            self.collection_is_cross_alert.update_one(
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
        return allert_server_pb2.IsCrossAlertResponse(message="IsCross Alert is ON")

    def IsCrossAlertOff(self, request, context):
        print("off")
        self.collection_is_cross_alert.update_one(
            {},  # No filter
            {'$set': {'IsOn': False}}
        )
        return allert_server_pb2.IsEmptyAlertResponse(message="Is Cross Alert is OFF")
    def SetCountResult(self, request, context):
        print(request.count)
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
        new_event={'date':request.odd_event.date,'description':request.odd_event.description}
        odd_events=self.collection_results.find_one({})['OddEvent']
        self.collection_results.update_one(
            {},
            {
                '$set':{'OddEvent': odd_events + [new_event] if odd_events else [new_event]}
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
    def SetIsCrossResult(self, request, context):
        self.collection_results.update_one(
            {},
            {
                '$set':{'IsCross':request.is_cross}
            },
            upsert=True
        )
        return allert_server_pb2.SetSendImageResultResponse(message="IsCross set")
    def GetIsCrossResult(self, request, context):
        is_cross=self.collection_results.find_one({})['IsCross']
        return allert_server_pb2.GetIsCrossResultResponse(is_cross=is_cross)
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
    def GetOnResults(self, request, context):
        results=[]
        all_results=self.collection_results.find_one({})
        if self.collection_accident_alert.find_one({'IsOn':True}):
            results+=['accident '+str(all_results['Accident'])]
        else:
            results+=['None']
        if self.collection_count_alert.find_one({'IsOn':True}):
            results+=['count objects'+str(all_results['Count'])]
        else:
            results+=['None']
        if self.collection_send_image_alert.find_one({'IsOn':True}):
            results+=['image '+str(all_results['Image'])]
        else:
            results+=['None']
        if self.collection_is_empty_alert.find_one({'IsOn':True}):
            results+=['is_empty '+str(all_results['IsEmpty'])]
        else:
            results+=['None']
        if self.collection_is_cross_alert.find_one({'IsOn':True}):
            results+=['is_cross '+str(all_results['IsCross'])]
        else:
            results+=['None']
        if self.collection_odd_event_alert.find_one({'IsOn':True}):
            odd_events="oddEvents: "
            for event in self.collection_results['OddEvent']:
                odd_events+=event['date']+event['description']+" "
            results+=[odd_events]
        else:
            results+=['None']
        return allert_server_pb2.GetOnResultsResponse(
            results=results
        )
    def NewDay(self, request, context):
        self.collection_accident_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0
                    }          
            },
            upsert=True
        )
        self.collection_odd_event_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0
                    }          
            },
            upsert=True
        )
        self.collection_is_cross_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0,
                        'coordinate1':[],
                        'coordinate2':[],
                        'image':b''
                    }          
            },
            upsert=True
        )
        self.collection_count_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0,
                        'coordinate1':[],
                        'coordinate2':[]
                    }          
            },
            upsert=True
        )
        self.collection_is_empty_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0
                    }          
            },
            upsert=True
        )
        self.collection_send_image_alert.update_one(
            {},
            {            
                '$set':{'IsOn':False,
                        'Count':0
                    }          
            },
            upsert=True
        )
        self.collection_results.update_one(
            {},
            {            
                '$set':{
                    'Count':0,
                    'Accident':False,
                    'IsEmpty':True,
                    'IsCross':False,
                    'Image':b'',
                    'OddEvent':[]
                    }          
            },
            upsert=True
        )
        return allert_server_pb2.NewDayResponse()
def serve():
    client = MongoClient('mongodb://localhost:27017/')  # Change this to your MongoDB connection string
    db = client['AllertDB']  # Replace with your database name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    allert_server_pb2_grpc.add_AlertServiceServicer_to_server(AlertService(db), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    with open('Server/output.txt', 'a') as file:
            # Write some text to the file
            file.write("server is running")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
