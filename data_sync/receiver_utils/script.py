import asyncio
import inspect
import json
from .utils import (
    request_websockt_websocket,
    connect_websocket,
    get_project_models
)
from core.settings import (
    SENDER_HOST,
    DATA_SYNC_SENDER_TOKEN,
    SECRET_KEY
)
from data_sync.receiver_utils.cipher import encrypt_data
from data_sync.receiver_utils.schema_verification import get_model_properties
from data_sync.models import DataSyncTestBooleanModel
# Example usage


def token_verification():
    data = connect_websocket(
        uri=f"{SENDER_HOST}/sender-socket/",
        message_to_send=json.dumps({
            "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
            "data": {
                "type": str(
                    inspect.currentframe(
                    ).f_code.co_name
                ).upper()
            }
        },
            indent=4
        ))
    return data

# json.dumps(data, indent=4)


def secret_key_verification():
    data = connect_websocket(
        uri=f"{SENDER_HOST}/sender-socket/",
        message_to_send=json.dumps(
            {
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper(),
                    "SECRET_KEY": encrypt_data(
                        SECRET_KEY
                    )
                }
            },
            indent=4
        )
    )
    return data


def schema_verification():

    for model in get_project_models():
        print('model', model)

        data = connect_websocket(
            uri=f"{SENDER_HOST}/sender-socket/",
            message_to_send=json.dumps({
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper(),
                    "model_meta_data": encrypt_data(
                        get_model_properties(
                            model=model
                        )
                    )
                }
            })
        )
    return data
