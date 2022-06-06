from django.urls import path
from .views import (QuestionListView, QuestionCreateView,
                    TagView, SingleQuestionView,
                    TagCreateView, AllQuestion,
                    AnswerView, UserAnswerView, CreateAnswerView)


urlpatterns = [
    path('questionlist_user/<int:pk>', QuestionListView.as_view()),
    path('question_list/', AllQuestion.as_view()),
    path('create_question/', QuestionCreateView.as_view()),
    path('question/<int:pk>', SingleQuestionView.as_view()),
    path('tag/list/', TagView.as_view()),
    path('tag/create/', TagCreateView.as_view()),
    path('answer/list', AnswerView.as_view()),
    path('answer/<int:pk>', UserAnswerView.as_view()),
    path('create_answer/', CreateAnswerView.as_view())
]
