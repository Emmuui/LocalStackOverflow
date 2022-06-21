from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Question, Tag, Answer, Comment


CONTENT_TYPES_MODEL = ['question', 'answer']


class TagSerializer(serializers.ModelSerializer):
    """ Tag serializer for CRUD views """

    class Meta:
        model = Tag
        fields = '__all__'


class OutputQuestionSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['user', 'title', 'tag', 'description', 'created_at']


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """ Question serializer for update view  """

    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                             write_only=True, many=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'description',
                  'tag']

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        question = Question.objects.create(**validated_data)
        for tag in tags:
            question.tag.add(tag)
        return question


class CreateQuestionSerializer(serializers.ModelSerializer):
    """ Question serializer for create view """
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True,
                                             many=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Question
        fields = ['title', 'tag', 'description']


class AnswerSerializer(serializers.ModelSerializer):
    """ Answer serializer with one additional field for rating """

    question = OutputQuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'user', 'title',
                  'description', 'vote_count', 'question']


class CreateAnswerSerializer(serializers.ModelSerializer):
    """ Answer serializer for create view """

    class Meta:
        model = Answer
        fields = ['user', 'title', 'description', 'question']


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment create serializer  """

    content_type = serializers.SlugRelatedField(queryset=ContentType.objects.filter(model__in=CONTENT_TYPES_MODEL),
                                                slug_field='model')
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, attrs):
        try:
            attrs['content_object'] = attrs['content_type'].model_class().objects.get(pk=attrs['object_id'])
        except:
            raise serializers.ValidationError({'object_id': ['Invalid pk "'+str(attrs['object_id'])+'" - object does not exist.']})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """ Comment serializer with one additional field for rating """

    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent',
                  'created_at', 'updated_at', 'vote_count',
                  'content_type', 'object_id']


