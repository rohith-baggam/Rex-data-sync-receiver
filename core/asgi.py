"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import django
import os
from data_sync import consumers as receiver_consumer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
django_asgi_app = get_asgi_application()


websocket_urlpatterns = [
    re_path(r'ws/receiver-socket/',
            receiver_consumer.DataSyncReceiverConsumer.as_asgi()),
    re_path(r'ws/data-transformation-socket/',
            receiver_consumer.DataSyncDataTransformationConsumer.as_asgi()),

]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            AllowedHostsOriginValidator(
                URLRouter(
                    websocket_urlpatterns
                )
            ))

    }
)
