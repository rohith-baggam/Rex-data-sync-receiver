import asyncio
import inspect
import json
import websockets
from .utils import (
    request_websockt_websocket,
    connect_websocket,
    get_project_models,
    convert_string_to_json,
    load_object
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
from django.db import transaction
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
        from time import sleep
        sleep(0.1)
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
    print('data_information')
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


def loaddata_from_response(index, socket_type):
    print('loaddata_from_response')
    response = connect_websocket(
                    uri=f"{SENDER_HOST}/sender-socket/",
                    message_to_send=json.dumps(
                        {
                            "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                            "data": {
                                "type":socket_type ,
                                "model_meta_data": {
                                    "index":  encrypt_data(index)
                                }
                            }
                        }
                    )
                )
    print(1)
    response_json_data = convert_string_to_json(
                    response)
    print(2)
    print()
    print()
    print('index',index)
    print()
    print()
    print()
    object_data = decrypt_data(
        response_json_data['data']['buffer_data']
    )
    print('object_data', object_data)
    load_object(
        model_name=object_data['model'],
        pk=object_data['pk'],
        data=object_data['fields']
    )
def data_transformation_successful():
    socket_response = {}
    socket_response['status_code'] = 200
    socket_response['message'] = "Data Transformation is Done Successfully"
    from data_sync.receiver_utils.websocket_utils import broadcast_data
    broadcast_data(
        messsage_object=socket_response
    )
    return socket_response

def data_transformation():
    print('data_transformation')
    data_info = data_information()
    print('data_info', data_info, type(data_info))
    json_data = convert_string_to_json(
        data_info)
    print('json_data', json_data)
    count = decrypt_data(
        json_data['data']['model_meta_data']
    )
    print('count', count)
    try:
        with transaction.atomic():
            for index in range(0, count):
                loaddata_from_response(
                                index, str(
                                    inspect.currentframe(
                                    ).f_code.co_name
                                ).upper())
                
        data_transformation_successful() 
    except Exception as e:
        print('Error index', e)
        return False
           
    return True 

from time import sleep
def run_data_transformation():
    token_verification_data = convert_string_to_json(token_verification())
    print('token_verification', token_verification_data)
    sleep(2.5)
    if token_verification_data['data']['status_code']==200:
        print('verified')
        sleep(2.5)
        secret_key_verification_data = convert_string_to_json(secret_key_verification())
        if secret_key_verification_data['data']['status_code']==200:
            print('verified')
            
            schema_verification_data = schema_verification()
            print('schema_verification_data output',schema_verification_data, type(schema_verification_data))
            # print('schema_verification_data statuscode', schema_verification_data)
            # schema_verification_data = convert_string_to_json(schema_verification_data)
            print('schema_verification_data status code', schema_verification_data['data'], )
            print("type(schema_verification_data['data'])", type(schema_verification_data['data']))
            if schema_verification_data['data']['status_code']==200:
                print('schema is verified')
                if data_transformation():
                    print("Data transformation is done")
                else:
                    print("Data transformation is failed")

        else:
            print('Secret key not verified')
    else:
            print('Token not verified')