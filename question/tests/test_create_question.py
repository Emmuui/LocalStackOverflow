from django.test import TestCase
from question.models import Question, Answer
from userapp.models import UserProfile
from rest_framework import status
from rest_framework.test import APITestCase
from question.service.record_service import CreateRecord
from question.serializers import CreateQuestionSerializer, OutputQuestionSerializer
from django.urls import reverse


class QuestionTestCase(APITestCase):

    def setUp(self):
        self.user_1 = UserProfile.objects.create(username='TestUser', password='testpassword', rank=100)
        self.client.login(username='john', password='johnpassword')
        self.question_1 = {
            "user": self.user_1.id,
            "title": "Hello from test"
        }

    def test_get_all_questions(self):
        question_1 = Question.objects.create(user=self.user_1, title='Hi')
        question_2 = Question.objects.create(user=self.user_1, title='Bye')
        url = reverse('question_list')
        response = self.client.get(url)
        serializer = OutputQuestionSerializer([question_1, question_2], many=True)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_create_question(self):
        serializer = CreateQuestionSerializer(data=self.question_1)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        expected_data = {
            'title': "Hello from test"
        }
        self.assertEqual(expected_data, validated_data)

