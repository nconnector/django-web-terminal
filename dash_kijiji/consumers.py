"""
Consumer can connect to websockets or worker processes
"""
import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.consumer import AsyncConsumer


class MessageConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("gossip", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print(f"Removed {self.channel_name} channel from gossip")

    async def user_gossip(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")


class CommandConsumer(AsyncConsumer):
    #channel_layer_alias = 'commands_layer'

    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        print(event)
        await self.send({  # send(event)
            "type": "websocket.send",
            "text": event["text"],
        })



class TickTockConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            await asyncio.sleep(1)
            await self.send_json('tick')
            await asyncio.sleep(1)
            await self.send_json('tock')

