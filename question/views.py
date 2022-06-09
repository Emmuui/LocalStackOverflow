from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Question, Tag, Answer, Comment
from .serializers import (QuestionSerializer, CreateQuestionSerializer,
                          TagSerializer, AnswerSerializer,
                          CreateAnswerSerializer, CommentSerializer,
                          CommentRelatedSerializer, QuestionUpdateSerializer)
from userapp.permissions import IsOwnerOnly
from userapp.models import UserProfile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserQuestionListView(APIView):
    """ Get all question by id of user """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        queryset = Question.objects.filter(username__pk=self.request.user.id)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    """ Get single question """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        queryset = Question.objects.get(id=pk)
        serializer = QuestionSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create question view """
    permission_classes = (IsAuthenticated, )

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


class QuestionListView(APIView):
    """ Create question view """
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionView(APIView):
    """ Update question """
    permission_classes = (IsOwnerOnly, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='int'),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'tag': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def put(self, request, pk, format=None):
        queryset = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteQuestionView(APIView):
    """ Delete question """

    def delete(self, request, pk, format=None):
        queryset = Question.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagView(APIView):
    """ Get all tag """
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagCreateView(APIView):
    """ Create new tag """
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'name': openapi.Schema(type=openapi.TYPE_STRING, description='int')})
    )
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagUpdateView(APIView):
    """ Create new tag """
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'name': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def put(self, request, pk, format=None):
        queryset = Tag.objects.get(pk=pk)
        serializer = TagSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(APIView):
    """ Get all answer """
    permission_classes = (AllowAny,)

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


class AnswerDetailView(APIView):
    """ Get answer by id """
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = Answer.objects.get(pk=pk)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateAnswerView(APIView):
    """ Create an answer to a question """
    permission_classes = (IsAuthenticated,)

    def rating_add(self, request):
        user = UserProfile.objects.get(pk=request.user.username)
        user.rating += 15
        user.save()
        return user

    def post(self, request):
        serializer = CreateAnswerSerializer(data=request.data)
        if serializer.is_valid():
            self.rating_add(request)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    """ List of all comments """

    def get(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    """ Create comment to an answer or a question """

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCommentView(APIView):
    """ Update comment """
    permission_classes = (IsOwnerOnly, IsAdminUser)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='int'),
                    'text': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def put(self, request, pk, format=None):
        queryset = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(APIView):
    """ Delete comment """

    def delete(self, request, pk, format=None):
        queryset = Comment.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailCommentView(APIView):
    """ Detail single comment by id """

    def get(self, request, pk):
        queryset = Comment.objects.get(id=pk)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)





# Внизу классы которые не корректно работают
class CommentRelatedView(APIView):
    """ Test class """

    def post(self, request):
        serializer = CommentRelatedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentTestRelatedView(APIView):
    """ One more test class """

    def post(self, request):
        serializer = CommentRelatedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
