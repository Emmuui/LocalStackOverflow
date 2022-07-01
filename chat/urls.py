from django.urls import path
from .views import PublicChatRoomView


urlpatterns = [
    path('public_chat/', PublicChatRoomView.as_view())
]
