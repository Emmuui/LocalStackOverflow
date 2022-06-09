from rest_framework import serializers
from .models import Question, Tag, Answer, Comment
from generic_relations.relations import GenericRelatedField


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class TagCreateView(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class QuestionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['username', 'title', 'description',
                  'tag']


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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"










# Внизу тестовые классы
class GenericField(serializers.RelatedField):

    def to_representation(self, value):

        if isinstance(value, Question):
            return value.id
        elif isinstance(value, Answer):
            return value.id
        raise Exception('Unexpected type of object')


class CommentTestSerializer(serializers.ModelSerializer):
    content_type = GenericField(source='content_object', read_only=True)

    class Meta:
        model = Comment
        fields = ('username', 'text', 'content_type')


""" Test class """
class CommentRelatedSerializer(serializers.ModelSerializer):

    content_object = GenericRelatedField({
        Question: serializers.HyperlinkedRelatedField(
            queryset=Question.objects.all(),
            view_name='question-detail',
        ),
        Answer: serializers.HyperlinkedRelatedField(
            queryset=Answer.objects.all(),
            view_name='answer-detail',
        ),
    })

    class Meta:
        model = Comment
        fields = ('username', 'text', 'content_object')
