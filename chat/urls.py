from django.urls import path
from .views import MessageToUserCreateView, GetAllMessageFromOneChat, GetListChatUser


urlpatterns = [
    path('create_message/', MessageToUserCreateView.as_view()),
    path('message_list_to_one_chat/<int:pk>', GetAllMessageFromOneChat.as_view()),
    path('user_all_chats/', GetListChatUser.as_view()),
]
