from django.urls import path
from .views import PublicChatRoomView, index, room, test


urlpatterns = [
    path('test/', test, name='test_page'),
    path('chat/', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('public_chat/', PublicChatRoomView.as_view()),
]
