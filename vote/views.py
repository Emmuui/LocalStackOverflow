from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Vote
from .serializers import CreateVoteSerializer, OutputSerializer
from .services import CountSystem
from .exceptions import TimeValidateException, BaseValidateException, RatingException


class VoteServiceView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'choose_rating': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                    'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='list'),
                    'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='string')})
    )
    def post(self, request):
        try:
            serializer = CreateVoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            val_data = serializer.validated_data
            content_object = val_data.get('content_object')
            count = CountSystem(user=self.request.user, content_object=val_data.get('content_object'),
                                content_type=val_data.get('content_type'),
                                obj_id=val_data.get('object_id'), choose_rating=val_data.get('choose_rating'),
                                first_vote=content_object.voting.filter(user=request.user).first(),
                                previous_vote=content_object.voting.filter(user=request.user).last(),
                                class_name=content_object.__class__.__name__)
            obj = count.run_system()
            output_serializer = OutputSerializer(obj)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except (TimeValidateException, BaseValidateException, RatingException) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class VoteListView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = Vote.objects.all()
        serializer = CreateVoteSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class VoteUserView(APIView):

    def get(self, request, pk):
        queryset = Vote.objects.filter(username__pk=self.request.user.id)
        serializer = CreateVoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
