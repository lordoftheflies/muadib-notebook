import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TerminalConsumer(WebsocketConsumer):
    # async def connect(self):
    #     await self.accept()
    #     # AsyncToSync(self.channel_layer.group_add)('task-i-1', self.channel_name)
    #
    # async def disconnect(self, close_code):
    #     pass
    #
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['resource_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))