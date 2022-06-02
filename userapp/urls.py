from django.urls import path
from .views import UserListView, UserDetailView

urlpatterns = [
    path('userlist', UserListView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view())
]
