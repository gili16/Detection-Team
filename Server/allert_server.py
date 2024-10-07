import grpc
from concurrent import futures
from pymongo import MongoClient
import allert_server_pb2
import allert_server_pb2_grpc
from allert_server_pb2 import Event
import time
import base64
class AlertService(allert_server_pb2_grpc.AlertServiceServicer):
    def __init__(self, db):
        self.db = db
        self.collections = {
            'CountAlert': db['CountAllert'],
            'SendImageAlert': db['SendImageAllert'],
            'AccidentAlert': db['AccidentAllert'],
            'OddEventAlert': db['OddEventAllert'],
            'IsEmptyAlert': db['IsEmptyAllert'],
            'IsCrossAlert': db['IsCrossAllert'],
            'Results': db['Results']
        }

    # Generic method for toggling alerts on/off
    def toggle_alert(self, alert_type, state, coordinates=None, image=None):
        collection = self.collections[alert_type]
        update_fields = {'IsOn': state}
        
        if coordinates:
            update_fields.update({
                'coordinate1': coordinates[0],
                'coordinate2': coordinates[1]
            })
        
        if image:
            update_fields['image'] = image
        
        collection.update_one(
            {},  # No filter, update the first document
            {'$set': update_fields,
             '$inc': {'Count': 1} if state else {}},  # Increment count only when turning on
            upsert=True
        )

    def toggle_result(self, field, value):
        self.collections['Results'].update_one(
            {}, 
            {'$set': {field: value}}, 
            upsert=True
        )

    # Alert methods can now use the generic toggle_alert method
    def CountAlertOn(self, request, context):
        self.toggle_alert('CountAlert', True, coordinates=((request.coordinate1_x, request.coordinate1_y), (request.coordinate2_x, request.coordinate2_y)))
        return allert_server_pb2.CountAlertResponse(message="Count Alert is ON")

    def CountAlertOff(self, request, context):
        self.toggle_alert('CountAlert', False)
        return allert_server_pb2.CountAlertResponse(message="Count Alert is OFF")

    def SendImageAlertOn(self, request, context):
        self.toggle_alert('SendImageAlert', True)
        return allert_server_pb2.SendImageAlertResponse(message="Send Image Alert is ON")

    def SendImageAlertOff(self, request, context):
        self.toggle_alert('SendImageAlert', False)
        return allert_server_pb2.SendImageAlertResponse(message="Send Image Alert is OFF")

    def AccidentAlertOn(self, request, context):
        self.toggle_alert('AccidentAlert', True)
        return allert_server_pb2.AccidentAlertResponse(message="Accident Alert is ON")

    def AccidentAlertOff(self, request, context):
        self.toggle_alert('AccidentAlert', False)
        return allert_server_pb2.AccidentAlertResponse(message="Accident Alert is OFF")

    def OddEventAlertOn(self, request, context):
        self.toggle_alert('OddEventAlert', True)
        return allert_server_pb2.OddEventAlertResponse(message="Odd Event Alert is ON")

    def OddEventAlertOff(self, request, context):
        self.toggle_alert('OddEventAlert', False)
        return allert_server_pb2.OddEventAlertResponse(message="Odd Event Alert is OFF")

    def IsEmptyAlertOn(self, request, context):
        self.toggle_alert('IsEmptyAlert', True)
        return allert_server_pb2.IsEmptyAlertResponse(message="Is Empty Alert is ON")

    def IsEmptyAlertOff(self, request, context):
        self.toggle_alert('IsEmptyAlert', False)
        return allert_server_pb2.IsEmptyAlertResponse(message="Is Empty Alert is OFF")

    def IsCrossAlertOn(self, request, context):
        self.toggle_alert('IsCrossAlert', True, coordinates=((request.coordinate1_x, request.coordinate1_y), (request.coordinate2_x, request.coordinate2_y)))
        return allert_server_pb2.IsCrossAlertResponse(message="IsCross Alert is ON")

    def IsCrossAlertOff(self, request, context):
        self.toggle_alert('IsCrossAlert', False)
        return allert_server_pb2.IsCrossAlertResponse(message="Is Cross Alert is OFF")

    # Results management using the toggle_result method
    def SetCountResult(self, request, context):
        self.toggle_result('Count', request.count)
        return allert_server_pb2.SetCountResultResponse(message="Count set")

    def SetAccidentResult(self, request, context):
        self.toggle_result('Accident', request.accident)
        return allert_server_pb2.SetAccidentResultResponse(message="Accident set")
    
    def SetSendImageResult(self, request, context):
        self.toggle_result('Image', request.image)
        return allert_server_pb2.SetSendImageResultResponse(message="send image set")

    def SetIsCrossResult(self, request, context):
        self.toggle_result('IsCross', request.is_cross)
        return allert_server_pb2.SetIsCrossResultResponse(message="is cross set")

    def SetIsEmptyResult(self, request, context):
        self.toggle_result('IsEmpty', request.is_empty)
        return allert_server_pb2.SetIsEmptyResultResponse(message="IsEmpty set")
    
    def SetOverallImageResult(self, request, context):
        self.toggle_result('OverallImage', request.image)
        return allert_server_pb2.SetOverallImageResultResponse(message="OverallImage set")
    
    def SetOddEventResult(self, request, context):
        new_event = {'date': request.odd_event.date, 'description': request.odd_event.description}
        odd_events = self.collections['Results'].find_one({})['OddEvent']
        updated_events = odd_events + [new_event] if odd_events else [new_event]
        self.toggle_result('OddEvent', updated_events)
        return allert_server_pb2.SetOddEventResultResponse(message="Odd Event set")

    # Define more result setters and getters as needed
     # Results getters
    def _get_result(self, key):
        # Find the result document
        result = self.collections['Results'].find_one({})
        
        # If no key is provided or key is an empty string, return the whole document
        if not key:
            return result
        
        # Otherwise, return the value associated with the specific key
        return result.get(key) if result else None

    def GetIsCrossResult(self, request, context):
        is_cross = self._get_result('IsCross')
        return allert_server_pb2.GetIsCrossResultResponse(is_cross=is_cross)

    def GetAccidentResult(self, request, context):
        accident = self._get_result('Accident')
        return allert_server_pb2.GetAccidentResultResponse(accident=accident)

    def GetCountResult(self, request, context):
        count = self._get_result('Count')
        return allert_server_pb2.GetCountResultResponse(count=count)

    def GetIsEmptyResult(self, request, context):
        is_empty = self._get_result('IsEmpty')
        return allert_server_pb2.GetIsEmptyResultResponse(is_empty=is_empty)

    def GetOddEventResult(self, request, context):
        odd_event = self._get_result('OddEvent')
        return allert_server_pb2.GetOddEventResultResponse(odd_event=odd_event[:5])

    def GetSendImageResult(self, request, context):
        image = self._get_result('Image')
        return allert_server_pb2.GetSendImageResultResponse(image=image)
    def GetOverallImageResult(self, request, context):
        image = self._get_result('OverAllImage')
        return allert_server_pb2.GetOverallImageResultResponse(image=image)
    # Decoding base64 string back to image bytes
    def decode_image(encoded_str):
        return base64.b64decode(encoded_str)
    # Handle multiple results
    def GetOnResults(self, request, context):
        # Create a response object
        need_overall_image=False
        response = allert_server_pb2.GetOnResultsResponse()
        all_results = self._get_result('')
        if self.collections['AccidentAlert'].find_one({'IsOn': True}):
            need_overall_image=True
            accident=all_results.get('Accident', 'None')
            if accident:
                response.accident=accident
            else:
                response.accident_empty=True
        if self.collections['CountAlert'].find_one({'IsOn': True}):
            need_overall_image=True
            count=all_results.get('Count', 'None')
            if count:
                response.count=count
            else:
                response.count_is_empty=True
        if self.collections['SendImageAlert'].find_one({'IsOn': True}) :
            image=all_results.get('Image', 'None')
            if image:
                response.image=image
            else:
                response.image_empty=True
        if self.collections['IsEmptyAlert'].find_one({'IsOn': True}):
            is_empty=all_results.get('IsEmpty', 'None')
            if is_empty:
                response.is_empty=is_empty
            else:
                response.is_empty_empty=True
        if self.collections['IsCrossAlert'].find_one({'IsOn': True}):
            need_overall_image=True
            is_cross=all_results.get('IsCross', 'None')
            if is_cross:
                response.is_cross=is_cross
            else:
                response.is_cross_empty=True
        if self.collections['OddEventAlert'].find_one({'IsOn': True}):
            need_overall_image=True
            odd_event=all_results.get('OddEvent', 'None')
            if odd_event:
                events=[Event(date=event['date'],description=event['description']) for event in odd_event]
                for event in events[:5]:
                    response.odd_event.append(event)
        if need_overall_image:
            overall_image=all_results.get('OverallImage','None')
            response.overall_image=overall_image
        else:
            response.overall_image_empty=True
        return response
    
    def NewDay(self, request, context):
        for alert_type in ['AccidentAlert', 'OddEventAlert', 'IsCrossAlert', 'CountAlert', 'IsEmptyAlert', 'SendImageAlert']:
            self.collections[alert_type].update_one(
                {}, 
                {'$set': {'IsOn': False, 'Count': 0}},
                upsert=True
            )
        
        self.collections['Results'].update_one(
            {}, 
            {'$set': {
                'Count': 0,
                'Accident': False,
                'IsEmpty': True,
                'IsCross': False,
                'Image': b'',
                'OddEvent': [],
                'OverallImage': b''
            }},
            upsert=True
        )
        return allert_server_pb2.NewDayResponse()

def start_server():
    client = MongoClient('mongodb://localhost:27017/')  # Change this to your MongoDB connection string
    db = client['AllertDB']  # Replace with your database name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    allert_server_pb2_grpc.add_AlertServiceServicer_to_server(AlertService(db), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    return server

def run_server(server):
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        kill_server(server)
def kill_server(server):
    server.stop(0)
if __name__ == '__main__':
    run_server(start_server())
