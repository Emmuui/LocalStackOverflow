from django.urls import path
from .views import (UserQuestionListView, QuestionCreateView, TagView,
                    QuestionDetailView, TagCreateView, QuestionListView,
                    AnswerView, UserAnswerView, CreateAnswerView,
                    CommentListView, CreateCommentView, CommentRelatedView,
                    AnswerDetailView, CommentTestRelatedView, UpdateCommentView,
                    DeleteCommentView, DetailCommentView, UpdateQuestionView,
                    DeleteQuestionView, TagUpdateView)

urlpatterns = [
    path('question_list/user/<int:pk>/', UserQuestionListView.as_view()),
    path('question/list/', QuestionListView.as_view()),
    path('question/create/', QuestionCreateView.as_view()),
    path('question/detail/<int:pk>/', QuestionDetailView.as_view()),
    path('question/update/<int:pk>/', UpdateQuestionView.as_view()),
    path('question/delete/<int:pk>/', DeleteQuestionView.as_view()),

    path('tag/list/', TagView.as_view()),
    path('tag/create/', TagCreateView.as_view()),
    path('tag/update/<int:pk>', TagUpdateView.as_view()),

    path('answer/list/', AnswerView.as_view()),
    path('answer/<int:pk>/', UserAnswerView.as_view()),
    path('answer/detail/<int:pk>', AnswerDetailView.as_view()),
    path('create/answer/', CreateAnswerView.as_view()),

    path('comment/list/', CommentListView.as_view()),
    path('comment/detail/<int:pk>', DetailCommentView.as_view()),
    path('comment/create/', CreateCommentView.as_view()),
    path('comment/update/<int:pk>', UpdateCommentView.as_view()),
    path('comment/delete/<int:pk>', DeleteCommentView.as_view()),

    path('test_view/', CommentRelatedView.as_view()),
    path('comment_test_view/', CommentTestRelatedView.as_view())
]


