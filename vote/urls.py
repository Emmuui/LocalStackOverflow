from django.urls import path
from .views import (VoteListView, VoteView)

urlpatterns = [
    path('create_vote/', VoteView.as_view()),
    path('vote/list/', VoteListView.as_view())
]
