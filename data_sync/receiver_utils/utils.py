import asyncio
import websockets
from django.apps import apps


async def request_websockt_websocket(uri, message_to_send):
    try:
        a = []
        async with websockets.connect(uri) as websocket:
            # Print the connect message
            print("Connected to WebSocket")

            # Send the message to the WebSocket server
            await websocket.send(message_to_send)
            print(f"Sent message: {message_to_send}")
            a.append(message_to_send)
            # Wait for and print the response from the server
            response = await websocket.recv()
            print(f"Received message: {response}")
            a.append(response)
        return a
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def connect_websocket(uri, message_to_send):
    output = asyncio.get_event_loop(
    ).run_until_complete(
        request_websockt_websocket(
            uri=uri,
            message_to_send=message_to_send
        )
    )
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
