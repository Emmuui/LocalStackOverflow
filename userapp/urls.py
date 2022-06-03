from django.urls import path
from .views import (GetUserListView, GetUserDetailView,
                    PutUserDetailView)

urlpatterns = [
    path('user/list/', GetUserListView.as_view()),
    path('user/get_detail/<int:pk>/', GetUserDetailView.as_view()),
    path('user/put_detail/<int:pk>/', PutUserDetailView.as_view()),
]
