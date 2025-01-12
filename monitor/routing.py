# routing.py

from django.urls import path
from .consumers import ScreenStreamConsumer

websocket_urlpatterns = [
    path('websockets/<str:id>', ScreenStreamConsumer.as_asgi()),
]
