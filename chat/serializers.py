from rest_framework import serializers
from .models import PublicChatUserMessage, PublicChatRoom


class PublicChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicChatRoom
        fields = ['title', 'users']

