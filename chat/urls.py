from django.urls import path
from .views import PublicChatRoomView, index, room


urlpatterns = [
    path('chat/', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('public_chat/', PublicChatRoomView.as_view()),
]
