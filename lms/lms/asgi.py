import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

application = get_asgi_application()
from channels.routing import ProtocolTypeRouter,URLRouter
from courses import consumers
from django.urls import path

ws_pattern= [
    path('ws/room/<room_code>/' , consumers.ChatConsumer.as_asgi())
]

application= ProtocolTypeRouter(
    {
        'websocket':(URLRouter(ws_pattern))
    }
)