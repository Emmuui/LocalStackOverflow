from rest_framework import serializers
from .models import Question, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['username', 'title', 'description', 'tag', 'created_at', 'updated_at']


class CreateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['username', 'title', 'description', ]

    def create(self, validated_data):
        question = Question.objects.create(
            username=validated_data['username'],
            title=validated_data['title'],
            description=validated_data['description'],
        )

        question.save()
        return question
