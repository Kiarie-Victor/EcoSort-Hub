from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
import json
from chat.models import Message
from .templatestags import chatextras
from django.utils import timezone

# making user authentication in websocket
class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = await self.get_user(scope=scope)
        return super().__call__(scope, receive, send)

    

    @sync_to_async
    def get_user(self, scope):
        if 'user' in scope:
            return scope['user']
        return None

class ChatConsumer(AsyncWebsocketConsumer):

    # WebSocket Connection Handling
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, text_content):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data = json.loads(text_data)
        message = text_data['message']
        name = text_data['name']
        new_message = await self.create_new_message(message,name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'name': name,
                'initials':chatextras.initials(value=name),
                'created_at': strftime(new_message.created_at, "%I:%M %p")
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        name = event['name']
        initials = event['initials']
        created_at = event['created_at']

        await self.send(text_data=json.dumps({
            'message': message,
            'name': name,
            'initials': initials,
            'created_at': created_at
        }))

    @sync_to_async
    def create_new_message(self, message, name):
        new_message = Message.objects.create(body=message, sent_by=name)
        new_message.save()
        return message

