from rest_framework import serializers
from .models import UserProfile


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']


