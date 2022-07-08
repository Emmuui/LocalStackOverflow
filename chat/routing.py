from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/async/<int:pk>/', consumers.MyAsyncWebSocketConsumer.as_asgi())
]
