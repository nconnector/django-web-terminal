"""
Consumer can connect to websockets or worker processes
"""
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class MessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("logging", self.channel_name)
        print(f"Added {self.channel_name} channel to logging")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("logging", self.channel_name)
        print(f"Removed {self.channel_name} channel from logging")

    async def case_logging(self, event):  # _ instead of . for sync method in signals.py
        await self.send_json(event)
        print(f"Got message {event}")
