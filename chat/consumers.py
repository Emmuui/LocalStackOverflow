import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from channels.generic.websocket import AsyncWebsocketConsumer


class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('AsyncWebsocket connected')
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_user_id = str(self.room_name)
        print(f'Channel layer: {self.channel_layer}')
        print(f'Channel name: {self.channel_name}')

        await self.channel_layer.group_add(
            self.room_user_id,
            self.channel_name
        )
        await self.accept()

    async def chat_message(self, event):
        await self.send(f'{event["author"]}: {event["message"]} ')

    async def disconnect(self, close_code):
        print(f'Websocket disconnected {close_code}')
        await self.channel_layer.group_discard(
            self.room_user_id,
            self.channel_name
        )
