from django.urls import re_path
from api.consumers import WsConsumer

websocket_urlpatterns = [
    re_path('ws/', WsConsumer.as_asgi()),
]
