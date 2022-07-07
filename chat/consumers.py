import asyncio
import os
from time import sleep

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from userapp.models import UserProfile


class MyWebSocketConsumer(WebsocketConsumer):

    def connect(self):
        print('Websocket connected')
        print(f'Channel layer: {self.channel_layer}')
        print(f'Channel name: {self.channel_name}')
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print(f'group_name = {self.group_name}')
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print(f'Message Received from Client... {text_data}')
        for i in range(20):
            self.send(text_data=str(i))
            sleep(1)

    def disconnect(self, close_code):
        print(f'Websocket disconnected {close_code}')


class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('Websocket connected')
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print(f'Message Received from Client... {text_data}')
        for i in range(5):
            await self.send(text_data=str(i))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        print(f'Websocket disconnected {close_code}')
