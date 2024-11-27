import json
import random
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from .serializer import NotificationSerializer


class WsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        try:
            for i in range(1000):
                await self.send(json.dumps({'message': random.randint(1, 100)}))
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Connection closed by client.")
        finally:
            await self.close()

    async def disconnect(self, code):
        print(f"WebSocket disconnected with code: {code}")


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def send_notification(self, notification):
        serializer = NotificationSerializer(notification)
        await self.send(text_data=json.dumps(serializer.data))
