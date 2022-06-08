from django.urls import path
from .views import (QuestionListView, QuestionCreateView, TagView,
                    QuestionDetailView, TagCreateView, AllQuestion,
                    AnswerView, UserAnswerView, CreateAnswerView,
                    CommentListView, CreateCommentView, CommentRelatedView,
                    AnswerDetailView, CommentTestRelatedView, UpdateCommentView,
                    DeleteCommentView, DetailCommentView)


urlpatterns = [
    path('question_list/user/<int:pk>/', QuestionListView.as_view()),
    path('question/list/', AllQuestion.as_view()),
    path('create/question/', QuestionCreateView.as_view()),
    path('question/detail/<int:pk>/', QuestionDetailView.as_view()),

    path('tag/list/', TagView.as_view()),
    path('tag/create/', TagCreateView.as_view()),

    path('answer/list/', AnswerView.as_view()),
    path('answer/<int:pk>/', UserAnswerView.as_view()),
    path('answer/detail/<int:pk>', AnswerDetailView.as_view()),
    path('create/answer/', CreateAnswerView.as_view()),

    path('comment/list/', CommentListView.as_view()),
    path('detail/comment/<int:pk>', DetailCommentView.as_view()),
    path('create/comment/', CreateCommentView.as_view()),
    path('update/comment/<int:pk>', UpdateCommentView.as_view()),
    path('delete/comment/<int:pk>', DeleteCommentView.as_view()),

    path('test_view/', CommentRelatedView.as_view()),
    path('comment_test_view/', CommentTestRelatedView.as_view())
]
