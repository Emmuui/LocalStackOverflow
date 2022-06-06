from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, Tag, Answer
from .serializers import (QuestionSerializer, CreateQuestionSerializer,
                          TagSerializer, AnswerSerializer,
                          CreateAnswerSerializer)
from userapp.models import UserProfile


class QuestionListView(APIView):
    """ Get all question by id of user """

    def get(self, request, pk):
        queryset = Question.objects.filter(username__pk=self.request.user.id)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleQuestionView(APIView):
    """ Get single question """

    def get(self, request, pk):
        queryset = Question.objects.get(id=pk)
        serializer = QuestionSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create question view """

    def check_rating(self):
        qs = Question.objects.filter(username=self.request.user).count()
        return qs

    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)
        print(self.check_rating())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllQuestion(APIView):
    """ Create question view """

    def get(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagView(APIView):
    """ Get all tag """

    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagCreateView(APIView):
    """ Create new tag """

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(APIView):
    """ Get all answer """
    def get(self, request):
        queryset = Answer.objects.all()
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAnswerView(APIView):
    """ Get user answer by his id """

    def get(self, request, pk):
        queryset = Answer.objects.filter(username__pk=self.request.user.id)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateAnswerView(APIView):
    """ Create an answer to a question """

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
