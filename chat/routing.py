from django.urls import path
from .consumers import ChatConsumer

# Define WebSocket URL patterns
websocket_urlpatterns = [
    # Route WebSocket connections to the ChatConsumer
    path('ws/chat/', ChatConsumer.as_asgi()),
]
