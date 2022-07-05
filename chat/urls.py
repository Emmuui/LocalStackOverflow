from django.urls import path
from .views import MessageToUserCreateView, GetAllMessageIfOwnerView, MessageListIfRecipientView,\
    RoomMessageCreate, RoomMessageListView, ListMessageByChat, PublicChatRoomView, index, room, test


urlpatterns = [
    path('create_message/', MessageToUserCreateView.as_view()),
    path('user_message_list/', GetAllMessageIfOwnerView.as_view()),
    path('message_if_recipient/', MessageListIfRecipientView.as_view()),

    path('list_message_by_chat/<int:pk>', ListMessageByChat.as_view()),

    path('room_message_create/', RoomMessageCreate.as_view()),
    path('room_message_list/<int:pk>', RoomMessageListView.as_view()),

    # path('test/', test, name='test_page'),
    # path('chat/', index, name='index'),
    # path('<str:room_name>/', room, name='room'),
    # path('public_chat/', PublicChatRoomView.as_view()),
]
