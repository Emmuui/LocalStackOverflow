from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *

from .models import PublicChatRoom, PublicChatUserMessage
from .serializers import PublicChatRoomSerializer


class PublicChatRoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PublicChatRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
