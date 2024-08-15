import asyncio
import websockets


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
