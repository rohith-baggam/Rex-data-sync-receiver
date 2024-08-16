import json
import ast
import asyncio
import websockets
from django.apps import apps


async def request_websockt_websocket(uri, message_to_send):
    try:
        async with websockets.connect(uri) as websocket:
            # Print the connect message
            print("Connected to WebSocket")

            # Send the message to the WebSocket server
            await websocket.send(message_to_send)
            print(f"Sent message: {message_to_send}")

            # Wait for and print the response from the server
            response = await websocket.recv()
            await websocket.send(message_to_send)
            response = await websocket.recv()

            print(f"Received message: {response}")
            return response
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def connect_websocket(uri, message_to_send):
    # output = asyncio.get_event_loop(
    # ).run_until_complete(
    #     request_websockt_websocket(
    #         uri=uri,
    #         message_to_send=message_to_send
    #     )
    # )
    output = asyncio.run(request_websockt_websocket(uri, message_to_send))
    return output


def get_project_models(model_name=None):
    installed_apps = [
        app_config.name for app_config in apps.get_app_configs()
    ]
    print('all models', apps.get_models())
    models = [
        model for model in apps.get_models()
        if model._meta.app_label in installed_apps and (not model_name or model_name in str(model))
    ]

    return models


def convert_nested_string_to_json(data):
    # ? Recursively process dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_nested_string_to_json(value)
        return data
    # ? Recursively process list
    elif isinstance(data, list):
        return [convert_nested_string_to_json(item) for item in data]
    # ? Convert string representation of a dict or list
    elif isinstance(data, str):
        try:
            # ? Attempt to parse as JSON
            parsed_data = json.loads(data)
            return convert_nested_string_to_json(parsed_data)
        except (json.JSONDecodeError, ValueError):
            try:
                # ? Attempt to evaluate Python dict-like string
                parsed_data = ast.literal_eval(data)
                return convert_nested_string_to_json(parsed_data)
            except (ValueError, SyntaxError):
                return data
    else:
        return data


def convert_string_to_json(data: str) -> dict:
    # ? First, parse the outermost JSON
    json_data = json.loads(data)
    # ? Then recursively convert any nested string representations
    json_data = convert_nested_string_to_json(json_data)
    return json_data
