from rest_framework import serializers
from .models import PublicChatUserMessage, PublicChatRoom, MessageToUser
from userapp.models import UserProfile


class MessageToUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['text', 'recipient', 'created_at']


class MessageListByOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['owner', 'recipient', 'created_at']
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




