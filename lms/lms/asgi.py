import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

application = get_asgi_application()
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from courses import consumers
from django.urls import path


from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser

ws_pattern= [
    path('ws/room/<room_code>/' , consumers.ChatConsumer.as_asgi())
]

application= ProtocolTypeRouter(
    {
        'websocket':(URLRouter(ws_pattern))
    }
)