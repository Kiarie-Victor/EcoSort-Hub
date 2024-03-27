from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware

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
