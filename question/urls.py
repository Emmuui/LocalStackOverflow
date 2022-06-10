from django.urls import path
from .views import (UserQuestionListView, QuestionCreateView, TagView,
                    QuestionDetailView, TagCreateView, QuestionListView,
                    AnswerView, UserAnswerView, CreateAnswerView,
                    CommentListView, CreateCommentView, AnswerDetailView,
                    UpdateCommentView, DeleteCommentView, DetailCommentView,
                    QuestionUpdateView, QuestionDeleteView, TagUpdateView,
                    TagDeleteView)

urlpatterns = [
    path('queston/user/<int:pk>/', UserQuestionListView.as_view()),
    path('question/list/', QuestionListView.as_view()),
    path('question/create/', QuestionCreateView.as_view()),
    path('question/detail/<int:pk>/', QuestionDetailView.as_view()),
    path('question/update/<int:pk>/', QuestionUpdateView.as_view()),
    path('question/delete/<int:pk>/', QuestionDeleteView.as_view()),

    path('tag/list/', TagView.as_view()),
    path('tag/create/', TagCreateView.as_view()),
    path('tag/update/<int:pk>/', TagUpdateView.as_view()),
    path('tag/delete/<int:pk>/', TagDeleteView.as_view()),

    path('answer/list/', AnswerView.as_view()),
    path('answer/user/', UserAnswerView.as_view()),
    path('answer/detail/<int:pk>/', AnswerDetailView.as_view()),
    path('answer/create/', CreateAnswerView.as_view()),

    path('comment/list/', CommentListView.as_view()),
    path('comment/detail/<int:pk>/', DetailCommentView.as_view()),
    path('comment/create/', CreateCommentView.as_view()),
    path('comment/update/<int:pk>/', UpdateCommentView.as_view()),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view()),
]
