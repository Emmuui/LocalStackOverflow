from django.urls import path
from .views import MessageToUserCreateView, GetAllMessageIfOwnerView, GetListChatByOneUser, \
    MessageToUserPutView


urlpatterns = [
    path('create_message/', MessageToUserCreateView.as_view()),
    path('update_message/<int:pk>', MessageToUserPutView.as_view()),
    path('user_message_list/', GetAllMessageIfOwnerView.as_view()),
    path('user_all_chats/', GetListChatByOneUser.as_view()),
]
