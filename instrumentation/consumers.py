import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class TerminalConsumer(AsyncJsonWebsocketConsumer):
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

    async def connect(self):
        self.resource_name = self.scope['url_route']['kwargs']['resource_name']
        self.resource_group_name = 'terminal_%s' % self.resource_name

        print('---------------------------------------------------------------')


        # Join room group
        await self.channel_layer.group_add(
            self.resource_group_name,
            self.channel_name
        )

        await self.accept()

        logger.info('"%s" connected to websocket-bridge "%s".' % (self.resource_name, self.resource_group_name))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.resource_group_name,
            self.channel_name
        )

        logger.info('"%s" disconnected to websocket-bridge "%s".' % (self.resource_name, self.resource_group_name))

    # Receive message from WebSocket
    async def receive_json(self, content):

        print('---------------------------------------------------------------')
        print('---------------------------------------------------------------')

        # text_data_json = json.loads(content)
        message = content

        # Send message to room group
        await self.channel_layer.group_send(
            self.resource_group_name,
            {
                'type': 'resource_terminal',
                'message': message
            }
        )

    # Receive message from room group
    async def resource_terminal(self, event):
        print('---------------------------------------------------------------')
        print('---------------------------------------------------------------')
        print('---------------------------------------------------------------')


        message = event['message']

        # Send message to WebSocket
        await self.send_json(content={
            'message': message
        })
