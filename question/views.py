from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from userapp.permissions import IsOwnerOnly
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Question, Tag, Answer, Comment
from .serializers import (QuestionUpdateSerializer, CreateQuestionSerializer,
                          TagSerializer, AnswerSerializer,
                          CreateAnswerSerializer, CommentCreateSerializer,
                          CommentSerializer, OutputQuestionSerializer)
from question.service.record_service import CreateRecord
from userapp.services import UserRating
from .exceptions import RecordPerDayException


class UserQuestionListView(APIView):
    """ Get all question by id of user """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        queryset = Question.objects.filter(user__pk=self.request.user.id)
        serializer = OutputQuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    """ Get single question """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        queryset = Question.objects.get(id=pk)
        serializer = OutputQuestionSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """ Create question view """
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'title': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'tag': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        try:
            serializer = CreateQuestionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            service = CreateRecord(user=self.request.user, data=serializer.validated_data, model='question')
            obj = service.run_system()
            add_rating = UserRating(user=self.request.user)
            add_rating.rating_for_creation_record()
            output_serializer = OutputQuestionSerializer(obj)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except RecordPerDayException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class QuestionListView(APIView):
    """ Create question view """
    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = Question.objects.all()
        serializer = OutputQuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuestionUpdateView(APIView):
    """ Update question """
    permission_classes = (IsOwnerOnly, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'title': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'tag': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def put(self, request, pk, format=None):
        queryset = Question.objects.get(pk=pk)
        serializer = QuestionUpdateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
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
    """ Update current tag """
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


class TagDeleteView(APIView):
    permission_classes = (IsAdminUser,)

    """ Tag comment """

    def delete(self, request, pk, format=None):
        queryset = Tag.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    """ Get all answer """
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Answer.objects.all()
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAnswerView(APIView):
    """ Get user answer by his id """

    def get(self, request):
        queryset = Answer.objects.filter(user__pk=self.request.user.id)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerDetailView(APIView):
    """ Get answer by id """
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        queryset = Answer.objects.get(pk=pk)
        serializer = AnswerSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateAnswerView(APIView):
    """ Create an answer to a question """
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'title': openapi.Schema(type=openapi.TYPE_STRING, description='title'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),
                    'question': openapi.Schema(type=openapi.TYPE_STRING, description='question')}
    ))
    def post(self, request):
        try:
            serializer = CreateAnswerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            service = CreateRecord(user=request.user, data=serializer.validated_data, model='answer')
            obj = service.find_model()
            add_rating = UserRating(user=self.request.user)
            add_rating.rating_for_creation_record()
            output_serializer = AnswerSerializer(obj)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except RecordPerDayException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    """ List of all comments """

    def get(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCommentView(APIView):
    """ Create comment to an answer or a question """

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'text': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='content_type'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='object_id')}
    ))
    def post(self, request):
        try:
            serializer = CommentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            service = CreateRecord(user=request.user, data=serializer.validated_data, model='comment')
            obj = service.find_model()
            add_rating = UserRating(user=self.request.user)
            add_rating.rating_for_creation_record()
            output_serializer = CommentSerializer(obj)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except RecordPerDayException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UpdateCommentView(APIView):
    """ Update comment """
    permission_classes = (IsOwnerOnly, IsAdminUser)

    def put(self, request, pk, format=None):
        queryset = Comment.objects.get(pk=pk)
        serializer = CommentCreateSerializer(queryset, data=request.data)
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
