from rest_framework import serializers
from .models import Question, Tag, Answer


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
        fields = ['username', 'title', 'description',
                  'tag', 'created_at', 'updated_at']


class CreateQuestionSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['username', 'title', 'description', 'tag']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['username', 'title',
                  'description', 'question']


class CreateAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['username', 'title',
                  'description', 'question']

