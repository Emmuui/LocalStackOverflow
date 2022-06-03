from django.urls import path
from .views import QuestionListView, QuestionCreateView


urlpatterns = [
    path('question_list/<int:pk>', QuestionListView.as_view()),
    path('create_question/', QuestionCreateView.as_view())
]
