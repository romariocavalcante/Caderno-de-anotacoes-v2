# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadernodeanotacoesv2.settings')

# application = get_asgi_application()



import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from caderno import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadernodeanotacoesv2.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('cliente/<int:id>/', consumers.AnotacoesConsumer.as_asgi(), name='anotacoes'),
        ])
    ),
})
