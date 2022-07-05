from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *

from userapp.permissions import IsOwnerOnly
from .models import PublicChatRoom, PublicChatUserMessage, MessageToUser, Chat
from .serializers import PublicChatRoomSerializer, MessageToUserSerializer,\
    PublicChatUserMessageSerializer, GetAllMessageFromChatSerializer
from django.shortcuts import render


class ListMessageByChat(APIView):

    def get(self, request, pk):
        queryset = Chat.objects.get(pk=pk)
        serializer = GetAllMessageFromChatSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageToUserCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = MessageToUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllMessageIfOwnerView(APIView):
    # permission_classes = (IsOwnerOnly, )

    def get(self, request):
        message = MessageToUser.objects.filter(user=self.request.user)
        serializer = MessageToUserSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageListIfRecipientView(APIView):

    def get(self, request):
        message = MessageToUser.objects.filter(recipient=self.request.user)
        serializer = MessageToUserSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomMessageCreate(APIView):

    def post(self, request):
        serializer = PublicChatUserMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomMessageListView(APIView):

    def get(self, request, pk):
        queryset = PublicChatUserMessage.objects.filter(room__pk=pk)
        serializer = PublicChatUserMessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicChatRoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PublicChatRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)












def test(request):
    return render(request, 'chat/test.html')


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

