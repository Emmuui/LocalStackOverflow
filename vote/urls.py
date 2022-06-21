from django.urls import path
from .views import (VoteListView, VoteServiceView,
                    VoteUserView)

urlpatterns = [
    path('vote_service/', VoteServiceView.as_view()),
    path('list/', VoteListView.as_view()),
    path('user/<int:pk>/', VoteUserView.as_view())
]
