import asyncio
import json

import redis

from channels.generic.websocket import AsyncWebsocketConsumer

redis_client = redis.Redis(host="localhost", port=6379)


class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        while True:

            data = redis_client.get("latest_metrics")

            if data:
                await self.send(data.decode())

            await asyncio.sleep(1)