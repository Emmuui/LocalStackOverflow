from django.urls import path
from .views import (GetUserListView, UserDetailView,
                    PutUserDetailView, OwnUserDataDetailView,
                    ImageUploadView)


urlpatterns = [
    path('user/me/', OwnUserDataDetailView.as_view()),
    path('user/list/', GetUserListView.as_view()),
    path('user/detail/<int:pk>/', UserDetailView.as_view()),
    path('user/put/', PutUserDetailView.as_view()),
    path('user/image_upload/', ImageUploadView.as_view())
]
