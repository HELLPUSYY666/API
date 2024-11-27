from django.urls import path
from api.consumers import WsConsumer, NotificationConsumer

websocket_urlpatterns = [
    path('ws/', WsConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]
