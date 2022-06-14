from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Vote
from .serializers import VoteSerializer
from .services import CountSystem


class VoteCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'choose_rating': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        count = CountSystem(content_type=request.data['content_type'], obj_id=request.data['object_id'],
                            user=request.user)
        serializer = VoteSerializer(data=request.data)
        print(f'request data = {request.data.get("content_type")}')
        if serializer.is_valid():
            count.validate_user()
            serializer.save(user=self.request.user)
            count.count_vote()
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


class VoteUpdateView(APIView):

    def put(self, request, pk, format=None):
        count = CountSystem(content_type=request.data['content_type'], obj_id=request.data['object_id'],
                            user=request.user)
        queryset = Vote.objects.get(pk=pk)
        serializer = VoteSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            count.count_vote()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
