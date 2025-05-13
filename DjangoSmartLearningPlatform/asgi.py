# asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import learning.routing  # مسیر اپی که Consumer دارد

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoSmartLearningPlatform.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            learning.routing.websocket_urlpatterns
        )
    ),
})
