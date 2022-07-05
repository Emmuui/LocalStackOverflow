from rest_framework import serializers
from .models import PublicChatUserMessage, PublicChatRoom, MessageToUser, Chat
from userapp.models import UserProfile


class MessageToUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['text', 'chat', 'created_at']


class GetAllMessageFromChatSerializer(serializers.ModelSerializer):
    message_chat = MessageToUserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['first_user', 'second_user', 'message_chat', 'created_at']


class MessageListByOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['user', 'chat', 'created_at']
        depth = 1





class PublicChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicChatRoom
        fields = ['title', 'users']


class PublicChatUserMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicChatUserMessage
        fields = ['room', 'message', 'created_at']


# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'username', 'email']




