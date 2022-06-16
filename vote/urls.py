from django.urls import path
from .views import (VoteListView, VoteCreateView,
                    VoteUserView, VoteUpdateView)

urlpatterns = [
    path('create/', VoteCreateView.as_view()),
    path('list/', VoteListView.as_view()),
    path('update/', VoteUpdateView.as_view()),
    path('user/<int:pk>/', VoteUserView.as_view())
]
