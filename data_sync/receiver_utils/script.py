import inspect
import json
from .utils import (
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
from data_sync.receiver_utils.websocket_utils import broadcast_data
from django.db import transaction
from time import sleep


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

        data = convert_string_to_json(data)
        if data['data']['status_code'] == 400:
            broadcast_data(
                {
                    'status_code': 400,
                    'message': "Schema verification failed",
                }
            )
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

    return response


def loaddata_from_response(index, socket_type):

    response = connect_websocket(
        uri=f"{SENDER_HOST}/sender-socket/",
        message_to_send=json.dumps(
            {
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": socket_type,
                    "model_meta_data": {
                        "index":  encrypt_data(index)
                    }
                }
            }
        )
    )

        uri = f"{SENDER_HOST}/sender-socket/",
        message_to_send = json.dumps(
            {
                "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                "data": {
                    "type": socket_type,
                    "model_meta_data": {
                        "index":  encrypt_data(index)
                    }
                }
            }
        )
    )

    response_json_data = convert_string_to_json(
        response)

        response)

    object_data = decrypt_data(
        response_json_data['data']['buffer_data']
    )


    load_object(
        model_name=object_data['model'],
        pk=object_data['pk'],
        data=object_data['fields']
    )




def data_transformation_successful():
    socket_response = {}
    socket_response['status_code'] = 200
    socket_response['message'] = "A perfect landing and a synchronized database mission! success from start to finish"
    from data_sync.receiver_utils.websocket_utils import broadcast_data
    broadcast_data(
        messsage_object=socket_response
    )
    return socket_response



def data_transformation():


    data_info = data_information()


    json_data = convert_string_to_json(
        data_info)


    count = decrypt_data(
        json_data['data']['model_meta_data']
    )


    try:
        with transaction.atomic():
            for index in range(0, count):
                loaddata_from_response(
                    index, str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper())

        data_transformation_successful()
                    index, str(
                        inspect.currentframe(
                        ).f_code.co_name
                    ).upper())

        data_transformation_successful()
    except Exception as e:


        return False

    return True

    return True



def run_data_transformation():
    verifications = [
        (token_verification, 'Token verification failed', 'Token verified'),
        (secret_key_verification, 'Secret key not verified', 'Secret key verified'),
        (schema_verification, 'Schema verification failed', 'Schema is verified')
    ]


    for verify_func, failure_message, success_message in verifications:
        print(f"Running {verify_func.__name__}...")
        if success_message == "Secret key verified":
            sleep(5)  # ? Simulating processing delay
        if verify_func == schema_verification:
            # ? For schema_verification, which doesn't use convert_string_to_json
            verification_data = verify_func()
            status_code = verification_data['data']['status_code']
        else:
            # ? For other verifications, use convert_string_to_json
            verification_data = convert_string_to_json(verify_func())
            status_code = verification_data['data']['status_code']


        if status_code == 200:
            print(success_message)
        else:
            print(failure_message)
            return

    # Final data transformation
    if data_transformation():
        print("Data transformation is done")
    else:
        print("Data transformation failed")

