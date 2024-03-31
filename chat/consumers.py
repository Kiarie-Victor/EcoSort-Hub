from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
import json
from chat.models import Message
from .templatestags import chatextras
from django.utils import timezone
from chat.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

# Middleware for user authentication in WebSocket


class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Function to authenticate the user based on scope
        scope['user'] = await self.get_user(scope=scope)
        return super().__call__(scope, receive, send)

    # Method to retrieve the user from scope asynchronously
    @sync_to_async
    def get_user(self, scope):
        if 'user' in scope:
            return scope['user']
        return None


class ChatConsumer(AsyncWebsocketConsumer):
    # Method to fetch the last 20 messages
    async def get_last_20_messages(self):
        return await Message.get_last_20_messages()

    # Method to fetch messages for a particular request
    async def fetch_messages(self, data):
        message = await self.get_last_20_messages()

        # Constructing message content to send
        content = {
            "command": "fetch_messages",
            "message": await self.message_to_json(message=message)
        }
        await self.send_message(content)

    # Method to convert messages to JSON format
    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(await self.message_to_json(message))
        return result

    # Method to convert a single message to JSON format
    async def message_to_json(self, message: Message):
        return {
            "message": message.body,
            "username": message.sent_by.username,
            "initials": chatextras.initials(message.sent_by.username),
            "created_at": message.created_at
        }

    # Method to handle new messages
    async def new_message(self, data):
        sent_by = await self.get_user(data['from'])
        message = await self.create_message(sent_by=data['from'], body=data['message'])

        # Constructing message content to send
        content = {
            'command': 'new_message',
            'message': await self.message_to_json(message=message)
        }
        await self.send_new_chat_message(content)

    # Method to create a new message
    async def create_message(self, sent_by, body):
        return await Message.objects.create(body=body, sent_by=sent_by)

    # Method to retrieve a user by username asynchronously
    async def get_user(self, username):
        return await User.objects.get(username=username)

    # WebSocket Connection Handling
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        # Adding the connection to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Method to disconnect from WebSocket
    async def disconnect(self, text_content):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Dictionary containing commands and their respective methods
    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    """
    The receive method expects to receive a dictionary containing the following keys:
    {
        "command": "Specifies the type of action to be performed, e.g., new_message or fetch_messages",
        "message": "Contains the message body if the command is new_message",
        "from": "Specifies the sender's username if the command is new_message"
    }
    """
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        command = text_data['command']
        if command:
            await self.commands[command](self, text_data)

    # Method to broadcast new messages to the group
    async def send_new_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    # Method to send a new chat message
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))

    # Method to send a message
    async def send_message(self, event):
        await self.send(text_data=json.dumps(event))
