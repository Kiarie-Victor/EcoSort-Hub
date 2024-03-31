from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
import json
from chat.models import Message
from .templatestags import chatextras
from django.utils import timezone
from chat.models import Message

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

    # fetching past messages
    async def get_last_20_messages(self):
        return await Message.get_last_20_messages()


    async def fetch_messages(self,data):
        message = await self.get_last_20_messages()
        
        content = {
            "command": "fetched_messages",
            "message": await self.message_to_json(message=message)
        }


    async def messages_to_json(self, messages):
        result=[]
        for message in messages:
            result.append(self.message_to_json(messages))
        return result

    async def message_to_json(self, message: Message):
        return {
            "message": message.body,
            "username": message.sent_by.username,
            "initials": chatextras.initials(message.sent_by.username),
            "created_at": message.created_at
        }

    # WebSocket Connection Handling
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.commands = {
            "fetch_message":"fetch_message",
            "new_message":"new_message"
        }

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

    async def send_new_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    @sync_to_async
    def create_new_message(self, message, name):
        new_message = Message.objects.create(body=message, sent_by=name)
        new_message.save()
        return message

