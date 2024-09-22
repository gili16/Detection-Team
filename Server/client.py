import grpc
import allert_server_pb2
import allert_server_pb2_grpc
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Adjust your connection string as needed
db = client['AllertDB']  # Replace with your database name
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = allert_server_pb2_grpc.AlertServiceStub(channel)

        # Read image from file
        # with open('img000002.jpg', 'rb') as f:  # Specify the correct path
        #     image_data = f.read()

        # # Example: Count Alert On
        # response = stub.CountAllertOn(allert_server_pb2.CountAlertRequest(
        #     is_on=True,
        #     count=1,
        #     coordinate1_x=10,
        #     coordinate1_y=20,
        #     coordinate2_x=30,
        #     coordinate2_y=40,
        #     image=image_data  # Send the image data as bytes
        # ))
        # print(response.message)


        # Example: Count Alert Off
        # response = stub.CountAllertOff(allert_server_pb2.CountAlertRequest(
        #     is_on=False
        # ))
        # print("CountAlertOff:", response.message)

        # Example: Send Image Alert On
        # response = stub.SendImageAlertOn(allert_server_pb2.SendImageAlertRequest(
        #     is_on=True
        # ))
        # print("SendImageAlertOn:", response.message)

        # # Example: Send Image Alert Off
        # response = stub.SendImageAlertOff(allert_server_pb2.SendImageAlertRequest(
        #     is_on=False
        # ))
        # print("SendImageAlertOff:", response.message)

        # Example: Accident Alert On
        # response = stub.AccidentAlertOn(allert_server_pb2.AccidentAlertRequest(
        #     is_on=True
        # ))
        # print("AccidentAlertOn:", response.message)

        # # Example: Accident Alert Off
        # response = stub.AccidentAlertOff(allert_server_pb2.AccidentAlertRequest(
        #     is_on=False
        # ))
        # print("AccidentAlertOff:", response.message)

        # Example: Odd Event Alert On
        # response = stub.OddEventAlertOn(allert_server_pb2.OddEventAlertRequest(
        #     is_on=True
        # ))
        # print("OddEventAlertOn:", response.message)

        # # Example: Odd Event Alert Off
        # response = stub.OddEventAlertOff(allert_server_pb2.OddEventAlertRequest(
        #     is_on=False
        # ))
        # print("OddEventAlertOff:", response.message)

        # Example: Is Empty Alert On
        # response = stub.IsEmptyAlertOn(allert_server_pb2.IsEmptyAlertRequest(
        #     is_on=True
        # ))
        # print("IsEmptyAlertOn:", response.message)

        # # Example: Is Empty Alert Off
        # response = stub.IsEmptyAlertOff(allert_server_pb2.IsEmptyAlertRequest(
        #     is_on=False
        # ))
        # print("IsEmptyAlertOff:", response.message)
        response = stub.GetAccidentResult(allert_server_pb2.GetAccidentResultRequest(
            
        ))
        print("accident result:", response.accident)

        response = stub.GetCountResult(allert_server_pb2.GetCountResultRequest(
            
        ))
        print("count result:", response.count)
        response = stub.GetOddEventResult(allert_server_pb2.GetOddEventResultRequest(
            
        ))
        print("odd event result:", response.odd_event)
        response = stub.GetIsEmptyResult(allert_server_pb2.GetIsEmptyResultRequest(
            
        ))
        print("is empty result:", response.is_empty)
        response = stub.GetSendImageResult(allert_server_pb2.GetSendImageResultRequest(
            
        ))
        print("image result:", response.image)
if __name__ == '__main__':
    run()
