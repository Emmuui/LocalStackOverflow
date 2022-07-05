from rest_framework import serializers
from .models import PublicChatUserMessage, PublicChatRoom
from userapp.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email']


class PublicChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicChatRoom
        fields = ['title', 'users']


class PublicChatUserMessageSerializer(serializers.ModelSerializer):
    messages = PublicChatRoomSerializer()

    class Meta:
        model = PublicChatUserMessage
        fields = ['user', 'room', 'messages', 'created_at']
        depth = 1
