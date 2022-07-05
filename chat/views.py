from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *

from .models import PublicChatRoom, PublicChatUserMessage
from .serializers import PublicChatRoomSerializer
from django.shortcuts import render


def test(request):
    return render(request, 'chat/test.html')


class PublicChatRoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PublicChatRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

