from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sync/<str:groupname>/', consumers.MyWebSocketConsumer.as_asgi()),
    path('ws/async/', consumers.MyAsyncWebSocketConsumer.as_asgi())
]
