from rest_framework import serializers
from .models import Question, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateView(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['username', 'title', 'description', 'tag', 'created_at', 'updated_at']


class CreateQuestionSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['username', 'title', 'description', 'tag']
