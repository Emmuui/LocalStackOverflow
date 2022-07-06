from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import PublicChatUserMessage, PublicChatRoom, MessageToUser, Chat
from userapp.models import UserProfile


class MessageToUserSerializer(serializers.Serializer):
    author = serializers.IntegerField()
    text = serializers.CharField(max_length=5000)
    chat = serializers.IntegerField()
    recipient = serializers.IntegerField()


class OutPutUserMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['author', 'text', 'chat', 'created_at']


class ListOfChatToOneUserSerializer(serializers.ModelSerializer):
    message_chat = OutPutUserMessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['members', 'message_chat', 'created_at']


class MessageListByOneChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['author', 'text', 'chat', 'created_at']
