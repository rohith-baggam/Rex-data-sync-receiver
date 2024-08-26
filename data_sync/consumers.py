from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from urllib.parse import parse_qs
from data_sync.receiver_utils.websocket_utils import (
    websocket_connectivity
)
import json
from data_sync.receiver_utils.script import run_data_transformation


class DataSyncReceiverConsumer(WebsocketConsumer):

    """
        This web socket does receiver action
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.conversation_name = None

    def connect(self):
        try:
            self.accept()
            query_string_bytes = self.scope.get("query_string", b"")
            query_string = parse_qs(query_string_bytes.decode("utf-8"))
            self.conversation_name = "receiver_socket"
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "data_sync",
                    "status": "sending",
                    "conversations": self.conversation_name,
                    "data": {
                        "status_code": 200,
                        "message": "Connected",
                        "buffer_data": None
                    }
                },
            )

        except Exception as e:
            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            try:
                text_data_json = json.loads(text_data)
            except Exception as e:
                text_data_json = {}
                self.disconnect(
                    f'json convertion error, {str(e)}'
                )
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )
            websocket_connectivity(
                text_json=text_data_json
            )
        except Exception as e:
            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def disconnect(self, close_code="Web disconnected"):

        return

    def data_sync(self, event):
        self.send(text_data=json.dumps(event))

    def data_transformation_successful(self, event):
        self.send(text_data=json.dumps(event))


class DataSyncDataTransformationConsumer(WebsocketConsumer):

    """
        This web socket does receiver action
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.conversation_name = None

    def connect(self):
        try:
            self.accept()
            self.conversation_name = "receiver_socket"
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_name,
                self.channel_name,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "data_transformation_controller",
                    "status": "sending",
                    "conversations": self.conversation_name,
                    "data": {
                        "status_code": 200,
                        "message": "Connected",
                        "buffer_data": None
                    }
                },
            )

        except Exception as e:
            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            run_data_transformation()
        except Exception as e:
            self.disconnect(
                close_code=f"Receiver was disconnected due to , {str(e)}")

    def disconnect(self, close_code="Web disconnected"):

        return

    def data_transformation_controller(self, event):
        self.send(text_data=json.dumps(event))
