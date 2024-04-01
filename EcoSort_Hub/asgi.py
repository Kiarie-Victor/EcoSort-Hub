"""
ASGI config for EcoSort_Hub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

# Set the Django settings module for the ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoSort_Hub.settings')

# Get the Django ASGI application
django_asgi_application = get_asgi_application()

# Define the ASGI application with routing for different protocols
application = ProtocolTypeRouter({
    # For HTTP protocol, use the Django ASGI application
    'http': django_asgi_application,
    # For WebSocket protocol, use allowed hosts origin validator and auth middleware stack
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    )
})
