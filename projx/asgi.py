import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projx.settings")

import django

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


from .token_auth import TokenAuthMiddleware
from signalbot.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenAuthMiddleware(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
