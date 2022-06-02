from rest_framework import serializers
from .models import UserProfile


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']

