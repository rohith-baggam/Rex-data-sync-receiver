import asyncio
import inspect
from .utils import request_websockt_websocket
from core.settings import (
    SENDER_HOST,
    DATA_SYNC_SENDER_TOKEN,
    SECRET_KEY
)
from data_sync.receiver_utils.cipher import encrypt_data
# Example usage


def token_verification():
    output = asyncio.get_event_loop(
    ).run_until_complete(
        request_websockt_websocket(
            uri=f"{SENDER_HOST}/sender-socket/?token=your_token_here", message_to_send=str(
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
    )
    print('output', output)


def secret_key_verification():
    output = asyncio.get_event_loop(
    ).run_until_complete(
        request_websockt_websocket(
            uri=f"{SENDER_HOST}/sender-socket/?token=your_token_here", message_to_send=str(
                {
                    "token": encrypt_data(DATA_SYNC_SENDER_TOKEN),
                    "data": {
                        "type": str(
                            inspect.currentframe(
                            ).f_code.co_name
                        ).upper(),
                        "SECRET_KEY": SECRET_KEY
                    }
                }
            )
        )
    )
    print('output', output)
