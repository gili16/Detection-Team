import grpc
import allert_server_pb2
import allert_server_pb2_grpc
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Adjust your connection string as needed
db = client['AllertDB']  # Replace with your database name
def run(output):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = allert_server_pb2_grpc.AlertServiceStub(channel)

        # Read image from file
        with open('Server/img000002.jpg', 'rb') as f:  # Specify the correct path
            image_data = f.read()

        # # Example: Count Alert On
        response = stub.CountAllertOn(allert_server_pb2.CountAlertRequest(
            is_on=True,
            count=1,
            coordinate1_x=10,
            coordinate1_y=20,
            coordinate2_x=30,
            coordinate2_y=40,
            # image=image_data  # Send the image data as bytes
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write(response.message+'\n')
        with open('Server/img000001.jpg', 'rb') as f:  # Specify the correct path
            image_data = f.read()

        # # Example: Count Alert On
        response = stub.IsCrossAlertOn(allert_server_pb2.IsCrossAlertRequest(
            # is_on=True,
            # count=1,
            coordinate1_x=10,
            coordinate1_y=20,
            coordinate2_x=30,
            coordinate2_y=40,
            image=image_data  # Send the image data as bytes
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("IsCross ON"+'\n')

        # Example: Count Alert Off
        # response = stub.CountAllertOff(allert_server_pb2.CountAlertRequest(
        #     is_on=False
        # ))
        # with open(output, 'a') as file:
                # Write some text to the file
                # file.write("Count alert Off"+response.message)

        # Example: Send Image Alert On
        response = stub.SendImageAlertOn(allert_server_pb2.SendImageAlertRequest(
            is_on=True
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("Send image alert"+response.message+'\n')

        # # Example: Send Image Alert Off
        # response = stub.SendImageAlertOff(allert_server_pb2.SendImageAlertRequest(
        #     is_on=False
        # ))
        # with open(output, 'a') as file:
                # Write some text to the file
                # file.write("Send image alert"+response.message)

        # Example: Accident Alert On
        response = stub.AccidentAlertOn(allert_server_pb2.AccidentAlertRequest(
            is_on=True
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("accident alert"+response.message+'\n')

        # # Example: Accident Alert Off
        # response = stub.AccidentAlertOff(allert_server_pb2.AccidentAlertRequest(
        #     is_on=False
        # ))
        # with open(output, 'a') as file:
                # Write some text to the file
                # file.write("accident alert"+response.message)

        # Example: Odd Event Alert On
        response = stub.OddEventAlertOn(allert_server_pb2.OddEventAlertRequest(
            is_on=True
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("odd event alert"+response.message+'\n')

        # # Example: Odd Event Alert Off
        # response = stub.OddEventAlertOff(allert_server_pb2.OddEventAlertRequest(
        #     is_on=False
        # ))
        # with open(output, 'a') as file:
                # Write some text to the file
                # file.write("odd event alert"+response.message)

        # Example: Is Empty Alert On
        response = stub.IsEmptyAlertOn(allert_server_pb2.IsEmptyAlertRequest(
            is_on=True
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("is empty on alert"+response.message+'\n')
        

        # Example: Is Cross Alert On
        response = stub.IsCrossAlertOn(allert_server_pb2.IsCrossAlertRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("IsCross on alert"+response.message+'\n')
        # # Example: Is Cross Alert Off
        # response = stub.IsCrossAlertOff(allert_server_pb2.IsCrossAlertRequest(
        #     # is_on=False
        # ))
        # with open(output, 'a') as file:
                # Write some text to the file
                # file.write("IsCross alert"+response.message)
        response = stub.GetAccidentResult(allert_server_pb2.GetAccidentResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("accident result"+str(response.accident)+'\n')

        response = stub.GetCountResult(allert_server_pb2.GetCountResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("count result"+str(response.count)+'\n')
        response = stub.GetOddEventResult(allert_server_pb2.GetOddEventResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("odd event result"+str(response.odd_event)+'\n')
        response = stub.GetIsEmptyResult(allert_server_pb2.GetIsEmptyResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("is empty result"+str(response.is_empty)+'\n')
        response = stub.GetSendImageResult(allert_server_pb2.GetSendImageResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("send image result"+str(response.image)+'\n')
        response = stub.GetIsCrossResult(allert_server_pb2.GetIsCrossResultRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("is cross result"+str(response.is_cross)+'\n')
        response = stub.GetOnResults(allert_server_pb2.GetOnResultsRequest(
            
        ))
        with open(output, 'a') as file:
                # Write some text to the file
                file.write("on results"+str(response.results)+'\n')
if __name__ == '__main__':
    output='Server/output.txt'
    run(output)
