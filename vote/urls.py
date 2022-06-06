from django.urls import path
from .views import (VoteListView, VoteCreateView,
                    VoteUserView, )

urlpatterns = [
    path('create_vote/', VoteCreateView.as_view()),
    path('vote/list/', VoteListView.as_view()),
    path('vote_user/<int:pk>', VoteUserView.as_view())
]
