import json
import random
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer


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
