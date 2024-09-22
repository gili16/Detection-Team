# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server import allert_server_pb2 as allert__server__pb2
# import allert_server_pb2 as allert__server__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in allert_server_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AlertServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CountAllertOn = channel.unary_unary(
                '/alerts.AlertService/CountAllertOn',
                request_serializer=allert__server__pb2.CountAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.CountAlertResponse.FromString,
                _registered_method=True)
        self.CountAllertOff = channel.unary_unary(
                '/alerts.AlertService/CountAllertOff',
                request_serializer=allert__server__pb2.CountAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.CountAlertResponse.FromString,
                _registered_method=True)
        self.SendImageAlertOn = channel.unary_unary(
                '/alerts.AlertService/SendImageAlertOn',
                request_serializer=allert__server__pb2.SendImageAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SendImageAlertResponse.FromString,
                _registered_method=True)
        self.SendImageAlertOff = channel.unary_unary(
                '/alerts.AlertService/SendImageAlertOff',
                request_serializer=allert__server__pb2.SendImageAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SendImageAlertResponse.FromString,
                _registered_method=True)
        self.AccidentAlertOn = channel.unary_unary(
                '/alerts.AlertService/AccidentAlertOn',
                request_serializer=allert__server__pb2.AccidentAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.AccidentAlertResponse.FromString,
                _registered_method=True)
        self.AccidentAlertOff = channel.unary_unary(
                '/alerts.AlertService/AccidentAlertOff',
                request_serializer=allert__server__pb2.AccidentAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.AccidentAlertResponse.FromString,
                _registered_method=True)
        self.OddEventAlertOn = channel.unary_unary(
                '/alerts.AlertService/OddEventAlertOn',
                request_serializer=allert__server__pb2.OddEventAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.OddEventAlertResponse.FromString,
                _registered_method=True)
        self.OddEventAlertOff = channel.unary_unary(
                '/alerts.AlertService/OddEventAlertOff',
                request_serializer=allert__server__pb2.OddEventAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.OddEventAlertResponse.FromString,
                _registered_method=True)
        self.IsEmptyAlertOn = channel.unary_unary(
                '/alerts.AlertService/IsEmptyAlertOn',
                request_serializer=allert__server__pb2.IsEmptyAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.IsEmptyAlertResponse.FromString,
                _registered_method=True)
        self.IsEmptyAlertOff = channel.unary_unary(
                '/alerts.AlertService/IsEmptyAlertOff',
                request_serializer=allert__server__pb2.IsEmptyAlertRequest.SerializeToString,
                response_deserializer=allert__server__pb2.IsEmptyAlertResponse.FromString,
                _registered_method=True)
        self.SetCountResult = channel.unary_unary(
                '/alerts.AlertService/SetCountResult',
                request_serializer=allert__server__pb2.SetCountResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SetCountResultResponse.FromString,
                _registered_method=True)
        self.SetAccidentResult = channel.unary_unary(
                '/alerts.AlertService/SetAccidentResult',
                request_serializer=allert__server__pb2.SetAccidentResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SetAccidentResultResponse.FromString,
                _registered_method=True)
        self.SetSendImageResult = channel.unary_unary(
                '/alerts.AlertService/SetSendImageResult',
                request_serializer=allert__server__pb2.SetSendImageResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SetSendImageResultResponse.FromString,
                _registered_method=True)
        self.SetOddEventResult = channel.unary_unary(
                '/alerts.AlertService/SetOddEventResult',
                request_serializer=allert__server__pb2.SetOddEventResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SetOddEventResultResponse.FromString,
                _registered_method=True)
        self.SetIsEmptyResult = channel.unary_unary(
                '/alerts.AlertService/SetIsEmptyResult',
                request_serializer=allert__server__pb2.SetIsEmptyResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.SetIsEmptyResultResponse.FromString,
                _registered_method=True)
        self.GetCountResult = channel.unary_unary(
                '/alerts.AlertService/GetCountResult',
                request_serializer=allert__server__pb2.GetCountResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.GetCountResultResponse.FromString,
                _registered_method=True)
        self.GetAccidentResult = channel.unary_unary(
                '/alerts.AlertService/GetAccidentResult',
                request_serializer=allert__server__pb2.GetAccidentResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.GetAccidentResultResponse.FromString,
                _registered_method=True)
        self.GetSendImageResult = channel.unary_unary(
                '/alerts.AlertService/GetSendImageResult',
                request_serializer=allert__server__pb2.GetSendImageResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.GetSendImageResultResponse.FromString,
                _registered_method=True)
        self.GetOddEventResult = channel.unary_unary(
                '/alerts.AlertService/GetOddEventResult',
                request_serializer=allert__server__pb2.GetOddEventResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.GetOddEventResultResponse.FromString,
                _registered_method=True)
        self.GetIsEmptyResult = channel.unary_unary(
                '/alerts.AlertService/GetIsEmptyResult',
                request_serializer=allert__server__pb2.GetIsEmptyResultRequest.SerializeToString,
                response_deserializer=allert__server__pb2.GetIsEmptyResultResponse.FromString,
                _registered_method=True)


class AlertServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CountAllertOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CountAllertOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendImageAlertOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendImageAlertOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AccidentAlertOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AccidentAlertOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OddEventAlertOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OddEventAlertOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsEmptyAlertOn(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsEmptyAlertOff(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetCountResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetAccidentResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetSendImageResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOddEventResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetIsEmptyResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCountResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccidentResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSendImageResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOddEventResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIsEmptyResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AlertServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CountAllertOn': grpc.unary_unary_rpc_method_handler(
                    servicer.CountAllertOn,
                    request_deserializer=allert__server__pb2.CountAlertRequest.FromString,
                    response_serializer=allert__server__pb2.CountAlertResponse.SerializeToString,
            ),
            'CountAllertOff': grpc.unary_unary_rpc_method_handler(
                    servicer.CountAllertOff,
                    request_deserializer=allert__server__pb2.CountAlertRequest.FromString,
                    response_serializer=allert__server__pb2.CountAlertResponse.SerializeToString,
            ),
            'SendImageAlertOn': grpc.unary_unary_rpc_method_handler(
                    servicer.SendImageAlertOn,
                    request_deserializer=allert__server__pb2.SendImageAlertRequest.FromString,
                    response_serializer=allert__server__pb2.SendImageAlertResponse.SerializeToString,
            ),
            'SendImageAlertOff': grpc.unary_unary_rpc_method_handler(
                    servicer.SendImageAlertOff,
                    request_deserializer=allert__server__pb2.SendImageAlertRequest.FromString,
                    response_serializer=allert__server__pb2.SendImageAlertResponse.SerializeToString,
            ),
            'AccidentAlertOn': grpc.unary_unary_rpc_method_handler(
                    servicer.AccidentAlertOn,
                    request_deserializer=allert__server__pb2.AccidentAlertRequest.FromString,
                    response_serializer=allert__server__pb2.AccidentAlertResponse.SerializeToString,
            ),
            'AccidentAlertOff': grpc.unary_unary_rpc_method_handler(
                    servicer.AccidentAlertOff,
                    request_deserializer=allert__server__pb2.AccidentAlertRequest.FromString,
                    response_serializer=allert__server__pb2.AccidentAlertResponse.SerializeToString,
            ),
            'OddEventAlertOn': grpc.unary_unary_rpc_method_handler(
                    servicer.OddEventAlertOn,
                    request_deserializer=allert__server__pb2.OddEventAlertRequest.FromString,
                    response_serializer=allert__server__pb2.OddEventAlertResponse.SerializeToString,
            ),
            'OddEventAlertOff': grpc.unary_unary_rpc_method_handler(
                    servicer.OddEventAlertOff,
                    request_deserializer=allert__server__pb2.OddEventAlertRequest.FromString,
                    response_serializer=allert__server__pb2.OddEventAlertResponse.SerializeToString,
            ),
            'IsEmptyAlertOn': grpc.unary_unary_rpc_method_handler(
                    servicer.IsEmptyAlertOn,
                    request_deserializer=allert__server__pb2.IsEmptyAlertRequest.FromString,
                    response_serializer=allert__server__pb2.IsEmptyAlertResponse.SerializeToString,
            ),
            'IsEmptyAlertOff': grpc.unary_unary_rpc_method_handler(
                    servicer.IsEmptyAlertOff,
                    request_deserializer=allert__server__pb2.IsEmptyAlertRequest.FromString,
                    response_serializer=allert__server__pb2.IsEmptyAlertResponse.SerializeToString,
            ),
            'SetCountResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SetCountResult,
                    request_deserializer=allert__server__pb2.SetCountResultRequest.FromString,
                    response_serializer=allert__server__pb2.SetCountResultResponse.SerializeToString,
            ),
            'SetAccidentResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SetAccidentResult,
                    request_deserializer=allert__server__pb2.SetAccidentResultRequest.FromString,
                    response_serializer=allert__server__pb2.SetAccidentResultResponse.SerializeToString,
            ),
            'SetSendImageResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SetSendImageResult,
                    request_deserializer=allert__server__pb2.SetSendImageResultRequest.FromString,
                    response_serializer=allert__server__pb2.SetSendImageResultResponse.SerializeToString,
            ),
            'SetOddEventResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOddEventResult,
                    request_deserializer=allert__server__pb2.SetOddEventResultRequest.FromString,
                    response_serializer=allert__server__pb2.SetOddEventResultResponse.SerializeToString,
            ),
            'SetIsEmptyResult': grpc.unary_unary_rpc_method_handler(
                    servicer.SetIsEmptyResult,
                    request_deserializer=allert__server__pb2.SetIsEmptyResultRequest.FromString,
                    response_serializer=allert__server__pb2.SetIsEmptyResultResponse.SerializeToString,
            ),
            'GetCountResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCountResult,
                    request_deserializer=allert__server__pb2.GetCountResultRequest.FromString,
                    response_serializer=allert__server__pb2.GetCountResultResponse.SerializeToString,
            ),
            'GetAccidentResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccidentResult,
                    request_deserializer=allert__server__pb2.GetAccidentResultRequest.FromString,
                    response_serializer=allert__server__pb2.GetAccidentResultResponse.SerializeToString,
            ),
            'GetSendImageResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSendImageResult,
                    request_deserializer=allert__server__pb2.GetSendImageResultRequest.FromString,
                    response_serializer=allert__server__pb2.GetSendImageResultResponse.SerializeToString,
            ),
            'GetOddEventResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOddEventResult,
                    request_deserializer=allert__server__pb2.GetOddEventResultRequest.FromString,
                    response_serializer=allert__server__pb2.GetOddEventResultResponse.SerializeToString,
            ),
            'GetIsEmptyResult': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIsEmptyResult,
                    request_deserializer=allert__server__pb2.GetIsEmptyResultRequest.FromString,
                    response_serializer=allert__server__pb2.GetIsEmptyResultResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'alerts.AlertService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('alerts.AlertService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AlertService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CountAllertOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/CountAllertOn',
            allert__server__pb2.CountAlertRequest.SerializeToString,
            allert__server__pb2.CountAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CountAllertOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/CountAllertOff',
            allert__server__pb2.CountAlertRequest.SerializeToString,
            allert__server__pb2.CountAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendImageAlertOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SendImageAlertOn',
            allert__server__pb2.SendImageAlertRequest.SerializeToString,
            allert__server__pb2.SendImageAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendImageAlertOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SendImageAlertOff',
            allert__server__pb2.SendImageAlertRequest.SerializeToString,
            allert__server__pb2.SendImageAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AccidentAlertOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/AccidentAlertOn',
            allert__server__pb2.AccidentAlertRequest.SerializeToString,
            allert__server__pb2.AccidentAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AccidentAlertOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/AccidentAlertOff',
            allert__server__pb2.AccidentAlertRequest.SerializeToString,
            allert__server__pb2.AccidentAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def OddEventAlertOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/OddEventAlertOn',
            allert__server__pb2.OddEventAlertRequest.SerializeToString,
            allert__server__pb2.OddEventAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def OddEventAlertOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/OddEventAlertOff',
            allert__server__pb2.OddEventAlertRequest.SerializeToString,
            allert__server__pb2.OddEventAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def IsEmptyAlertOn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/IsEmptyAlertOn',
            allert__server__pb2.IsEmptyAlertRequest.SerializeToString,
            allert__server__pb2.IsEmptyAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def IsEmptyAlertOff(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/IsEmptyAlertOff',
            allert__server__pb2.IsEmptyAlertRequest.SerializeToString,
            allert__server__pb2.IsEmptyAlertResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetCountResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SetCountResult',
            allert__server__pb2.SetCountResultRequest.SerializeToString,
            allert__server__pb2.SetCountResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetAccidentResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SetAccidentResult',
            allert__server__pb2.SetAccidentResultRequest.SerializeToString,
            allert__server__pb2.SetAccidentResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetSendImageResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SetSendImageResult',
            allert__server__pb2.SetSendImageResultRequest.SerializeToString,
            allert__server__pb2.SetSendImageResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetOddEventResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SetOddEventResult',
            allert__server__pb2.SetOddEventResultRequest.SerializeToString,
            allert__server__pb2.SetOddEventResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetIsEmptyResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/SetIsEmptyResult',
            allert__server__pb2.SetIsEmptyResultRequest.SerializeToString,
            allert__server__pb2.SetIsEmptyResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetCountResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/GetCountResult',
            allert__server__pb2.GetCountResultRequest.SerializeToString,
            allert__server__pb2.GetCountResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAccidentResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/GetAccidentResult',
            allert__server__pb2.GetAccidentResultRequest.SerializeToString,
            allert__server__pb2.GetAccidentResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSendImageResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/GetSendImageResult',
            allert__server__pb2.GetSendImageResultRequest.SerializeToString,
            allert__server__pb2.GetSendImageResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetOddEventResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/GetOddEventResult',
            allert__server__pb2.GetOddEventResultRequest.SerializeToString,
            allert__server__pb2.GetOddEventResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetIsEmptyResult(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/alerts.AlertService/GetIsEmptyResult',
            allert__server__pb2.GetIsEmptyResultRequest.SerializeToString,
            allert__server__pb2.GetIsEmptyResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
