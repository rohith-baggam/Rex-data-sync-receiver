import asyncio
import inspect
import json
import websockets
from .utils import (
    request_websockt_websocket,
    connect_websocket,
    get_project_models,
    convert_string_to_json
)
from core.settings import (
    SENDER_HOST,
    DATA_SYNC_SENDER_TOKEN,
    SECRET_KEY
)
from data_sync.receiver_utils.cipher import encrypt_data, decrypt_data
from data_sync.receiver_utils.schema_verification import get_model_properties
from data_sync.models import DataSyncTestBooleanModel
from data_sync.receiver_utils.websocket_utils import broadcast_data
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

    # data = [
    #     connect_websocket(
    #         uri=f"{SENDER_HOST}/sender-socket/",
    #         message_to_send=json.dumps(
    #             {
    #                 "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
    #                 "data": {
    #                     "type": str(
    #                         inspect.currentframe(
    #                         ).f_code.co_name
    #                     ).upper(),
    #                     "model_meta_data": encrypt_data(
    #                         get_model_properties(
    #                             model=model
    #                         )
    #                     )
    #                 }
    #             }
    #         )
    #     )
    #     for model in get_project_models()
    # ]
    for model in get_project_models():
        from time import sleep
        sleep(1)
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
                        "model_meta_data": encrypt_data(
                            get_model_properties(
                                model=model
                            )
                        )
                    }
                }
            )
        )
        print('json-data', convert_string_to_json(data))
        print("data['data']['status_code']", data, type(data))
        print('json-data', convert_string_to_json(data),
              type(convert_string_to_json(data)))
        data = convert_string_to_json(data)
        if data['data']['status_code'] == 400:
            broadcast_data(
                {
                    'status_code': 400,
                    'message': "Schema verification failed",
                }
            )
            return data
    return data


def data_information():
    response = connect_websocket(
        uri=f"{SENDER_HOST}/sender-socket/",
        message_to_send=json.dumps(
            {
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper()
                }
            }
        )
    )
    # count = response['']
    print('response', response)
    return response


def data_transformation():
    # data_info = data_information()
    # print('data_info', data_info, type(data_info))
    # json_data = convert_string_to_json(
    #     data_info)
    # print('json_data', json_data)
    # count = decrypt_data(
    #     json_data['data']['model_meta_data']
    # )
    # print('count', count)
    response = connect_websocket(
        uri=f"{SENDER_HOST}/sender-socket/",
        message_to_send=json.dumps(
            {
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper(),
                    "model_meta_data": {
                        "index":  encrypt_data(10)
                    }
                }
            }
        )
    )
    return response
