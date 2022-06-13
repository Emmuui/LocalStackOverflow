from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from question.services import vote
from .models import Vote
from .serializers import VoteSerializer


class VoteCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'choose_rating': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteListView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = Vote.objects.all()
        serializer = VoteSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class VoteUserView(APIView):

    def get(self, request, pk):
        queryset = Vote.objects.filter(username__pk=self.request.user.id)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

